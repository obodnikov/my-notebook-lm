# Visual Guide: Full-Screen Chat Toggle

## 🎨 User Interface Changes

### Header Button Location
```
┌─────────────────────────────────────────────────────┐
│ 🤖 Chat with Notebook    [⛶ Expand] [🕐 Sessions]  │ ← New button here!
├─────────────────────────────────────────────────────┤
│                                                     │
│  Chat messages appear here...                       │
│                                                     │
```

### Button States

**Collapsed State (Default):**
```
┌──────────────┐
│ ⛶  Expand    │ ← Click to maximize
└──────────────┘
```

**Expanded State:**
```
┌──────────────┐
│ ⊡  Collapse  │ ← Click to restore
└──────────────┘
```

## 📐 Layout Transformation

### Before Expansion (3 Columns)
```
┌──────────────────────────────────────────────────────────────┐
│                       Notebook Page                          │
├───────────────┬───────────────┬──────────────────────────────┤
│               │               │                              │
│   Sources     │     Notes     │      Chat with Notebook      │
│               │               │  ┌────────────────────────┐  │
│  ┌─────────┐  │  ┌─────────┐  │  │ 🤖 Chat  [⛶][🕐]       │  │
│  │Source 1 │  │  │ Note 1  │  │  ├────────────────────────┤  │
│  └─────────┘  │  └─────────┘  │  │                        │  │
│               │               │  │  Messages here...      │  │
│  ┌─────────┐  │  ┌─────────┐  │  │                        │  │
│  │Source 2 │  │  │ Note 2  │  │  └────────────────────────┘  │
│  └─────────┘  │  └─────────┘  │                              │
│               │               │                              │
└───────────────┴───────────────┴──────────────────────────────┘
```

### After Expansion (1 Column)
```
┌──────────────────────────────────────────────────────────────┐
│                       Notebook Page                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│               Chat with Notebook (Full Width)                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ 🤖 Chat with Notebook            [⊡ Collapse] [🕐]     │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │                                                        │  │
│  │  Bot: Hello! How can I help?                           │  │
│  │                                                        │  │
│  │                         You: Tell me about my sources  │  │
│  │                                                        │  │
│  │  Bot: You have 2 sources...                            │  │
│  │                                                        │  │
│  │                                                        │  │
│  │  More comfortable reading space here!                  │  │
│  │                                                        │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 🔄 State Flow Diagram

```
                   ┌─────────────────┐
                   │   Page Loads    │
                   │ (Default State) │
                   └────────┬────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │  isChatExpanded = false │
              │                         │
              │  ✓ Sources visible      │
              │  ✓ Notes visible        │
              │  ✓ Chat visible (1/3)   │
              └──────────┬──────────────┘
                         │
          User clicks    │    User clicks
           "Expand"      │     "Collapse"
                    ▼    │    ▲
        ┌────────────────┴────┴─────────────┐
        │   isChatExpanded = true           │
        │                                   │
        │   ✗ Sources hidden                │
        │   ✗ Notes hidden                  │
        │   ✓ Chat visible (full width)     │
        └───────────────────────────────────┘
```

## 💻 Code Flow

```
User clicks "Expand" button
         │
         ▼
onToggleExpand() called in ChatPanel
         │
         ▼
handleToggleChatExpand() in page.tsx
         │
         ▼
setIsChatExpanded(true)
         │
         ▼
React re-renders with new state
         │
         ├─► Grid class changes to 'grid-cols-1'
         │
         ├─► {!isChatExpanded && ...} hides Sources/Notes
         │
         └─► Chat panel expands to full width
```

## 📱 Responsive Behavior

### Desktop (lg breakpoint and up)
```
Collapsed: [Sources] [Notes] [Chat]  (3 columns)
Expanded:  [        Chat        ]     (1 column)
```

### Tablet (md to lg breakpoint)
```
Collapsed: [Sources] [Notes]  (2 columns on one row)
           [      Chat      ]  (1 column on second row)

Expanded:  [      Chat      ]  (1 column full width)
```

### Mobile (below md breakpoint)
```
Collapsed: [   Sources   ]  (1 column, stacked)
           [    Notes     ]  (1 column, stacked)
           [     Chat     ]  (1 column, stacked)

Expanded:  [     Chat     ]  (1 column full width)
```

## 🎯 Click Targets

The expand/collapse button has good accessibility:
- Minimum size: 40x40px (touch-friendly)
- Hover state: Background color change
- Title attribute: Shows "Expand chat" or "Collapse chat"
- Keyboard accessible: Can be tabbed to and activated with Enter/Space

## 🎨 Icon Meanings

- **⛶ (Maximize2)**: Expand to full screen
- **⊡ (Minimize2)**: Collapse/minimize to original size
- **🕐 (Clock)**: Sessions management (unchanged)
- **🤖 (Bot)**: Chat indicator (unchanged)

## 📊 State Comparison

| Feature | Collapsed (Default) | Expanded |
|---------|---------------------|----------|
| Sources visible | ✅ Yes | ❌ No |
| Notes visible | ✅ Yes | ❌ No |
| Chat visible | ✅ Yes (33% width) | ✅ Yes (100% width) |
| Button icon | ⛶ Maximize | ⊡ Minimize |
| Button text | "Expand" | "Collapse" |
| Grid columns | 3 (lg screens) | 1 |
| Reading comfort | Good | Excellent |
| Typing space | Limited | Spacious |

## 🚀 Performance Notes

- **No re-fetching**: Sources and notes remain in memory when hidden
- **Fast toggle**: Pure CSS show/hide, no data loading
- **Preserved state**: Chat history, context selections, and session data remain intact
- **Smooth experience**: Instant visual feedback on button click
