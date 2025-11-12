# Sources Page Chat Expand/Collapse Implementation

## 📋 Overview

This document describes the implementation of the chat expand/collapse feature for the **Sources Page** (`/sources/[id]`), extending the existing feature that was initially implemented for the Notebook Page.

**Created**: 2025-11-12
**Patch File**: `004-add-chat-expand-sources-page.patch`
**Status**: ✅ Ready for Application

---

## 🎯 Purpose

The Sources Page displays source detail content alongside a chat interface in a 2-column layout (66% / 33%). This implementation allows users to temporarily expand the chat to full width for a more comfortable conversation experience, then collapse back to the original layout.

### User Benefits

- **Better Readability**: Full-width chat provides more space for reading long AI responses
- **Easier Typing**: More room for composing detailed questions and prompts
- **Focused Interaction**: Temporarily hide the source detail to focus on the conversation
- **Quick Toggle**: Instant switch between layouts with one click
- **Preserved Context**: All chat history and state remains intact during toggle

---

## 🏗️ Technical Architecture

### Component Hierarchy

```
SourceDetailPage (sources/[id]/page.tsx)
  ├── State: isChatExpanded (boolean)
  ├── Handler: handleToggleChatExpand()
  │
  ├── SourceDetailContent (conditionally rendered)
  │   └── Hidden when isChatExpanded = true
  │
  └── ChatPanel
      ├── Props: isExpanded, onToggleExpand
      └── UI: Expand/Collapse button
```

### State Management

**Location**: `sources/[id]/page.tsx`

```typescript
const [isChatExpanded, setIsChatExpanded] = useState(false)

const handleToggleChatExpand = () => {
  setIsChatExpanded(prev => !prev)
}
```

**Initial State**: `false` (collapsed, 2-column layout)

### Layout Logic

The grid layout dynamically changes based on `isChatExpanded`:

- **Collapsed** (`isChatExpanded = false`):
  - Grid: `lg:grid-cols-[2fr_1fr]` (66% / 33%)
  - Source Detail: Visible
  - Chat: Visible (33% width)

- **Expanded** (`isChatExpanded = true`):
  - Grid: `grid-cols-1` (100%)
  - Source Detail: Hidden
  - Chat: Visible (100% width)

---

## 📝 Implementation Details

### Changes Made

#### 1. Import Addition
```typescript
import { useCallback, useState } from 'react'  // Added useState
```

#### 2. State Declaration
```typescript
// Chat expansion state
const [isChatExpanded, setIsChatExpanded] = useState(false)
```

#### 3. Toggle Handler
```typescript
// Handler to toggle chat expansion
const handleToggleChatExpand = () => {
  setIsChatExpanded(prev => !prev)
}
```

#### 4. Conditional Grid Class
```typescript
// Before:
<div className="flex-1 grid gap-6 lg:grid-cols-[2fr_1fr] overflow-hidden px-6">

// After:
<div className={`flex-1 grid gap-6 overflow-hidden px-6 ${isChatExpanded ? 'grid-cols-1' : 'lg:grid-cols-[2fr_1fr]'}`}>
```

#### 5. Conditional Source Detail Rendering
```typescript
// Wrapped in conditional:
{!isChatExpanded && (
  <div className="overflow-y-auto px-4 pb-6">
    <SourceDetailContent ... />
  </div>
)}
```

#### 6. Props Passed to ChatPanel
```typescript
<ChatPanel
  // ... existing props ...
  isExpanded={isChatExpanded}
  onToggleExpand={handleToggleChatExpand}
/>
```

---

## 🔗 Integration with Existing Code

### ChatPanel Component

The `ChatPanel` component already supports the `isExpanded` and `onToggleExpand` props (added in patch 003). No changes to `ChatPanel.tsx` are needed for the sources page - we simply pass the props.

**Existing ChatPanel Props Interface** (from patch 003):
```typescript
interface ChatPanelProps {
  // ... other props ...
  isExpanded?: boolean
  onToggleExpand?: () => void
}
```

The button UI is automatically available and functional once these props are provided.

---

## 🎨 User Experience

### Visual Changes

1. **Button Location**: Top-right of chat header, left of "Sessions" button
2. **Button States**:
   - Collapsed: "⛶ Expand" (Maximize2 icon)
   - Expanded: "⊡ Collapse" (Minimize2 icon)
3. **Layout Transition**: Instant (CSS-based, no animation)

### User Flow

```
1. User navigates to /sources/[id]
   → Sees source detail (66%) and chat (33%)

2. User clicks "Expand" button
   → Source detail hides
   → Chat expands to 100% width
   → Button changes to "Collapse"

3. User has conversation in full-width chat
   → Comfortable reading and typing space

4. User clicks "Collapse" button
   → Source detail reappears
   → Chat returns to 33% width
   → Button changes to "Expand"
   → Chat history is preserved
```

---

## 🧪 Testing Requirements

### Functional Testing

- [ ] Expand button appears in chat header
- [ ] Click "Expand" → Source detail hides, chat expands
- [ ] Click "Collapse" → Source detail appears, chat shrinks
- [ ] Chat messages preserved during toggle
- [ ] Session management still works
- [ ] Model selection still works
- [ ] Message sending works in both states

### Responsive Testing

- [ ] **Desktop** (≥1024px): 2-column → 1-column transition works
- [ ] **Tablet** (768-1024px): Layout behaves correctly
- [ ] **Mobile** (<768px): Feature works on small screens

### Integration Testing

- [ ] No conflicts with existing source detail functionality
- [ ] Navigation (back button) works correctly
- [ ] URL navigation preserves state correctly
- [ ] Multiple source pages work independently

---

## 🔍 Patch Details

**File**: `004-add-chat-expand-sources-page.patch`

**Target File**: `upstream/app/frontend/src/app/(dashboard)/sources/[id]/page.tsx`

**Statistics**:
- Lines changed: ~18
- Additions: ~15
- Deletions: ~3
- Risk level: Low
- Dependencies: ChatPanel props (already available from patch 003)

**Conflicts**:
- **Low risk** - Only modifies one page component
- Possible conflict if upstream significantly restructures the sources page layout

---

## 🚀 Deployment

### Prerequisites

Patches 001, 002, and 003 must be applied first (for ChatPanel button support).

### Application Command

```bash
git apply patches/chat-fullscreen-toggle/004-add-chat-expand-sources-page.patch
```

### Verification

```bash
# Check file was modified
git status | grep "sources/\[id\]/page.tsx"

# Run TypeScript check
cd frontend && npm run type-check

# Start dev server and test
npm run dev
# Navigate to any source: http://localhost:3000/sources/[id]
# Click "Expand" button in chat header
```

---

## 🔄 Comparison with Notebook Page

| Aspect | Notebook Page | Sources Page |
|--------|---------------|--------------|
| **Patch File** | 002 | 004 |
| **Layout Type** | 3-column | 2-column |
| **Columns Hidden** | Sources + Notes | Source Detail |
| **Grid Classes** | `grid-cols-1 lg:grid-cols-3` | `grid-cols-1 lg:grid-cols-[2fr_1fr]` |
| **Implementation Pattern** | Same | Same |
| **State Management** | Same | Same |
| **ChatPanel Integration** | Direct | Same (reuses patch 003) |

**Key Similarity**: Both implementations use identical state management patterns and rely on the same `ChatPanel` component button (patch 003).

**Key Difference**: Notebook page hides two separate columns (Sources + Notes), while sources page hides one column (Source Detail).

---

## 📚 Related Documentation

- **PATCH_README.md** - Overall feature documentation
- **PATCH_IMPLEMENTATION_GUIDE.md** - Step-by-step implementation guide
- **VISUAL_GUIDE.md** - Visual diagrams and UI mockups
- **AI.md** - Repository patch workflow
- **Patch 002** - Notebook page implementation (reference)
- **Patch 003** - ChatPanel button implementation (dependency)

---

## ✅ Success Criteria

- [x] Patch file created and tested
- [x] Documentation updated
- [x] Integration with ChatPanel verified
- [x] No breaking changes to existing functionality
- [x] TypeScript compilation passes
- [ ] Manual testing completed
- [ ] Applied to repository

---

## 🐛 Known Limitations

1. **State not persisted**: Expansion state resets on page refresh (by design - UX preference)
2. **No animation**: Transition is instant (CSS-based, could add transition if desired)
3. **Mobile UX**: On very small screens, expand/collapse may have limited value since both states are similar

---

## 🎉 Conclusion

This implementation successfully extends the chat expand/collapse feature to the Sources Page using the same proven pattern as the Notebook Page. The patch is minimal, low-risk, and provides immediate UX improvement for users interacting with source documents.

**Estimated Impact**:
- Development time: 30 minutes
- User benefit: High (improved chat readability)
- Maintenance cost: Low (follows existing patterns)
- Regression risk: Very low (isolated change)
