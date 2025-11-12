# AI_PATCHES.md — Patch Creation Guidelines

## 📍 Purpose

This document defines the standard workflow for creating, applying, and managing patch files in this repository. All AI assistants and developers must follow these guidelines to ensure patch compatibility and maintainability.

---

## 🎯 Core Principles

### 1. Patches Are Generated, Never Written

**Rule**: Patches must always be generated from actual file differences, never manually constructed.

**Why**: Patch format is precise and error-prone. Git tools guarantee correct formatting.

**How**:
```bash
# ✅ CORRECT: Generate from actual diff
git diff path/to/file > patches/feature/001-description.patch

# ❌ WRONG: Never manually write patches
# Don't use Write tool or text editor to create patch files
```

### 2. One Logical Change Per Patch

**Rule**: Each patch should represent a single, atomic change.

**Examples**:
- ✅ Add state management to component
- ✅ Update imports for new dependency
- ✅ Refactor function signature
- ❌ Add feature + fix unrelated bug + refactor
- ❌ Multiple unrelated files in one patch

### 3. Patches Must Be Reproducible

**Rule**: Anyone should be able to apply your patch to a clean repository state and get the same result.

**Requirements**:
- Patch applies cleanly with `git apply`
- No manual steps required
- No dependencies on uncommitted changes
- Clear application order (numbered patches)

### 4. Test Before Committing

**Rule**: Always verify patches work before committing them.

**Process**:
```bash
# 1. Generate patch
git diff file.tsx > patches/001-change.patch

# 2. Reset file
git checkout file.tsx

# 3. Test application
git apply --check patches/001-change.patch  # Must succeed
git apply patches/001-change.patch

# 4. Verify result matches expectation
```

---

## 🔄 Standard Workflow

### For AI Assistants

```
1. Read target file
   ↓
2. Apply changes using Edit tool
   ↓
3. Generate patch: git diff > patch-file
   ↓
4. Verify: git apply --check
   ↓
5. Test: reset → apply → verify
   ↓
6. Document patch purpose
```

### For Developers

```
1. Make changes to file(s)
   ↓
2. Review changes: git diff
   ↓
3. Generate patch: git diff > patches/NNN-name.patch
   ↓
4. Test: git checkout → git apply
   ↓
5. Commit patch + modified files
```

---

## 📂 Patch Organization

### Directory Structure

```
patches/
├── feature-name-1/
│   ├── 001-first-change.patch
│   ├── 002-second-change.patch
│   ├── 003-final-change.patch
│   └── README.md                    ← Explain feature & patch order
├── feature-name-2/
│   ├── 001-change.patch
│   └── README.md
└── bugfix-name/
    └── 001-fix.patch
```

### Naming Conventions

**Pattern**: `NNN-brief-description.patch`

- `NNN`: Zero-padded sequential number (001, 002, ..., 100)
- `brief-description`: Lowercase, hyphen-separated, descriptive
- `.patch`: Always use this extension

**Examples**:
```
✅ 001-add-chat-expand-button.patch
✅ 002-implement-state-management.patch
✅ 010-refactor-api-client.patch

❌ patch1.patch                    (not descriptive)
❌ AddChatExpandButton.patch       (wrong case)
❌ fix_bug.patch                   (use hyphens not underscores)
❌ 1-change.patch                  (not zero-padded)
```

### Feature Directories

Each independent feature or fix should have its own directory:

**Structure**:
```
patches/feature-name/
├── README.md              ← Required: explains feature
├── 001-*.patch            ← Numbered patches
├── 002-*.patch
└── IMPLEMENTATION.md      ← Optional: detailed docs
```

**README.md Template**:
```markdown
# Feature Name

## Purpose
Brief description of what this feature does.

## Patches
1. 001-*.patch - Description
2. 002-*.patch - Description

## Application Order
Apply in numerical order: 001, 002, ...

## Dependencies
List any required patches from other features.

## Testing
How to verify the feature works.
```

---

## 🛠️ Patch Generation

### Single File Patch

```bash
# After editing the file
git diff path/to/file.tsx > patches/feature/001-description.patch
```

### Multiple Files (Same Feature)

```bash
# Generate patch for all changed files
git diff > patches/feature/001-multi-file-change.patch

# Or specific files only
git diff file1.tsx file2.tsx > patches/feature/001-two-files.patch
```

### With Specific Context

```bash
# Default: 3 lines of context
git diff path/to/file.tsx > patch.patch

# More context (useful for clarity)
git diff -U5 path/to/file.tsx > patch.patch

# Less context (use cautiously)
git diff -U1 path/to/file.tsx > patch.patch
```

---

## ✅ Patch Verification

### Required Checks

Before committing any patch:

```bash
# 1. Format check: patch is well-formed
git apply --check patches/feature/001-name.patch
# Exit code 0 = success

# 2. Application test: actually apply it
git checkout path/to/file.tsx          # Reset
git apply patches/feature/001-name.patch

# 3. Result check: verify changes are correct
git diff path/to/file.tsx              # Compare with expectation

# 4. Reverse test: can be unapplied cleanly
git apply -R patches/feature/001-name.patch
```

### Visual Inspection

```bash
# View patch contents
cat patches/feature/001-name.patch

# Check for formatting issues
cat -A patches/feature/001-name.patch  # Shows whitespace

# Validate line endings (should be Unix LF)
file patches/feature/001-name.patch
```

---

## 📋 Patch Application

### Basic Application

```bash
# Check if patch will apply
git apply --check patches/feature/001-name.patch

# Apply patch
git apply patches/feature/001-name.patch

# Apply with verbose output
git apply --verbose patches/feature/001-name.patch
```

### Advanced Options

```bash
# Show statistics (what will change)
git apply --stat patches/feature/001-name.patch

# Dry run (don't actually apply)
git apply --check patches/feature/001-name.patch

# Apply with 3-way merge (handles conflicts)
git apply -3 patches/feature/001-name.patch

# Reverse/undo a patch
git apply -R patches/feature/001-name.patch

# Ignore whitespace issues
git apply --whitespace=fix patches/feature/001-name.patch
```

### Applying Patch Series

```bash
# Apply all patches in order
for patch in patches/feature/*.patch; do
    echo "Applying $patch..."
    git apply "$patch" || {
        echo "Failed to apply $patch"
        exit 1
    }
done

# Or with explicit ordering
git apply patches/feature/001-*.patch
git apply patches/feature/002-*.patch
git apply patches/feature/003-*.patch
```

---

## 🔍 Troubleshooting

### When Patches Don't Apply

**Step 1: Check File State**
```bash
# Ensure file is in clean state
git status path/to/file.tsx

# If modified, either commit or stash
git stash
# or
git checkout path/to/file.tsx
```

**Step 2: Check Patch Format**
```bash
# Verify patch is valid
git apply --check patches/feature/001-name.patch

# See detailed error
git apply --verbose patches/feature/001-name.patch 2>&1
```

**Step 3: Inspect Differences**
```bash
# Compare expected vs actual file state
git diff path/to/file.tsx

# Check if file has diverged from patch expectations
cat patches/feature/001-name.patch | head -50
```

**Step 4: Regenerate if Necessary**
```bash
# If patch is corrupt or outdated:
# 1. Manually apply the intended changes
# 2. Generate new patch
git diff path/to/file.tsx > patches/feature/001-name-v2.patch

# 3. Test new patch
git checkout path/to/file.tsx
git apply patches/feature/001-name-v2.patch
```

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "corrupt patch at line X" | Malformed patch format | Regenerate using `git diff` |
| "patch does not apply" | File state mismatch | Reset file, ensure clean state |
| "trailing whitespace" | Whitespace differences | Use `git apply --whitespace=fix` |
| "already exists" | Patch already applied | Check git log or reverse patch |
| Line number mismatch | File has changed | Update patch for current state |

---

## 🎯 Best Practices

### DO ✅

- Generate patches using `git diff` or `diff -u`
- Test patches before committing
- Use descriptive, numbered filenames
- Organize patches by feature/fix
- Document patch purpose and order
- Keep patches atomic and focused
- Include README in patch directories
- Verify patches apply cleanly
- Use consistent naming conventions
- Keep git history clean

### DON'T ❌

- Manually write patch files
- Edit patches in text editor
- Mix unrelated changes in one patch
- Skip patch verification
- Use ambiguous naming
- Apply patches to dirty working tree
- Create patches from uncommitted base
- Omit documentation
- Break working state between patches
- Commit untested patches

---

## 📊 Patch Lifecycle

```
┌─────────────────┐
│  Make Changes   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generate Patch  │ ← git diff > patch
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Verify Format  │ ← git apply --check
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Test Apply    │ ← reset → apply → verify
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Document     │ ← README, comments
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Commit Patch   │ ← git add → git commit
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Upstream Sync   │ ← tools/update_upstream.sh
└─────────────────┘
```

---

## 🔗 Integration with Repository Workflow

### Vendor + Patch Model

This repository uses a **vendor + patch model**:

1. **Upstream code**: `upstream/app/` (read-only)
2. **Customizations**: `patches/` (patch files)
3. **Updates**: Patches reapply after upstream sync

### Update Cycle

```bash
# 1. Import new upstream code
./tools/update_upstream.sh

# 2. Script automatically reapplies all patches
for patch in patches/*/*.patch; do
    git apply "$patch"
done

# 3. Handle any conflicts
# If patch fails, regenerate for new upstream version
```

### Creating New Patches

```bash
# 1. Make changes to upstream files
vim upstream/app/frontend/src/component.tsx

# 2. Generate patch in feature directory
git diff upstream/app/frontend/src/component.tsx > \
    patches/my-feature/001-description.patch

# 3. Document in README
echo "## My Feature" > patches/my-feature/README.md

# 4. Commit patch (not the modified file)
git add patches/my-feature/
git commit -m "Add patch: my-feature"
```

---

## 🧪 Testing Patches

### Manual Testing

```bash
# 1. Clean state
git checkout path/to/file

# 2. Apply patch
git apply patches/feature/001-name.patch

# 3. Run application
npm run dev  # or appropriate command

# 4. Verify feature works
# - Check UI changes
# - Test functionality
# - Look for console errors

# 5. Run test suite
npm test

# 6. Type check
npm run type-check  # or tsc --noEmit
```

### Automated Testing

```bash
# Script to test all patches
#!/bin/bash
for patch in patches/*/*.patch; do
    echo "Testing $patch"

    # Reset to clean state
    git checkout .

    # Apply patch
    if ! git apply "$patch"; then
        echo "❌ Failed: $patch"
        exit 1
    fi

    # Run tests
    if ! npm test; then
        echo "❌ Tests failed after: $patch"
        exit 1
    fi

    echo "✅ Passed: $patch"
done
```

---

## 📝 Documentation Requirements

### Patch-Level Documentation

Each patch should be self-documenting through:

- **Filename**: Clear, descriptive name
- **Commit message**: Explains what and why
- **Comments**: In patch header (optional)

### Feature-Level Documentation

Each patch directory should include:

- **README.md**: Feature overview, patch list, application order
- **IMPLEMENTATION.md** (optional): Detailed technical docs
- **TESTING.md** (optional): Test procedures

---

## 🎓 Examples

### Example 1: Simple Single-File Change

```bash
# 1. Edit file
vim upstream/app/frontend/src/Button.tsx

# 2. Review change
git diff upstream/app/frontend/src/Button.tsx

# 3. Generate patch
mkdir -p patches/button-variant
git diff upstream/app/frontend/src/Button.tsx > \
    patches/button-variant/001-add-outline-variant.patch

# 4. Document
cat > patches/button-variant/README.md << 'EOF'
# Button Variant Feature

## Purpose
Adds outline variant to Button component.

## Patches
- 001-add-outline-variant.patch - Adds outline styling option

## Testing
npm run dev → navigate to /components → verify outline button
EOF

# 5. Test
git checkout upstream/app/frontend/src/Button.tsx
git apply patches/button-variant/001-add-outline-variant.patch
npm run dev  # Manual verification

# 6. Commit
git add patches/button-variant/
git commit -m "feat: Add outline variant to Button

Applied patch: 001-add-outline-variant.patch"
```

### Example 2: Multi-File Feature

```bash
# 1. Make changes to multiple files
vim upstream/app/frontend/src/hooks/useAuth.ts
vim upstream/app/frontend/src/components/LoginForm.tsx

# 2. Generate single patch for related changes
git diff > patches/auth-refactor/001-extract-auth-hook.patch

# 3. Document
cat > patches/auth-refactor/README.md << 'EOF'
# Auth Refactor

## Purpose
Extracts authentication logic into reusable hook.

## Patches
- 001-extract-auth-hook.patch - Creates useAuth hook + updates LoginForm

## Application Order
Apply single patch.

## Testing
- Login still works
- Logout still works
- Session persists on refresh
EOF

# 4. Test and commit
git checkout upstream/app/frontend/src/hooks/useAuth.ts \
             upstream/app/frontend/src/components/LoginForm.tsx
git apply patches/auth-refactor/001-extract-auth-hook.patch
npm test
git add patches/auth-refactor/
git commit -m "refactor: Extract auth logic into useAuth hook"
```

---

## 🔔 Summary for AI Agents

**Golden Rules**:

1. **Never write patches manually** → Always use `git diff`
2. **Always apply changes first** → Then generate patch
3. **Always test patches** → Reset → Apply → Verify
4. **One logical change per patch** → Keep patches atomic
5. **Document everything** → README files in patch directories

**Standard Workflow**:
```
Edit file → git diff > patch → git apply --check → Test → Commit
```

**If patch fails**:
```
Don't fix patch manually → Regenerate from git diff
```

---

## 📚 Related Documentation

- **AI.md** - Repository workflow (vendor + patch model)
- **AI_TS.md** - TypeScript coding standards
- **AI_PYTHON.md** - Python coding standards
- **CLAUDE.md** - Project-specific coding rules

---

*This AI_PATCHES.md is binding for all automated assistants operating on this repository.*
