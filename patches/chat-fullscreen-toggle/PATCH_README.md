# Chat Expand/Collapse Feature - Patch-Based Implementation

## 🎯 Repository Model

This repository is a **downstream derivative** that uses a **vendor + patch model**:
- Upstream code lives in `upstream/app/` (read-only)
- All customizations are `.patch` files in `patches/`
- Never modify `upstream/app/` directly

## 📦 What's Included

### Patch Files (Apply These)
1. **001-add-chat-expand-chatcolumn.patch** - ChatColumn component changes
2. **002-add-chat-expand-page.patch** - Notebook page layout changes
3. **003-add-chat-expand-chatpanel.patch** - ChatPanel button UI changes
4. **004-add-chat-expand-sources-page.patch** - Sources page layout changes

### Documentation
4. **PATCH_IMPLEMENTATION_GUIDE.md** - Detailed implementation steps
5. **VISUAL_GUIDE.md** - Visual diagrams of the feature
6. **KEY_CHANGES.md** - Code-level summary

### Reference Files (For Comparison Only)
7. **ChatColumn.tsx** - Final result after patches
8. **ChatPanel.tsx** - Final result after patches
9. **page.tsx** - Final result after patches

## ⚡ Quick Start

```bash
# 1. Create feature directory and copy patches
mkdir -p /path/to/your-repo/patches/chat-fullscreen-toggle
cp 00*.patch /path/to/your-repo/patches/chat-fullscreen-toggle/

# 2. Apply patches
cd /path/to/your-repo
git apply patches/chat-fullscreen-toggle/001-add-chat-expand-chatcolumn.patch
git apply patches/chat-fullscreen-toggle/002-add-chat-expand-page.patch
git apply patches/chat-fullscreen-toggle/003-add-chat-expand-chatpanel.patch
git apply patches/chat-fullscreen-toggle/004-add-chat-expand-sources-page.patch

# 3. Commit changes
git add .
git commit -m "feat: Add chat expand/collapse functionality"

# 4. Test
cd frontend && npm run dev
```

## 🔍 What This Does

### Notebook Page (/notebooks/[id])

**Before (Cramped):**
```
┌─────────┬─────────┬─────────┐
│ Sources │  Notes  │  Chat   │  ← Chat is 33% width
└─────────┴─────────┴─────────┘
```

**After (Expanded):**
```
┌───────────────────────────────┐
│           Chat                │  ← Chat is 100% width
│      (Full Screen)            │
└───────────────────────────────┘
```

### Sources Page (/sources/[id])

**Before (Cramped):**
```
┌─────────────────┬─────────┐
│ Source Detail   │  Chat   │  ← Chat is 33% width
│    (66%)        │ (33%)   │
└─────────────────┴─────────┘
```

**After (Expanded):**
```
┌───────────────────────────────┐
│           Chat                │  ← Chat is 100% width
│      (Full Screen)            │
└───────────────────────────────┘
```

### Features
✅ Click "Expand" button to maximize chat
✅ Sources and Notes columns hide automatically (notebook page)
✅ Source detail column hides automatically (sources page)
✅ Click "Collapse" to restore original layout
✅ Chat history preserved during toggle
✅ Zero breaking changes  

## 📋 Files Modified by Patches

```
frontend/src/
├── app/(dashboard)/
│   ├── notebooks/
│   │   ├── [id]/
│   │   │   └── page.tsx                ← Patch 002 (Notebook page)
│   │   └── components/
│   │       └── ChatColumn.tsx          ← Patch 001
│   └── sources/
│       └── [id]/
│           └── page.tsx                ← Patch 004 (Sources page)
└── components/source/
    └── ChatPanel.tsx                   ← Patch 003
```

**Patch Directory Structure:**
```
patches/
└── chat-fullscreen-toggle/
    ├── 001-add-chat-expand-chatcolumn.patch
    ├── 002-add-chat-expand-page.patch
    ├── 003-add-chat-expand-chatpanel.patch
    └── 004-add-chat-expand-sources-page.patch
```

## 🔄 Why Patches?

This repository maintains:
- **Clean separation** from upstream
- **Easy upstream updates** (patches reapply automatically)
- **Version control** for customizations
- **Conflict detection** when upstream changes

Following the workflow in **AI.md**:
> "Never modify vendor (upstream) code directly... All local changes must be made as patches"

## 📊 Patch Statistics

| Patch | File | Lines Changed | Risk Level |
|-------|------|---------------|------------|
| 001 | ChatColumn.tsx | +5 | Low |
| 002 | notebooks/[id]/page.tsx | +20 | Low |
| 003 | ChatPanel.tsx | +30 | Low |
| 004 | sources/[id]/page.tsx | +18 | Low |
| **Total** | **4 files** | **~73 lines** | **Low** |

## 🧪 Verification

After applying patches, verify:

```bash
# Check files were modified
git status

# Should show:
# modified: frontend/src/app/(dashboard)/notebooks/components/ChatColumn.tsx
# modified: frontend/src/app/(dashboard)/notebooks/[id]/page.tsx
# modified: frontend/src/components/source/ChatPanel.tsx
# modified: frontend/src/app/(dashboard)/sources/[id]/page.tsx

# Run TypeScript check
cd frontend && npm run type-check

# Start dev server
npm run dev
```

## 🛠️ Maintenance

### When Upstream Updates

The patches will automatically reapply via `tools/update_upstream.sh`:

```bash
./tools/update_upstream.sh
# Script will:
# 1. Update vendor copy from upstream
# 2. Reapply all patches (including these)
# 3. Report any conflicts
```

### If Patches Conflict

Regenerate the patch:

```bash
# Edit the file manually
vim upstream/app/frontend/src/.../ChatColumn.tsx

# Generate new patch
git diff > patches/chat-fullscreen-toggle/001-add-chat-expand-chatcolumn.patch
```

## 📝 Implementation Priorities

Follow this order:

1. ✅ **Read** PATCH_IMPLEMENTATION_GUIDE.md
2. ✅ **Backup** existing patches directory
3. ✅ **Copy** four .patch files to `patches/`
4. ✅ **Apply** patches in order (001, 002, 003, 004)
5. ✅ **Commit** changes to your repository
6. ✅ **Test** in browser (both /notebooks/[id] and /sources/[id] pages)
7. ✅ **Document** in your changelog

## 🎯 Success Criteria

✅ Feature directory `patches/chat-fullscreen-toggle/` created
✅ All four patches in feature directory
✅ Patches apply without conflicts
✅ TypeScript compiles successfully
✅ Feature works in browser on /notebooks/[id] page
✅ Feature works in browser on /sources/[id] page
✅ No breaking changes
✅ Ready for next upstream update  

## 📚 Key Documents

- **AI.md** - Repository workflow (vendor + patch model)
- **AI_TS.md** - TypeScript coding standards
- **tools/update_upstream.sh** - Automated patch application

## 🆘 Need Help?

1. Check **PATCH_IMPLEMENTATION_GUIDE.md** for detailed steps
2. Review **VISUAL_GUIDE.md** for UI mockups
3. See **KEY_CHANGES.md** for code-level details
4. Compare with reference .tsx files if needed

## 🎉 Result

Once implemented, you'll have:
- Comfortable full-width chat experience
- Easy toggle between layouts
- Clean patch-based customization
- Ready for upstream updates

**Total implementation time: ~5-10 minutes** ⚡

---

**Important**: Always follow the patch-based workflow defined in AI.md. Never edit `upstream/app/` directly!
