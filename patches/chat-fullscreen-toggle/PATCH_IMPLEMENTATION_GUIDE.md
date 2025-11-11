# Chat Expand/Collapse Feature - Patch Implementation Guide

## 🎯 Overview

This implementation follows the **vendor + patch model** for this downstream derivative repository. All changes are applied as patches to the upstream code, ensuring clean separation and easy upstream updates.

## 📋 Patch Files Included

1. **001-add-chat-expand-chatcolumn.patch**
   - Adds `isExpanded` and `onToggleExpand` props to ChatColumn
   - Passes props down to ChatPanel component
   
2. **002-add-chat-expand-page.patch**
   - Adds chat expansion state management
   - Modifies layout to conditionally hide Sources/Notes
   - Implements expand/collapse handler
   
3. **003-add-chat-expand-chatpanel.patch**
   - Adds Maximize2/Minimize2 icons import
   - Adds expand/collapse button to header
   - Implements button UI with conditional rendering

## 🔧 Implementation Steps

### Step 1: Backup Current Patches (Recommended)

```bash
# From repository root
cp -r patches patches.backup.$(date +%Y%m%d)
```

### Step 2: Copy Patch Files

```bash
# Create feature subdirectory and copy patches
mkdir -p patches/chat-fullscreen-toggle
cp 001-add-chat-expand-chatcolumn.patch patches/chat-fullscreen-toggle/
cp 002-add-chat-expand-page.patch patches/chat-fullscreen-toggle/
cp 003-add-chat-expand-chatpanel.patch patches/chat-fullscreen-toggle/
```

### Step 3: Apply Patches

#### Option A: Manual Application (Recommended for first time)

```bash
# Navigate to repository root
cd /path/to/your-repo

# Apply each patch individually
git apply patches/chat-fullscreen-toggle/001-add-chat-expand-chatcolumn.patch
git apply patches/chat-fullscreen-toggle/002-add-chat-expand-page.patch
git apply patches/chat-fullscreen-toggle/003-add-chat-expand-chatpanel.patch

# Commit the changes
git commit -am "feat: Add chat expand/collapse functionality

- Add expand/collapse button to chat panel header
- Implement state management for chat expansion
- Hide Sources/Notes columns when chat is expanded
- Preserve chat history and context during toggle"
```

#### Option B: Automated via Update Script

If your repository has an automated patch application system:

```bash
# The update_upstream.sh script will automatically apply patches
./tools/update_upstream.sh
```

### Step 4: Verify Application

```bash
# Check that files were modified
git status

# Review changes
git diff HEAD~1

# Expected modified files:
# - frontend/src/app/(dashboard)/notebooks/components/ChatColumn.tsx
# - frontend/src/app/(dashboard)/notebooks/[id]/page.tsx
# - frontend/src/components/source/ChatPanel.tsx
```

### Step 5: Test the Feature

```bash
# Start dev server
cd frontend
npm run dev

# Navigate to any notebook
# Look for "Expand" button next to "Sessions" in Chat header
# Click to test expand/collapse functionality
```

## 📁 File Structure After Application

```
your-repo/
├── patches/
│   ├── chat-fullscreen-toggle/              ← New feature directory
│   │   ├── 001-add-chat-expand-chatcolumn.patch
│   │   ├── 002-add-chat-expand-page.patch
│   │   └── 003-add-chat-expand-chatpanel.patch
│   └── ... (other feature directories)
├── upstream/
│   └── app/
│       └── frontend/
│           ├── src/
│           │   ├── app/(dashboard)/notebooks/
│           │   │   ├── [id]/
│           │   │   │   └── page.tsx          ← Modified by patch
│           │   │   └── components/
│           │   │       └── ChatColumn.tsx    ← Modified by patch
│           │   └── components/
│           │       └── source/
│           │           └── ChatPanel.tsx     ← Modified by patch
└── tools/
    └── update_upstream.sh
```

## 🔄 How This Works with Upstream Updates

When upstream updates are needed:

1. **Update vendor copy** (done by `update_upstream.sh`):
   ```bash
   git rm -r upstream/app
   git read-tree --prefix=upstream/app -u upstream/main
   ```

2. **Reapply all patches** (including these new ones):
   ```bash
   for dir in patches/*/; do
     for p in "$dir"*.patch; do
       git apply "$p"
     done
   done
   ```

3. **Handle conflicts** (if any):
   - If a patch fails, regenerate it based on new upstream code
   - Keep patch logic intact, adjust line numbers/context as needed

## 🔍 Patch Details

### Patch 001: ChatColumn Props
- **Lines changed**: ~5
- **Risk level**: Low
- **Dependencies**: None
- **Conflicts**: Unlikely (interface change only)

### Patch 002: Page Layout
- **Lines changed**: ~20
- **Risk level**: Low
- **Dependencies**: ChatColumn props
- **Conflicts**: Possible if upstream changes layout structure

### Patch 003: ChatPanel Button
- **Lines changed**: ~30
- **Risk level**: Low
- **Dependencies**: None
- **Conflicts**: Unlikely (adds new UI element)

## 🧪 Testing Checklist

After applying patches:

- [ ] Patches applied without conflicts
- [ ] TypeScript compilation successful
- [ ] No console errors in browser
- [ ] Expand button appears in chat header
- [ ] Sources/Notes hide when expanded
- [ ] Chat takes full width when expanded
- [ ] Collapse restores 3-column layout
- [ ] Chat history preserved during toggle
- [ ] Sessions button still works
- [ ] Mobile responsive works correctly

## 🐛 Troubleshooting

### Patch Application Fails

**Error**: "patch does not apply"

**Solutions**:
1. Check if upstream files have changed significantly
2. Manually apply changes and regenerate patch:
   ```bash
   # Make manual edits to the file
   git diff > patches/00X-fixed-patch.patch
   ```

### Conflicts with Existing Patches

**Issue**: Other patches modify the same files

**Solutions**:
1. Apply patches in correct order (these should be last)
2. Merge patch logic if needed
3. Regenerate combined patch

### TypeScript Errors

**Error**: Type mismatches after application

**Solutions**:
1. Verify all three patches are applied
2. Check import statements are correct
3. Rebuild TypeScript: `npm run build`

## 📝 Maintenance Notes

### Regenerating Patches

If upstream code changes and patches need updates:

```bash
# 1. Apply old patch to see conflicts
git apply patches/chat-fullscreen-toggle/001-add-chat-expand-chatcolumn.patch

# 2. Manually fix conflicts in the file

# 3. Generate new patch
git diff upstream/app/frontend/src/app/(dashboard)/notebooks/components/ChatColumn.tsx > patches/chat-fullscreen-toggle/001-add-chat-expand-chatcolumn.patch

# 4. Repeat for other patches
```

### Keeping Patches Clean

- Each patch should be **atomic** (single logical change)
- Include **clear commit messages** in patch header
- Keep **line context minimal** (3-5 lines before/after)
- **Document rationale** in patch description

## 🎉 Success Criteria

After successful implementation:

✅ Feature directory `patches/chat-fullscreen-toggle/` created  
✅ Three patch files in feature directory  
✅ Patches apply cleanly to upstream code  
✅ Feature works as expected in browser  
✅ No breaking changes to existing functionality  
✅ Patches are ready for next upstream update cycle  

## 📚 References

- **AI.md** - Repository patch workflow guidelines
- **tools/update_upstream.sh** - Automated patch application script
- **AI_TS.md** - TypeScript coding standards

---

**Note**: This implementation follows the repository's vendor + patch model as defined in AI.md. Never modify `upstream/app/` directly - all changes must be patches.
