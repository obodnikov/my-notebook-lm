# Open Notebook - My Fork

This is a fork of [Open Notebook](https://github.com/lfnovo/open-notebook) - an open source, privacy-focused alternative to Google's Notebook LM.

> **📖 For full documentation, features, and installation instructions, see the [original README.md](upstream/app/README.md) or visit the [official repository](https://github.com/lfnovo/open-notebook).**

---

## 🎯 Added Features

This fork adds the following features on top of the original Open Notebook:

### 📢 Source Direct TTS (Text-to-Speech)

Generate direct text-to-speech audio from source documents without podcast-style transformation.

**Key Features:**
- 🎙️ **Direct Reading**: Reads source text as-is in the original language
- 🔊 **Audio Player**: In-browser audio playback with seek/scrub controls
- 📦 **Automatic Chunking**: Splits long texts (>4000 chars) for processing
- 💾 **Persistent Storage**: Audio files saved and linked to sources
- 🔄 **Regeneration**: Re-generate audio with different settings
- ⬇️ **Download**: Download audio files for offline use
- 🗑️ **Cleanup**: Delete generated audio when no longer needed

**Technical Details:**
- Supports multiple TTS providers (OpenAI, ElevenLabs, etc.)
- HTTP range request support for streaming
- Progress tracking with status polling
- Error handling with retry functionality
- Database migration for schema changes

**Patches:** 18 patches (`001-018`) in `patches/source-direct-tts/`

**Documentation:**
- [Implementation Guide](patches/source-direct-tts/IMPLEMENTATION.md)
- [Bug Fixes](patches/source-direct-tts/FIXES_v2.md)
- [Feature Description](patches/source-direct-tts/README.md)

---

## 📦 Installation

Follow the standard [Open Notebook installation instructions](upstream/app/README.md), then apply the patches:

```bash
cd /path/to/my-notebook-lm

# Apply Source Direct TTS patches
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
git apply patches/source-direct-tts/017-add-migration-for-audio-fields.patch
git apply patches/source-direct-tts/018-enable-audio-streaming-range-requests.patch

# Rebuild and restart
docker-compose up --build -d
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
