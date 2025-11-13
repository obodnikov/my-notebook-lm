"""
Direct text-to-speech generation for sources.

This module provides direct TTS conversion without podcast-style transformation,
reading source text as-is in the original language.
"""

import time
from pathlib import Path
from typing import Optional, List
import tempfile

from loguru import logger
from pydantic import BaseModel
from surreal_commands import CommandInput, CommandOutput, command

from open_notebook.config import DATA_FOLDER
from open_notebook.database.repository import ensure_record_id, repo_query
from open_notebook.domain.notebook import Source
from open_notebook.domain.models import model_manager


class SourceTTSInput(CommandInput):
    """Input for source TTS generation"""
    source_id: str
    chunk_size: int = 4000  # Characters per chunk (safe for most TTS providers)


class SourceTTSOutput(CommandOutput):
    """Output from source TTS generation"""
    success: bool
    audio_file_path: Optional[str] = None
    processing_time: float
    chunks_processed: int = 0
    total_characters: int = 0
    warning_message: Optional[str] = None
    error_message: Optional[str] = None


def split_text_into_chunks(text: str, chunk_size: int = 4000) -> List[str]:
    """
    Split text into chunks, trying to break at sentence boundaries.

    Args:
        text: The text to split
        chunk_size: Maximum characters per chunk

    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    current_chunk = ""

    # Split by sentences (basic approach)
    sentences = text.replace('! ', '!|').replace('? ', '?|').replace('. ', '.|').split('|')

    for sentence in sentences:
        # If adding this sentence exceeds chunk size, save current chunk and start new one
        if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += " " + sentence if current_chunk else sentence

    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


async def concatenate_audio_files(audio_files: List[Path], output_path: Path) -> None:
    """
    Concatenate multiple audio files into one.

    Args:
        audio_files: List of paths to audio files
        output_path: Path where to save the concatenated audio
    """
    try:
        # Use pydub for audio concatenation if available
        try:
            from pydub import AudioSegment

            combined = AudioSegment.empty()
            for audio_file in audio_files:
                audio = AudioSegment.from_mp3(str(audio_file))
                combined += audio

            combined.export(str(output_path), format="mp3")
            logger.info(f"Concatenated {len(audio_files)} audio files using pydub")

        except ImportError:
            # Fallback: simple binary concatenation (works for MP3)
            logger.warning("pydub not available, using simple concatenation")
            with open(output_path, 'wb') as outfile:
                for audio_file in audio_files:
                    with open(audio_file, 'rb') as infile:
                        outfile.write(infile.read())
            logger.info(f"Concatenated {len(audio_files)} audio files using binary concatenation")

    except Exception as e:
        logger.error(f"Error concatenating audio files: {e}")
        raise


@command("generate_source_audio", app="open_notebook")
async def generate_source_audio_command(
    input_data: SourceTTSInput,
) -> SourceTTSOutput:
    """
    Generate direct text-to-speech audio from source content.

    This command:
    1. Fetches the source text
    2. Splits into chunks if necessary
    3. Generates TTS for each chunk
    4. Concatenates chunks into final audio file
    5. Stores audio file path in source record
    """
    start_time = time.time()
    warning_message = None

    try:
        logger.info(f"Starting TTS generation for source: {input_data.source_id}")

        # 1. Load source
        source = await Source.get(input_data.source_id)
        if not source:
            raise ValueError(f"Source {input_data.source_id} not found")

        if not source.full_text:
            raise ValueError(f"Source {input_data.source_id} has no text content")

        text = source.full_text
        total_characters = len(text)
        logger.info(f"Source text length: {total_characters} characters")

        # 2. Get TTS model
        tts_model = await model_manager.get_text_to_speech()
        if not tts_model:
            raise ValueError("No default TTS model configured. Please configure a TTS model in Settings → Models.")

        logger.info(f"Using TTS model: {tts_model}")

        # 3. Split text into chunks if needed
        chunks = split_text_into_chunks(text, input_data.chunk_size)
        num_chunks = len(chunks)

        if num_chunks > 1:
            warning_message = (
                f"Source text was split into {num_chunks} chunks for processing. "
                f"Total length: {total_characters} characters."
            )
            logger.warning(warning_message)

        logger.info(f"Processing {num_chunks} chunk(s)")

        # 4. Create output directory
        output_dir = Path(f"{DATA_FOLDER}/sources/{input_data.source_id}")
        output_dir.mkdir(parents=True, exist_ok=True)

        # 5. Generate TTS for each chunk
        audio_files = []

        for i, chunk in enumerate(chunks, 1):
            logger.info(f"Generating audio for chunk {i}/{num_chunks} ({len(chunk)} chars)")

            if num_chunks ==  1:
                chunk_file = output_dir / "audio.mp3"
            else:
                chunk_file = output_dir / f"audio_chunk_{i:03d}.mp3"

            # Generate speech using Esperanto TTS model
            audio_response = await tts_model.agenerate_speech(
                text=chunk,
                # Default voice will be used from model configuration
            )

            # Save audio chunk
            tts_model.save_audio(audio_response.audio_data, str(chunk_file))
            audio_files.append(chunk_file)

            logger.info(f"Saved chunk {i} to {chunk_file}")

        # 6. Concatenate chunks if multiple
        final_audio_path = output_dir / "audio.mp3"

        if num_chunks > 1:
            logger.info(f"Concatenating {num_chunks} audio chunks...")
            await concatenate_audio_files(audio_files, final_audio_path)

            # Clean up chunk files
            for chunk_file in audio_files:
                if chunk_file != final_audio_path:
                    chunk_file.unlink()
                    logger.debug(f"Deleted temporary chunk: {chunk_file}")

        # 7. Update source record with audio file path
        source.audio_file = str(final_audio_path)
        source.audio_generation_command = (
            ensure_record_id(input_data.execution_context.command_id)
            if input_data.execution_context
            else None
        )
        await source.save()

        processing_time = time.time() - start_time
        logger.info(
            f"Successfully generated audio for source {input_data.source_id} "
            f"in {processing_time:.2f}s ({num_chunks} chunks, {total_characters} chars)"
        )

        return SourceTTSOutput(
            success=True,
            audio_file_path=str(final_audio_path),
            processing_time=processing_time,
            chunks_processed=num_chunks,
            total_characters=total_characters,
            warning_message=warning_message,
        )

    except Exception as e:
        processing_time = time.time() - start_time
        error_message = str(e)
        logger.error(f"Failed to generate audio for source {input_data.source_id}: {error_message}")
        logger.exception(e)

        return SourceTTSOutput(
            success=False,
            processing_time=processing_time,
            error_message=error_message,
        )
