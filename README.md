# Open Notebook - My Fork

This is a fork of [Open Notebook](https://github.com/lfnovo/open-notebook) - an open source, privacy-focused alternative to Google's Notebook LM.

> **📖 For full documentation, features, and installation instructions, see the [original README.md](upstream/app/README.md) or visit the [official repository](https://github.com/lfnovo/open-notebook).**

---

## 🎯 Added Features

This fork adds the following features on top of the original Open Notebook:

### 1. 💬 Chat Fullscreen Toggle

Expand/collapse chat interface for better focus and screen real estate.

**Key Features:**
- 🔲 **Expand Button**: Toggle button in chat panel header
- 📏 **Full Width Chat**: Hide Sources/Notes columns to expand chat
- ↩️ **Quick Restore**: Collapse button to restore 3-column layout
- 🎯 **Better Focus**: More comfortable chat experience without distractions
- 📱 **Works Everywhere**: Available in both Notebooks and Sources pages

**Technical Details:**
- React state management for expand/collapse
- CSS Grid layout adjustments
- Maximize/Minimize icons from lucide-react
- Zero breaking changes to existing functionality

**Patches:** 4 patches (`001-004`) in `patches/chat-fullscreen-toggle/`

**Documentation:**
- [Quick Start Guide](patches/chat-fullscreen-toggle/00-READ-ME-FIRST.md)
- [Implementation Guide](patches/chat-fullscreen-toggle/PATCH_IMPLEMENTATION_GUIDE.md)
- [Visual Guide](patches/chat-fullscreen-toggle/VISUAL_GUIDE.md)

---

### 2. 📢 Source Direct TTS (Text-to-Speech)

Generate direct text-to-speech audio from source documents without podcast-style transformation.

**Key Features:**
- 🎙️ **Direct Reading**: Reads source text as-is in the original language
- 🔊 **Audio Player**: In-browser audio playback with seek/scrub controls
- 📦 **Automatic Chunking**: Splits long texts (>4000 chars) for processing
- 💾 **Persistent Storage**: Audio files saved and linked to sources
- 🔄 **Regeneration**: Re-generate audio with different settings
- ⬇️ **Download**: Download audio files for offline use
- 🗑️ **Cleanup**: Delete generated audio when no longer needed
- ⏱️ **Progress Tracking**: Real-time status updates during generation

**Technical Details:**
- Supports multiple TTS providers (OpenAI, ElevenLabs, etc.)
- HTTP range request support for audio streaming
- Database migration (migration 10) for schema changes
- Command-based async processing
- Error handling with detailed feedback
- Chunking with sentence boundary detection

**Patches:** 20 patches (`001-020`) in `patches/source-direct-tts/`
- Patches 015-016 are debug/diagnostic patches (optional)
- Patch 019 adds preload metadata (optional enhancement)
- Core functionality: patches 001-011, 013-014, 017-018, 020

**Documentation:**
- [Feature Overview](patches/source-direct-tts/README.md)
- [Implementation Guide](patches/source-direct-tts/IMPLEMENTATION.md)
- [Bug Fixes Documentation](patches/source-direct-tts/FIXES_v2.md)

---

## 📦 Installation

Follow the standard [Open Notebook installation instructions](upstream/app/README.md), then apply the patches for the features you want:

### Option 1: Install All Features

```bash
cd /path/to/my-notebook-lm

# Feature 1: Chat Fullscreen Toggle
git apply patches/chat-fullscreen-toggle/001-add-chat-expand-chatcolumn.patch
git apply patches/chat-fullscreen-toggle/002-add-chat-expand-page.patch
git apply patches/chat-fullscreen-toggle/003-add-chat-expand-chatpanel.patch
git apply patches/chat-fullscreen-toggle/004-add-chat-expand-sources-page.patch

# Feature 2: Source Direct TTS (Core patches)
git apply patches/source-direct-tts/001-add-audio-fields-domain.patch
git apply patches/source-direct-tts/002-add-tts-command.patch
git apply patches/source-direct-tts/003-add-audio-endpoints.patch
git apply patches/source-direct-tts/004-add-audio-api-client.patch
git apply patches/source-direct-tts/005-add-audio-ui-integration.patch
git apply patches/source-direct-tts/006-fix-register-tts-command.patch
git apply patches/source-direct-tts/007-fix-error-handling-ui.patch
git apply patches/source-direct-tts/008-fix-audio-response-type.patch
git apply patches/source-direct-tts/009-fix-failed-status-detection.patch
git apply patches/source-direct-tts/010-fix-error-message-display.patch
git apply patches/source-direct-tts/011-fix-typescript-audio-status-interface.patch
git apply patches/source-direct-tts/013-use-absolute-path-for-audio-file.patch
git apply patches/source-direct-tts/014-fix-api-status-when-audio-exists.patch
git apply patches/source-direct-tts/017-add-migration-for-audio-fields.patch  # 🔴 Database schema
git apply patches/source-direct-tts/018-enable-audio-streaming-range-requests.patch
git apply patches/source-direct-tts/020-fix-audio-authentication-with-blob-url.patch  # 🔴 Authentication

# Rebuild and restart
docker-compose up --build -d
```

### Option 2: Install Individual Features

#### Chat Fullscreen Toggle Only
```bash
cd /path/to/my-notebook-lm
git apply patches/chat-fullscreen-toggle/*.patch
# Restart frontend or rebuild container
```

#### Source Direct TTS Only
```bash
cd /path/to/my-notebook-lm
# Apply patches (see full list above)
docker-compose up --build -d  # Required for migration
```

---

## 📂 Repository Structure

```
my-notebook-lm/
├── patches/
│   ├── chat-fullscreen-toggle/    # Feature 1: Chat expand/collapse
│   │   ├── 001-*.patch            # 4 patches
│   │   ├── 00-READ-ME-FIRST.md    # Quick start
│   │   ├── PATCH_README.md
│   │   └── *.md                   # Documentation
│   │
│   └── source-direct-tts/         # Feature 2: Direct TTS
│       ├── 001-*.patch            # 17 patches
│       ├── README.md              # Feature overview
│       ├── IMPLEMENTATION.md
│       └── FIXES_v2.md            # Bug fixes
│
├── upstream/                      # Original Open Notebook (read-only)
│   └── app/
│       ├── README.md             # Original documentation
│       └── ...
│
└── README.md                     # This file
```

---

## 🛠️ Development Notes

### Patch Organization
- Each feature has its own subdirectory under `patches/`
- One subdirectory = one feature
- Never modify `upstream/app/` directly
- All customizations are applied via Git patches

### Updating Upstream
When updating the original Open Notebook:
```bash
cd upstream/app
git pull origin main
cd ../..
# Re-apply patches if needed
```

---

## 📝 License

This project inherits the MIT License from the original Open Notebook project.

See [LICENSE](upstream/app/LICENSE) for details.

---

## 🙏 Credits

- **Original Project**: [Open Notebook](https://github.com/lfnovo/open-notebook) by [@lfnovo](https://github.com/lfnovo)
- **Community**: Join the [Discord server](https://discord.gg/37XJPXfz2w) for support and discussions

---

## 🔗 Links

- **Original Repository**: https://github.com/lfnovo/open-notebook
- **Official Website**: https://www.open-notebook.ai
- **Documentation**: See [upstream/app/README.md](upstream/app/README.md)

---

## 📊 Summary

| Feature | Patches | Status | Complexity |
|---------|---------|--------|------------|
| Chat Fullscreen Toggle | 4 | ✅ Stable | Low |
| Source Direct TTS | 20 (16 core) | ✅ Stable | Medium |

**Total Features**: 2
**Total Patches**: 24 (20 core)
**Installation Time**: ~10 minutes
