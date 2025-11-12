# TODO: Apply Sources Page Chat Expansion Patch

**Created**: 2025-11-12
**Status**: ⏳ Pending Application

---

## ✅ Prerequisites Checklist

Before applying patch 004, verify these patches are already applied:

- [ ] **Patch 001**: ChatColumn props
  ```bash
  grep "isExpanded.*onToggleExpand" upstream/app/frontend/src/app/\(dashboard\)/notebooks/components/ChatColumn.tsx
  ```
  Should show the props in the interface.

- [ ] **Patch 002**: Notebook page layout
  ```bash
  grep "isChatExpanded" upstream/app/frontend/src/app/\(dashboard\)/notebooks/\[id\]/page.tsx
  ```
  Should show the state variable.

- [ ] **Patch 003**: ChatPanel button
  ```bash
  grep "Maximize2.*Minimize2" upstream/app/frontend/src/components/source/ChatPanel.tsx
  ```
  Should show the icon imports.

---

## 📋 Application Steps

### Step 1: Verify Current State

```bash
# Check current git status
git status

# Verify you're on the correct branch
git branch --show-current
# Should show: chat-fullscreen-toggle
```

### Step 2: Apply Patch 004

```bash
# Navigate to repository root
cd /home/mike/src/my-notebook-lm

# Apply the sources page patch
git apply patches/chat-fullscreen-toggle/004-add-chat-expand-sources-page.patch

# Check for errors
echo $?
# Should output: 0 (success)
```

### Step 3: Verify Patch Applied

```bash
# Check git status
git status

# Should show:
# modified: upstream/app/frontend/src/app/(dashboard)/sources/[id]/page.tsx

# View the changes
git diff upstream/app/frontend/src/app/\(dashboard\)/sources/\[id\]/page.tsx | head -30
```

### Step 4: Build Check

```bash
# Run TypeScript type check
cd frontend
npm run type-check

# Should complete without errors
```

### Step 5: Manual Testing

```bash
# Start dev server
npm run dev

# In browser:
# 1. Navigate to http://localhost:3000
# 2. Open any source (click on a source from sources page)
# 3. You should see the source detail page with chat on the right
# 4. Look for "Expand" button in chat header (next to Sessions)
# 5. Click "Expand" - source detail should hide, chat expands
# 6. Click "Collapse" - source detail reappears
# 7. Verify chat messages are preserved
```

### Step 6: Commit Changes

```bash
# Stage the modified file
git add upstream/app/frontend/src/app/\(dashboard\)/sources/\[id\]/page.tsx

# Commit with descriptive message
git commit -m "feat: Add chat expand/collapse to sources page

- Implement chat expansion state management on sources page
- Hide source detail column when chat is expanded
- Integrate with existing ChatPanel expand button (patch 003)
- Mirror notebook page implementation pattern (patch 002)

Applied patch: 004-add-chat-expand-sources-page.patch
Feature: chat-fullscreen-toggle"

# Push changes
git push origin chat-fullscreen-toggle
```

---

## 🧪 Testing Checklist

### Functional Tests

- [ ] Expand button appears in chat header on sources page
- [ ] Clicking "Expand" hides source detail and expands chat to 100%
- [ ] Clicking "Collapse" shows source detail and shrinks chat to 33%
- [ ] Chat messages are preserved during expansion/collapse
- [ ] Sessions button still works
- [ ] Model selection still works
- [ ] Back button navigation works correctly

### Integration Tests

- [ ] Notebook page expand/collapse still works
- [ ] Sources page expand/collapse works independently
- [ ] No console errors in browser
- [ ] No TypeScript compilation errors

### Responsive Tests

- [ ] Desktop (≥1024px): Layout transitions correctly
- [ ] Tablet (768-1024px): Feature works on medium screens
- [ ] Mobile (<768px): Feature accessible on small screens

---

## 🐛 Troubleshooting

### Patch Fails to Apply

**Error**: "patch does not apply"

**Solution**:
```bash
# Check if file already has the changes
git diff upstream/app/frontend/src/app/\(dashboard\)/sources/\[id\]/page.tsx

# If changes are already there, the patch may have been applied
# If not, check if the file has been modified by other patches

# To regenerate the patch (if needed):
# 1. Manually edit the file with the changes from patch 004
# 2. Create new patch:
git diff upstream/app/frontend/src/app/\(dashboard\)/sources/\[id\]/page.tsx > patches/chat-fullscreen-toggle/004-add-chat-expand-sources-page-v2.patch
```

### TypeScript Errors

**Error**: Type errors after applying patch

**Solution**:
```bash
# Verify all dependencies are installed
cd frontend
npm install

# Clear build cache
rm -rf .next
npm run build

# Re-run type check
npm run type-check
```

### Feature Not Working

**Issue**: Button doesn't appear or doesn't work

**Solution**:
1. Verify patch 003 is applied (ChatPanel button implementation)
   ```bash
   grep "onToggleExpand" upstream/app/frontend/src/components/source/ChatPanel.tsx
   ```

2. Check browser console for JavaScript errors
3. Clear browser cache and hard refresh (Ctrl+Shift+R)
4. Restart dev server

---

## 📚 Reference Documentation

- **SOURCES_PAGE_EXTENSION_SUMMARY.md** - Complete overview
- **SOURCES_PAGE_IMPLEMENTATION.md** - Technical details
- **PATCH_IMPLEMENTATION_GUIDE.md** - Full implementation guide
- **VISUAL_GUIDE.md** - Visual diagrams and expected behavior

---

## ✅ Success Criteria

All of the following should be true:

- [ ] Patch applied without errors
- [ ] TypeScript compiles successfully
- [ ] Dev server starts without errors
- [ ] Feature works on sources page
- [ ] Feature works on notebook page (no regression)
- [ ] All tests pass
- [ ] Changes committed to git

---

## 🎉 Next Steps After Success

1. **Create Pull Request** (if using PR workflow)
   ```bash
   gh pr create --title "feat: Add chat expand/collapse to sources page" \
                --body "Extends chat-fullscreen-toggle feature to sources page. See patches/chat-fullscreen-toggle/SOURCES_PAGE_EXTENSION_SUMMARY.md"
   ```

2. **Update Changelog** (if applicable)
   ```markdown
   ## [Unreleased]
   ### Added
   - Chat expand/collapse button on sources page
   - Full-width chat mode for source conversations
   ```

3. **Deploy to Staging** (if applicable)
   ```bash
   # Follow your deployment process
   ```

4. **Monitor for Issues**
   - Check error logs
   - Monitor user feedback
   - Watch for console errors

---

**Status**: ⏳ Ready to apply
**Last Updated**: 2025-11-12
**Patch File**: `004-add-chat-expand-sources-page.patch`
