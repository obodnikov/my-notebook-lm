# Source Direct Text-to-Speech Feature

## 📋 Overview

This feature adds direct text-to-speech (TTS) audio generation for source content in Open Notebook. Unlike the podcast feature which creates conversational multi-speaker content, this provides a simple, direct audio reading of the source text as-is in its original language.

## ✨ Features

- **Direct TTS Generation**: Converts source text directly to audio without transformation
- **Automatic Chunking**: Handles long texts by splitting into chunks and concatenating
- **Async Processing**: Background job processing with status tracking
- **Audio Player**: In-browser HTML5 audio player with download option
- **Warning Messages**: Alerts users when content is split into chunks
- **Multiple Actions**: Generate, download, regenerate, and delete audio

## 📦 Patch Files

All patches should be applied in order:

### Backend Patches

1. **001-add-audio-fields-domain.patch** (753 bytes)
   - Adds `audio_file` and `audio_generation_command` fields to Source model
   - File: `upstream/app/open_notebook/domain/notebook.py`

2. **002-add-tts-command.patch** (8.3K)
   - Creates TTS command with chunking logic
   - File: `upstream/app/commands/source_tts_commands.py` (new file)
   - Features:
     - Text chunking (4000 chars per chunk)
     - Audio concatenation
     - Warning messages for long texts
     - Uses system default TTS model

3. **003-add-audio-endpoints.patch** (8.2K)
   - Adds 4 new API endpoints
   - File: `upstream/app/api/routers/sources.py`
   - Endpoints:
     - `POST /sources/{id}/generate-audio` - Start generation
     - `GET /sources/{id}/audio` - Stream/download audio
     - `GET /sources/{id}/audio/status` - Check status
     - `DELETE /sources/{id}/audio` - Delete audio

### Frontend Patches

4. **004-add-audio-api-client.patch** (1.5K)
   - Adds TypeScript API client methods
   - File: `upstream/app/frontend/src/lib/api/sources.ts`
   - Methods: `generateAudio`, `getAudio`, `getAudioStatus`, `deleteAudio`

5. **005-add-audio-ui-integration.patch** (4.1K)
   - Integrates audio feature into Source Detail UI
   - File: `upstream/app/frontend/src/components/source/SourceDetailContent.tsx`
   - Changes:
     - New "Audio" tab in the tabs navigation
     - "Generate Audio Reading" option in dropdown menu
     - Audio player component with controls
     - Status polling during generation
     - Warning message display

### Bug Fix Patches (REQUIRED!)

6. **006-fix-register-tts-command.patch** (750 bytes) 🔴 **CRITICAL**
   - Registers TTS command with surreal-commands worker
   - File: `upstream/app/commands/__init__.py`
   - **Without this patch, the feature will not work!**
   - **IMPORTANT**: Restart backend after applying

7. **007-fix-error-handling-ui.patch** (4.1K) 🟠 **IMPORTANT**
   - Adds timeout to polling (5 minutes max)
   - Wraps polling in try-catch for error handling
   - Adds failed state UI in Audio tab
   - Improves error messages
   - File: `upstream/app/frontend/src/components/source/SourceDetailContent.tsx`
   - **Without this patch, errors will cause infinite loading**

> **⚠️ Note**: Patches 006-007 fix critical issues found during testing. See [FIXES.md](FIXES.md) for details.

## 🚀 Installation

### Prerequisites

- Open Notebook installation
- TTS model configured in Settings → Models
- Python backend with all dependencies installed
- React frontend built and running

### Apply Patches

```bash
cd /home/mike/src/my-notebook-lm

# Apply patches in order (1-5: feature implementation)
git apply patches/source-direct-tts/001-add-audio-fields-domain.patch
git apply patches/source-direct-tts/002-add-tts-command.patch
git apply patches/source-direct-tts/003-add-audio-endpoints.patch
git apply patches/source-direct-tts/004-add-audio-api-client.patch
git apply patches/source-direct-tts/005-add-audio-ui-integration.patch

# Apply patches (6-7: critical bug fixes) - REQUIRED!
git apply patches/source-direct-tts/006-fix-register-tts-command.patch
git apply patches/source-direct-tts/007-fix-error-handling-ui.patch

# Verify all patches applied successfully
git status
```

> **⚠️ IMPORTANT**: Patches 006 and 007 are REQUIRED bug fixes. Without them:
> - Patch 006: Feature will not work (command not found error)
> - Patch 007: Errors will cause infinite loading with no user feedback

### Database Migration

No explicit database migration is required. The new fields (`audio_file` and `audio_generation_command`) will be automatically available in SurrealDB for Source records.

### Restart Services

```bash
# Restart backend
cd upstream/app
# Your restart command here

# Rebuild frontend
cd frontend
npm run build

# Or for development
npm run dev
```

## 💡 Usage

### From the UI

1. **Navigate** to any source detail page
2. **Click** the three-dot menu (⋮) in the top right
3. **Select** "Generate Audio Reading"
4. **Wait** for generation to complete (status updates automatically)
5. **Go** to the "Audio" tab
6. **Play** audio directly in browser or download MP3

### Via API

```bash
# Generate audio
curl -X POST http://localhost:5055/api/sources/{source_id}/generate-audio

# Check status
curl http://localhost:5055/api/sources/{source_id}/audio/status

# Download audio
curl http://localhost:5055/api/sources/{source_id}/audio --output audio.mp3

# Delete audio
curl -X DELETE http://localhost:5055/api/sources/{source_id}/audio
```

## 🎯 How It Works

### Text Chunking

For sources with more than 4000 characters:

1. Text is split at sentence boundaries
2. Each chunk is processed individually
3. Audio chunks are concatenated into a single MP3
4. User receives a warning about the splitting

### TTS Model Selection

The feature uses the **default TTS model** configured in Open Notebook Settings:

- Settings → Models → Text-to-Speech
- Supports: OpenAI TTS, ElevenLabs, Google TTS, Local TTS (Speaches)
- Uses default voice from the model configuration

### Async Processing

- Generation runs in the background using surreal-commands
- Status is polled every 2 seconds
- No blocking of the UI
- Multiple sources can be processed simultaneously

## 📊 Technical Details

### Storage

Audio files are stored at:
```
./data/sources/{source_id}/audio.mp3
```

### Dependencies

**Backend:**
- `esperanto` - TTS model abstraction
- `surreal-commands` - Async job processing
- `pydub` (optional) - Better audio concatenation

**Frontend:**
- React hooks for state management
- Axios for API calls
- HTML5 `<audio>` element for playback

### Error Handling

- Missing TTS model → Clear error message
- No text content → HTTP 400 error
- Generation failure → Job status reflects error
- File not found → HTTP 404 with helpful message

## 🔧 Configuration

### Chunk Size

Default: 4000 characters

To modify, edit `source_tts_commands.py`:

```python
command_input = SourceTTSInput(
    source_id=str(source.id),
    chunk_size=4000,  # Adjust this value
)
```

### Audio Quality

Quality depends on the TTS model configured. For best results:

1. Use premium TTS providers (OpenAI, ElevenLabs)
2. Or configure local TTS with high-quality models
3. See `docs/features/local_tts.md` for local setup

## 🐛 Troubleshooting

### "No default TTS model configured"

**Solution**: Go to Settings → Models and configure a Text-to-Speech model

### Audio generation stuck at "running"

**Check**:
```bash
# View surreal-commands logs
# Check backend logs for errors
```

**Solution**: Restart backend or retry generation

### Audio not playing in browser

**Causes**:
- Browser doesn't support MP3
- File path incorrect
- CORS issues

**Solution**: Download MP3 and play locally

### Poor audio quality

**Solutions**:
- Use a premium TTS provider
- Check TTS model configuration
- Ensure text is well-formatted (no special characters)

## 📝 Comparison with Podcast Feature

| Feature | Direct TTS (This) | Podcast Feature |
|---------|-------------------|-----------------|
| **Purpose** | Simple audio reading | Conversational podcast |
| **Speakers** | 1 (single voice) | 1-4 (multi-speaker) |
| **Transformation** | None (as-is) | AI-generated conversation |
| **Speed** | Fast (TTS only) | Slower (outline + transcript + TTS) |
| **Location** | Source-level | Notebook-level |
| **Use Case** | Quick audio version | Engaging content |

## 🔐 Security Considerations

- Audio files stored in `./data/` directory
- No public access without authentication
- File paths validated to prevent directory traversal
- Audio files cleaned up when source is deleted

## 📈 Performance

- **Small sources** (< 4000 chars): ~5-15 seconds
- **Medium sources** (4000-20000 chars): ~30-60 seconds
- **Large sources** (20000+ chars): ~2-5 minutes

*Times vary based on TTS provider and text length*

## 🤝 Contributing

To extend this feature:

1. Follow `AI_PATCHES.md` guidelines
2. Create new patches in this directory
3. Update this README with changes
4. Test all patches apply cleanly

## 📚 Related Documentation

- [AI.md](../../AI.md) - Repository patch workflow
- [AI_PATCHES.md](../../AI_PATCHES.md) - Patch creation guidelines
- [AI_TS.md](../../AI_TS.md) - TypeScript standards
- [docs/features/local_tts.md](../../upstream/app/docs/features/local_tts.md) - Local TTS setup
- [docs/features/podcasts.md](../../upstream/app/docs/features/podcasts.md) - Podcast feature

## 📜 License

Same as Open Notebook (MIT License)

## ✅ Success Criteria

After applying all patches, you should be able to:

- [x] See "Generate Audio Reading" in source detail dropdown
- [x] Generate audio for any source with text
- [x] Play audio directly in the "Audio" tab
- [x] Download audio as MP3
- [x] See warning messages for long texts
- [x] Regenerate or delete audio
- [x] Track generation status in real-time

---

**Total Patches**: 5
**Total Changes**: ~30K (compressed)
**Installation Time**: ~5 minutes
**First Audio**: ~30 seconds after installation

🎉 Enjoy direct text-to-speech audio for your sources!
