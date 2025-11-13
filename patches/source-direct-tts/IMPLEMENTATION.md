# Source Direct TTS - Implementation Guide

## 🏗️ Architecture Overview

This feature follows Open Notebook's vendor + patch model, adding text-to-speech capability at the source level without modifying upstream code directly.

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (React)                       │
│  ┌────────────────────────────────────────────────────┐ │
│  │ SourceDetailContent.tsx                            │ │
│  │  ├── Audio Tab                                     │ │
│  │  ├── Generate Audio Button (Dropdown)             │ │
│  │  ├── Audio Player Component                       │ │
│  │  └── Status Polling (2s intervals)                │ │
│  └────────────────────────────────────────────────────┘ │
│                         │                                │
│                         ▼                                │
│  ┌────────────────────────────────────────────────────┐ │
│  │ API Client (sources.ts)                            │ │
│  │  ├── generateAudio()                               │ │
│  │  ├── getAudio()                                    │ │
│  │  ├── getAudioStatus()                              │ │
│  │  └── deleteAudio()                                 │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                         │
                         │ HTTP / REST API
                         ▼
┌─────────────────────────────────────────────────────────┐
│                Backend (FastAPI + Python)                │
│  ┌────────────────────────────────────────────────────┐ │
│  │ API Router (sources.py)                            │ │
│  │  ├── POST /sources/{id}/generate-audio            │ │
│  │  ├── GET  /sources/{id}/audio                     │ │
│  │  ├── GET  /sources/{id}/audio/status              │ │
│  │  └── DELETE /sources/{id}/audio                   │ │
│  └────────────────────────────────────────────────────┘ │
│                         │                                │
│                         ▼                                │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Command (source_tts_commands.py)                   │ │
│  │  ├── split_text_into_chunks()                      │ │
│  │  ├── concatenate_audio_files()                     │ │
│  │  └── generate_source_audio_command()              │ │
│  └────────────────────────────────────────────────────┘ │
│                         │                                │
│                         ▼                                │
│  ┌────────────────────────────────────────────────────┐ │
│  │ TTS Model (Esperanto + AIFactory)                  │ │
│  │  ├── OpenAI TTS                                    │ │
│  │  ├── ElevenLabs                                    │ │
│  │  ├── Google TTS                                    │ │
│  │  └── Local TTS (Speaches)                         │ │
│  └────────────────────────────────────────────────────┘ │
│                         │                                │
│                         ▼                                │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Storage (./data/sources/{id}/audio.mp3)           │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│        Database (SurrealDB)                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Source Model                                       │ │
│  │  ├── audio_file: Optional[str]                     │ │
│  │  └── audio_generation_command: Optional[RecordID] │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 📁 File Changes

### Backend (Python)

#### 1. Domain Model (`notebook.py`)

**Changes**:
- Added two new optional fields to `Source` class
- Both fields are nullable (won't break existing sources)

```python
audio_file: Optional[str] = Field(
    default=None,
    description="Path to generated TTS audio file"
)
audio_generation_command: Optional[Union[str, RecordID]] = Field(
    default=None,
    description="Link to audio generation command"
)
```

**Rationale**:
- `audio_file` stores the file system path for streaming/download
- `audio_generation_command` links to the async job for status tracking

#### 2. TTS Command (`source_tts_commands.py` - NEW FILE)

**Purpose**: Background command for TTS generation

**Key Functions**:

```python
def split_text_into_chunks(text: str, chunk_size: int = 4000) -> List[str]
```
- Splits text at sentence boundaries
- Prevents cutting mid-sentence
- Returns list of text chunks

```python
async def concatenate_audio_files(audio_files: List[Path], output_path: Path)
```
- Uses pydub if available (better quality)
- Falls back to binary concatenation
- Creates single MP3 from multiple chunks

```python
@command("generate_source_audio", app="open_notebook")
async def generate_source_audio_command(input_data: SourceTTSInput) -> SourceTTSOutput
```
- Main command registered with surreal-commands
- Handles entire TTS generation pipeline
- Returns structured output with metadata

**Processing Pipeline**:
1. Fetch source and validate text exists
2. Get default TTS model from model_manager
3. Split text into chunks (if > 4000 chars)
4. Generate TTS for each chunk sequentially
5. Concatenate chunks if multiple
6. Store audio file path in source record
7. Clean up temporary chunk files
8. Return success/failure status

#### 3. API Endpoints (`sources.py`)

**New Endpoints**:

```python
@router.post("/sources/{source_id}/generate-audio")
async def generate_source_audio(source_id: str)
```
- Submits TTS generation as background job
- Checks for existing in-progress jobs
- Returns command_id for status tracking

```python
@router.get("/sources/{source_id}/audio")
async def get_source_audio(source_id: str)
```
- Streams audio file as MP3
- Returns FileResponse with proper media type
- 404 if audio not generated

```python
@router.get("/sources/{source_id}/audio/status")
async def get_audio_generation_status(source_id: str)
```
- Returns comprehensive status information
- Includes command status (queued/running/completed/failed)
- Provides generation metadata (chunks, characters, time)

```python
@router.delete("/sources/{source_id}/audio")
async def delete_source_audio(source_id: str)
```
- Deletes audio file from disk
- Clears database fields
- Returns confirmation message

### Frontend (TypeScript/React)

#### 4. API Client (`sources.ts`)

**New Methods**:

```typescript
generateAudio: async (id: string) => Promise<{
  message: string
  command_id: string
  source_id: string
  status: string
}>
```
- Triggers audio generation
- Returns job information

```typescript
getAudio: async (id: string) => Promise<AxiosResponse<Blob>>
```
- Downloads audio as Blob
- Used for download and streaming

```typescript
getAudioStatus: async (id: string) => Promise<{
  source_id: string
  has_audio: boolean
  audio_file: string | null
  command_status: string | null
  command_info: {...} | null
  command_id: string | null
}>
```
- Polls generation status
- Returns detailed progress information

```typescript
deleteAudio: async (id: string) => Promise<{ message: string }>
```
- Deletes generated audio

#### 5. UI Integration (`SourceDetailContent.tsx`)

**State Management**:

```typescript
const [audioStatus, setAudioStatus] = useState<{
  has_audio: boolean
  command_status: string | null
  warning_message?: string
} | null>(null)
const [isGeneratingAudio, setIsGeneratingAudio] = useState(false)
const [isDeletingAudio, setIsDeletingAudio] = useState(false)
```

**New Functions**:

```typescript
const fetchAudioStatus = useCallback(async () => {...}, [sourceId])
```
- Fetches current audio status on component mount
- Called in useEffect alongside other data fetching

```typescript
const handleGenerateAudio = async () => {...}
```
- Triggers generation via API
- Starts status polling (2-second intervals)
- Stops polling when complete/failed
- Shows toast notifications

```typescript
const handleDownloadAudio = async () => {...}
```
- Downloads audio as MP3 file
- Creates temporary blob URL
- Triggers browser download

```typescript
const handleDeleteAudio = async () => {...}
```
- Confirms deletion with user
- Calls delete API
- Refreshes status

**UI Components Added**:

1. **Audio Tab**:
   - 4th tab in the tab navigation
   - Shows checkmark icon when audio exists
   - Contains audio player and controls

2. **Dropdown Menu Item**:
   - "Generate Audio Reading" option
   - Shows status (Generating... / Regenerate)
   - Disabled during generation

3. **Audio Player Section**:
   - HTML5 `<audio>` element for playback
   - Download, Regenerate, Delete buttons
   - Warning message display (for chunked content)
   - Loading state during generation
   - Empty state with generate button

## 🔄 Data Flow

### Generation Flow

```
User clicks "Generate Audio Reading"
            │
            ▼
Frontend: handleGenerateAudio()
            │
            ├── Call API: POST /sources/{id}/generate-audio
            │
            ▼
Backend: generate_source_audio()
            │
            ├── Validate source exists
            ├── Check not already running
            ├── Submit command to surreal-commands
            │
            ▼
Command: generate_source_audio_command()
            │
            ├── 1. Load source text
            ├── 2. Get TTS model
            ├── 3. Split text into chunks
            ├── 4. For each chunk:
            │       ├── Generate TTS
            │       └── Save to temp file
            ├── 5. Concatenate chunks
            ├── 6. Save final audio.mp3
            ├── 7. Update source record
            └── 8. Return success
            │
            ▼
Frontend: Status Polling (every 2s)
            │
            ├── Call API: GET /sources/{id}/audio/status
            ├── Update UI with status
            ├── Check if completed/failed
            └── Stop polling when done
            │
            ▼
User: Audio tab shows player
```

### Playback Flow

```
User navigates to Audio tab
            │
            ▼
Frontend: Renders <audio> element
            │
            └── src="/api/sources/{id}/audio"
            │
            ▼
Browser: Requests audio file
            │
            ▼
Backend: get_source_audio()
            │
            ├── Find audio file path
            ├── Verify file exists
            └── Return FileResponse (streaming)
            │
            ▼
Browser: Plays audio
```

## 🎨 UI States

### Audio Tab States

1. **No Audio Generated**:
   - Empty state with icon
   - "Generate Audio Reading" button
   - Descriptive text

2. **Generating (Queued)**:
   - Loading spinner
   - "Generating audio..." text
   - No controls available

3. **Generating (Running)**:
   - Loading spinner
   - "Generating audio..." text
   - Polling every 2 seconds

4. **Generation Complete**:
   - Audio player with controls
   - Download button
   - Regenerate button
   - Delete button
   - Warning message (if chunked)

5. **Generation Failed**:
   - Error message
   - Retry button

## 🔧 Configuration Options

### Chunk Size

**Location**: `source_tts_commands.py`

```python
chunk_size: int = 4000  # Characters per chunk
```

**Considerations**:
- Too small: More API calls, slower generation
- Too large: May exceed TTS provider limits
- Default 4000: Safe for most providers

### Poll Interval

**Location**: `SourceDetailContent.tsx`

```typescript
const pollInterval = setInterval(async () => {
  // ...status check
}, 2000)  // 2 seconds
```

**Considerations**:
- Faster: More responsive UI, more API calls
- Slower: Less responsive, fewer API calls
- Default 2000ms: Good balance

### Audio Storage Path

**Location**: `source_tts_commands.py`

```python
output_dir = Path(f"{DATA_FOLDER}/sources/{input_data.source_id}")
```

**Structure**:
```
./data/
└── sources/
    └── {source_id}/
        └── audio.mp3
```

## 📊 Database Schema

### Source Table

```sql
-- Existing fields
id: record
title: string
full_text: string
asset: object
...

-- New fields (added by patch)
audio_file: string | null
audio_generation_command: record<command> | null
```

**Migration**: Not required (fields are optional)

## 🐛 Error Handling

### Backend Errors

| Error | HTTP Code | Response | Handling |
|-------|-----------|----------|----------|
| Source not found | 404 | `{detail: "Source not found"}` | Show error toast |
| No text content | 400 | `{detail: "Source has no text..."}` | Show error toast |
| No TTS model configured | 500 | `{detail: "No default TTS model..."}` | Guide user to settings |
| Generation failed | 500 | Command status = "failed" | Show retry option |
| Audio file missing | 404 | `{detail: "Audio file not found..."}` | Allow regeneration |

### Frontend Error Handling

```typescript
try {
  await sourcesApi.generateAudio(source.id)
  toast.success('Generation started')
} catch (error) {
  console.error('Failed:', error)
  toast.error('Failed to start generation')
  setIsGeneratingAudio(false)
}
```

## 🔒 Security

### Path Validation

Audio files are stored in a controlled directory:
- Base path: `./data/sources/`
- No user input in path construction
- Path traversal prevented

### Access Control

- All endpoints require authentication (via API middleware)
- Users can only access their own sources
- Audio files served through authenticated endpoints

### File Cleanup

- Audio files deleted when:
  - User explicitly deletes audio
  - Source is deleted (cascade)
  - Regeneration occurs (old file replaced)

## ⚡ Performance Optimization

### Chunking Strategy

- Split at sentence boundaries (not word boundaries)
- Prevents awkward pauses mid-sentence
- Optimal chunk size balances speed vs quality

### Concurrent Processing

- Each chunk processed sequentially (TTS providers have rate limits)
- Future enhancement: Parallel chunk processing with rate limiting

### Caching

- No caching of audio (files stored on disk)
- Status polling cached by browser (cache headers)

### Audio Concatenation

- Prefers pydub (better quality, proper MP3 merging)
- Falls back to binary concatenation (faster, simpler)

## 🧪 Testing

### Backend Testing

```python
# Test command
async def test_generate_source_audio():
    input_data = SourceTTSInput(source_id="source:123")
    output = await generate_source_audio_command(input_data)
    assert output.success == True
    assert output.audio_file_path is not None
```

### Frontend Testing

```typescript
// Test audio generation
it('should generate audio when button clicked', async () => {
  const {getByText} = render(<SourceDetailContent sourceId="123" />)
  const button = getByText('Generate Audio Reading')
  fireEvent.click(button)
  // Assert API called
})
```

### Manual Testing Checklist

- [ ] Generate audio for small source (< 4000 chars)
- [ ] Generate audio for large source (> 10000 chars)
- [ ] Verify warning message appears for chunked content
- [ ] Play audio in browser
- [ ] Download audio file
- [ ] Regenerate audio (replaces old file)
- [ ] Delete audio
- [ ] Generate while another source is generating (concurrent)
- [ ] Verify status polling stops when complete
- [ ] Test with different TTS providers
- [ ] Test error handling (no TTS model, no text, etc.)

## 📈 Future Enhancements

Potential improvements (not in current patches):

1. **Voice Selection UI**:
   - Let users choose voice before generation
   - Remember preferred voice per user

2. **Speed Control**:
   - Allow speed adjustment (0.5x - 2x)
   - Store in user preferences

3. **Progress Percentage**:
   - Show "Processing chunk 3/5" during generation
   - Real-time progress bar

4. **Batch Generation**:
   - Generate audio for all sources in notebook
   - Queue management

5. **Streaming Generation**:
   - Stream chunks as they're generated
   - Start playback before full completion

6. **Audio Editing**:
   - Trim silence
   - Normalize volume
   - Add intro/outro

## 🤝 Contributing

To extend or modify this feature:

1. Read `AI_PATCHES.md` for patch guidelines
2. Make changes to files (don't modify upstream directly)
3. Generate patches using `git diff`
4. Test patches apply cleanly
5. Update this documentation
6. Submit for review

---

**Implementation Complete**: All components working together to provide direct TTS for sources.
