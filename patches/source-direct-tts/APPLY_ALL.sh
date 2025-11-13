#!/bin/bash
# Apply all Source Direct TTS patches in order

set -e  # Exit on any error

cd "$(dirname "$0")/../.."  # Go to repo root

echo "Applying Source Direct TTS patches..."
echo ""

# Original feature patches (1-5)
echo "==> Applying feature patches (001-005)..."
git apply patches/source-direct-tts/001-add-audio-fields-domain.patch
git apply patches/source-direct-tts/002-add-tts-command.patch
git apply patches/source-direct-tts/003-add-audio-endpoints.patch
git apply patches/source-direct-tts/004-add-audio-api-client.patch
git apply patches/source-direct-tts/005-add-audio-ui-integration.patch

# First round of bug fixes (6-7)
echo "==> Applying first round of fixes (006-007)..."
git apply patches/source-direct-tts/006-fix-register-tts-command.patch
git apply patches/source-direct-tts/007-fix-error-handling-ui.patch

# Second round of bug fixes (8-11)
echo "==> Applying second round of fixes (008-011)..."
git apply patches/source-direct-tts/008-fix-audio-response-type.patch
git apply patches/source-direct-tts/009-fix-failed-status-detection.patch
git apply patches/source-direct-tts/010-fix-error-message-display.patch
git apply patches/source-direct-tts/011-fix-typescript-audio-status-interface.patch

echo ""
echo "✅ All 11 patches applied successfully!"
echo ""
echo "Next steps:"
echo "1. Restart backend (docker compose restart or similar)"
echo "2. Rebuild frontend (if needed)"
echo "3. Test audio generation on a source"
echo ""
git status
