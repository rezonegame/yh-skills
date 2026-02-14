---
name: boardgame-components
description: Board game components design including tokens, markers, player aids, rulebooks, score pads, and reference cards. Covers size standards, icon systems, and production specifications for non-card, non-tile, non-board components.
version: 1.0.0
parent: print-design
tags: [boardgame, components, tokens, rulebooks, player-aids, print-design]
triggers:
  - "设计游戏标记"
  - "规则书排版"
  - "玩家辅助卡设计"
  - "记分板设计"
  - "游戏配件制作"
---

# Board Game Components Design

Complete guide to designing and producing board game components including tokens, markers, player aids, rulebooks, score pads, and reference materials.

## Component Categories (配件分类)

### Component Types

| Category | Items | Viewing Distance | Complexity |
|----------|-------|------------------|------------|
| **Tokens** | Resource tokens, coins, cubes | 30-60cm | Low-Medium |
| **Markers** | Player markers, action markers | 50-80cm | Low |
| **Player Aids** | Reference cards, mats | 30-50cm | Medium |
| **Rulebooks** | Game rules, guides | 25-35cm | High |
| **Score Pads** | Score sheets, tracking | 30-40cm | Medium |
| **Reference Cards** | Quick guides, summaries | 30-50cm | Medium |

### Production Priority

**Tier 1 (Essential):**
- Player markers
- Resource tokens
- Rulebook
- Basic player aids

**Tier 2 (Important):**
- Score pads
- Reference cards
- Action markers
- Custom tokens

**Tier 3 (Nice to Have):**
- Custom score trackers
- Advanced player mats
- Deluxe tokens
- Premium components

## Tokens and Markers (标记物)

### Standard Token Sizes

**Circular Tokens (圆形标记):**

| Size | Diameter | Thickness | Use Case | Visibility |
|------|-----------|-----------|----------|------------|
| **Small** | 15mm | 2mm | Resources, markers | Low |
| **Medium** | 22mm | 2mm | Standard tokens | Medium |
| **Large** | 30mm | 2-2.5mm | Important markers | High |
| **Extra Large** | 35-40mm | 2.5mm | Special tokens | Very High |

**Other Shapes:**

| Shape | Size (typical) | Thickness | Use Case |
|--------|----------------|-----------|----------|
| **Square** | 15-25mm | 2mm | Resource cubes |
| **Hexagon** | 20-30mm | 2mm | Custom tokens |
| **Custom** | Variable | 2mm | Unique shapes |

### Token Design

**Visual Hierarchy:**

```
Priority 1 (Identify type):
- Primary icon or symbol
- Dominant color
- Size: 40-60% of token

Priority 2 (Show value/amount):
- Number or quantity
- Secondary color
- Size: 20-30% of token

Priority 3 (Decoration):
- Border, texture
- Tertiary color
- Size: 10-20% of token
```

**Color Coding:**

| Token Type | Color Schemes | Contrast | Accessibility |
|------------|---------------|----------|---------------|
| **Resources** | Distinct colors | High | Add icons |
| **Players** | 4-6 distinct | Very High | Test color blind |
| **Actions** | Action-specific | Medium-High | Icon + color |
| **Markers** | Neutral | High | Shape variation |

**Icon Integration:**

```
Icon Sizing (at 22mm token):
- Primary icon: 12-15mm
- Secondary icon: 6-8mm
- Number: 4-6mm height
- Border: 1-2mm

Placement:
Center: Main icon or number
Edge: Secondary icons, values
Background: Texture, pattern
```

### Stackability Considerations

**Stackable Tokens:**

```
Requirements:
- Flat tops and bottoms
- Uniform thickness (±0.1mm)
- Rounded edges (prevents catching)
- Weight: Not too light

Design:
- Avoid protruding elements
- Keep graphics away from edges
- Test stacking 10-20 high
```

**Non-Stackable Tokens:**

```
Use: Unique markers, player pieces
Features:
- Taller or shaped tops
- 3D elements (meeple, figure)
- Easy to pick up
- Distinctive silhouette
```

### Player Markers

** meeple-Style Markers:**

```
Standard meeple:
- Height: 20-30mm
- Width: 15-20mm
- Thickness: 3-5mm
- Material: Wood or plastic

Custom figures:
- Height: 25-40mm
- Base: 20-30mm diameter
- Stable base required
- Material: Plastic or metal
```

**Standee Markers:**

```
Standee dimensions:
- Height: 30-50mm
- Width: 15-25mm
- Base: 20-30mm (plastic)
- Material: Cardstock + plastic base

Design:
- Character illustration
- Name or number at base
- Distinct silhouette
- Player color on base
```

## Player Aids (玩家辅助)

### Reference Cards

**Standard Sizes:**

| Card Type | Dimensions | Use Case | Content |
|-----------|------------|----------|---------|
| **Small** | A6 (105×148mm) | Quick reference | 5-7 key points |
| **Standard** | A5 (148×210mm) | Player aids | 8-12 key points |
| **Large** | A4 (210×297mm) | Complex reference | 15+ key points |

**Layout Structure:**

```
┌─────────────────────────┐
│  [Title/Header]         │  ← Game/phase name
├─────────────────────────┤
│  Section 1:             │
│  • Point 1              │
│  • Point 2              │
│  • Point 3              │
├─────────────────────────┤
│  Section 2:             │
│  • Point 1              │
│  • Point 2              │
├─────────────────────────┤
│  Section 3:             │
│  • Point 1              │
│  • Point 2              │
└─────────────────────────┘

Spacing:
- Sections: 10-15mm apart
- Points: 5-8mm apart
- Margins: 10-15mm
```

**Information Hierarchy:**

```
Level 1 (Most Important):
- Section headers (14-18pt)
- Key actions (icons + text)
- Critical values (numbers)

Level 2 (Important):
- Explanations (10-12pt)
- Examples (8-10pt)
- Secondary info

Level 3 (Supporting):
- Flavor text (8-9pt)
- Notes (8pt)
- Reminders
```

### Player Mats

**Mat vs Reference Card:**

| Characteristic | Player Mat | Reference Card |
|----------------|------------|----------------|
| **Thickness** | 2-3mm | 0.3mm (cardstock) |
| **Durability** | High | Medium |
| **Components** | Can hold pieces | Information only |
| **Size** | A5-A4 | A6-A5 |
| **Cost** | Higher | Lower |

**Player Mat Layout:**

```
┌─────────────────────────┐
│  [Player Name/Color]     │
├─────────────────────────┤
│  Resources:              │
│  [Resource Track 1]      │  ← Token slots
│  [Resource Track 2]      │
│  [Resource Track 3]      │
├─────────────────────────┤
│  Actions:               │
│  [Action 1] [Action 2]   │  ← Action spaces
│  [Action 3] [Action 4]   │
├─────────────────────────┤
│  Buildings/Upgrades:     │
│  ☐ ☐ ☐ ☐ ☐ ☐           │  ← Check boxes
├─────────────────────────┤
│  Score Track:            │
│  0 ──●── 10 ─── 20      │  ← Linear track
└─────────────────────────┘

Design Principles:
- Clear sections
- Logical flow
- Visual hierarchy
- Component fit
```

**Token Slots on Mats:**

```
Slot Design:
┌─────┐  ← Outline or background
│ ⊕   │  ← Placeholder icon
│     │  ← Token placement area
└─────┘

Specs:
- Size: Token diameter + 3mm
- Outline: Subtle (1-2pt line)
- Label: Small text or icon
- Color: Neutral or player color
```

## Rulebooks (规则书)

### Rulebook Structure

**Standard Rulebook Sections:**

```
1. Cover
   • Game title
   • Tagline/summary
   • Player count
   • Duration
   • Age recommendation

2. Table of Contents
   • Section list with page numbers
   • Visual hierarchy

3. Setup
   • Component list
   • Board setup diagram
   • Initial arrangement
   • Ready-to-play photo

4. Overview
   • Objective
   • How to win
   • Game concept

5. Components
   • List and photos
   • Component descriptions

6. Gameplay
   • Turn structure
   • Actions available
   • Rules explanations
   • Examples

7. Special Rules
   • Advanced concepts
   • Edge cases
   • Clarifications

8. Game End
   • Winning conditions
   • Scoring
   • Tie-breakers

9. Variants
   • Alternative rules
   • Player counts
   • Difficulty levels

10. Credits/Appendix
    • Designer credits
    • FAQ
    • Index (optional)
```

### Rulebook Layout

**Page Specifications:**

| Rulebook Size | Page Size | Margins | Columns | Body Text |
|---------------|-----------|---------|---------|-----------|
| **Small** | A5 (148×210mm) | 12-15mm | 1 | 9-10pt |
| **Standard** | A5 (148×210mm) | 12-15mm | 2 | 9-10pt |
| **Large** | A4 (210×297mm) | 15-20mm | 2 | 10-11pt |

**Typography:**

```
Hierarchy:
- Title: 24-36pt
- Chapter headers: 18-24pt
- Section headers: 14-18pt
- Body text: 9-11pt
- Captions/notes: 8-9pt
- Page numbers: 8-9pt

Leading:
- Body: 12-14pt (1.3-1.4 × font)
- Headers: 1.2 × font
- Captions: 10-12pt
```

**Layout Grid:**

```
2-Column Layout (A5):
┌────┬────┐
│    │    │  ← Column width: ~60mm
│    │    │  ← Gutter: 4-6mm
│    │    │  ← Margins: 12-15mm
└────┴────┘

Content flow:
- Top to bottom
- Left to right
- Cross columns sparingly
- Visual breaks between sections
```

### Diagrams and Examples

**Diagram Standards:**

```
Visual Elements:
- Component photos: Actual size or larger
- Setup diagrams: Clear overhead view
- Action examples: Sequential panels
- Icons: Consistent with game

Sizing:
- Full-width: 120-140mm (A5)
- Half-width: 55-65mm
- Spot illustrations: 30-50mm

Captions:
- Size: 8-9pt
- Placement: Below image
- Style: Italic or different color
```

**Example Boxes:**

```
┌─────────────────────────┐
│ Example: Trading        │  ← Header
├─────────────────────────┤
│ Player A gives 1 wood   │
│ to Player B in exchange │
│ for 2 sheep.            │
└─────────────────────────┘

Specs:
- Border: 1-2pt line
- Background: Light tint
- Padding: 3-5mm
- Header: Bold, distinct color
```

### Rulebook Production

**Page Count Guidelines:**

| Game Complexity | Pages | Binding |
|-----------------|-------|---------|
| **Simple** | 8-16 | Saddle stitch |
| **Moderate** | 16-32 | Saddle stitch |
| **Complex** | 32-64 | Perfect bound |
| **Very Complex** | 64-100+ | Perfect bound |

**Paper Selection:**

| Element | Stock | Weight | Finish |
|---------|-------|--------|--------|
| **Cover** | Cardstock | 250-300gsm | Matte/Gloss |
| **Interior** | Book paper | 100-130gsm | Uncoated/Matte |
| **Insert** | Newsprint | 80-100gsm | Uncoated |

**Binding Options:**

| Binding Type | Page Range | Lay Flat | Durability | Cost |
|--------------|------------|----------|------------|------|
| **Saddle stitch** | 8-48 | No | Medium | Low |
| **Spiral/Coil** | 8-100 | Yes | High | Medium |
| **Perfect bound** | 48-200 | Partially | High | Medium-High |
| **Hardcover** | 32-200 | No | Very High | High |

## Score Pads (记分板)

### Score Pad Design

**Standard Formats:**

| Format | Size | Sheets | Use Case |
|--------|------|--------|----------|
| **Small** | A6 | 50-100 | Short games |
| **Standard** | A5 | 50-100 | Most games |
| **Large** | A4 | 30-50 | Complex scoring |

**Layout Structure:**

```
Score Sheet Example:
┌─────────────────────────┐
│  Game Title             │
│  Player: ___________     │
├─────────────────────────┤
│  Round 1:  [    ]       │  ← Entry boxes
│  Round 2:  [    ]       │
│  Round 3:  [    ]       │
│  Round 4:  [    ]       │
├─────────────────────────┤
│  Bonuses:               │
│  ☐ Bonus A:  [    ]     │
│  ☐ Bonus B:  [    ]     │
├─────────────────────────┤
│  TOTAL:     [    ]       │
└─────────────────────────┘

Box sizing:
- Entry boxes: 15-20mm wide
- Height: 8-10mm
- Lines: Bottom border
- Spacing: 3-5mm between
```

### Score Track Alternatives

**Printed Track:**

```
Advantages:
- Reusable
- No writing needed
- Component-based

Disadvantages:
- Limited players
- Board space needed
- Can be lost
```

**Score Pad:**

```
Advantages:
- Unlimited players
- Permanent record
- Detailed tracking
- Cheap

Disadvantages:
- Single-use
- Need pens
- Paper waste
```

**App/Sheet:**

```
Advantages:
- Reusable
- Auto-calculation
- Permanent record

Disadvantages:
- Requires device
- Setup time
- Cost
```

## Production Specifications (制作规范)

### Material Selection

**Tokens/Markers:**

| Material | Thickness | Durability | Cost | Best For |
|----------|-----------|------------|------|----------|
| **Chipboard** | 1.5-2mm | Good | Low | Standard tokens |
| **Grayboard** | 2mm | Very Good | Low-Medium | Premium tokens |
| **Wood** | 3mm | Excellent | Medium | Deluxe editions |
| **Plastic** | 2-3mm | Excellent | Medium-High | High volume |
| **Acrylic** | 3mm | Extreme | High | Premium/luxury |

**Player Aids/Cards:**

| Material | Thickness | Durability | Cost | Best For |
|----------|-----------|------------|------|----------|
| **Cardstock** | 300gsm | Fair | Low | Player aids |
| **Cardstock + core** | 350-400gsm | Good | Medium | Player mats |
| **Mounted** | 2mm | Very Good | Medium-High | Premium mats |

### Die-Cutting

**Token Die-Cutting:**

```
Specifications:
- Tolerance: ±0.3mm
- Spacing: 2-3mm between tokens
- Bleed: 2-3mm beyond cut
- Registration: ±0.5mm

Sheet Layout (A4):
- 15mm tokens: ~60-80 per sheet
- 22mm tokens: ~35-45 per sheet
- 30mm tokens: ~20-25 per sheet
```

**Custom Shapes:**

```
Considerations:
- Minimum detail: 1mm
- Minimum bridge: 2mm
- Corner radius: 1-2mm
- Test cut required
- Higher tooling cost
```

### Printing Specifications

**Resolution:**
- 300 DPI @ final size
- Vector preferred for text and icons
- Raster: 300 DPI minimum

**Color:**
- CMYK mode
- Color profile: FOGRA39/51
- Test color accuracy for tokens

**File Formats:**
- Tokens/Markers: PDF/X-4 with die lines
- Player aids: PDF/X-4
- Rulebooks: PDF/X-4 with spreads

## Quick Reference Cards (快速参考卡)

### Card Types

**Summary Cards:**

```
┌─────────────────────────┐
│  GAME TITLE             │
├─────────────────────────┤
│  Turn Structure:         │
│  1. Action phase         │
│  2. Buy phase            │
│  3. Cleanup phase        │
├─────────────────────────┤
│  Scoring:                │
│  • Buildings: 2pts       │
│  • Roads: 1pt           │
│  • Bonus: 3pts           │
└─────────────────────────┘

Use: Quick reminders
Size: A6 or poker card
Content: 5-7 key points
```

**Turn Reference Cards:**

```
┌─────────────────────────┐
│  ACTIONS (On Your Turn) │
├─────────────────────────┤
│  ⚔️  Attack      Cost: 2 │
│  🛡️  Defend      Cost: 1 │
│  💰  Trade       Cost: 1 │
│  🏗️  Build       Cost: 3 │
├─────────────────────────┤
│  Draw 2 cards at end     │
└─────────────────────────┘

Use: Action reference
Size: A6 or half-A5
Content: Action list with costs
```

**Phase Cards:**

```
Front:
┌─────────────────────────┐
│        PHASE 1           │
│     Setup Phase          │
│                          │
│     [Icon or Art]        │
└─────────────────────────┘

Back:
┌─────────────────────────┐
│  • Draw starting hand    │
│  • Place initial tokens  │
│  • Determine start player│
└─────────────────────────┘

Use: Phase reminders
Size: A6 or poker card
Content: Phase-specific rules
```

## Component Integration (组件集成)

### Storage Solutions

**Token Storage:**

```
Box Trays:
┌─────────────────────────┐
│  [Token Tray]            │
│  ════════════════       │
│                         │
└─────────────────────────┘

- Depth: 10-15mm
- Compartments: By token type
- Labels: Clear identification
- Lid: Prevents spilling

Bags:
- Ziplock bags
- Drawstring bags
- Labeled by type
- Cheap, effective

Inserts:
- Custom cutouts
- Organized storage
- Premium feel
- Higher cost
```

### Rulebook Integration

**Component Checklist:**

```
Include in rulebook:
- Component list with photos
- Quantity per player
- Setup diagram with all components
- Storage guide
- Component descriptions

Visual aids:
- Actual-size photos
- Scale comparisons
- Quantity indicators
```

## Accessibility Considerations

### Color Blindness

**Token Color Coding:**

```
Safe Combinations:
- Red vs Blue
- Yellow vs Purple
- Orange vs Green (add icons)
- Black vs White

Always include:
- Icons or shapes
- Text labels
- Pattern or texture
- Multiple identification cues
```

### Readability

**Font Choices:**
- Sans-serif for body text
- High contrast colors
- Adequate size (9pt minimum)
- Clear hierarchy

**Icon Design:**
- Simple, recognizable
- Consistent style
- Color blind safe
- Text labels when needed

## Quality Control

### Pre-Production Checklist

**Tokens/Markers:**
- [ ] Size confirmed (15-40mm)
- [ ] Thickness specified (2mm standard)
- [ ] Material selected
- [ ] Die line created
- [ ] Color proof tested
- [ ] Stackability tested
- [ ] Color blind tested

**Player Aids:**
- [ ] Size finalized (A6-A5)
- [ ] Content complete
- [ ] Hierarchy clear
- [ ] Icons consistent
- [ ] Proofread
- [ ] Playtested

**Rulebooks:**
- [ ] Page count confirmed
- [ ] Binding selected
- [ ] Layout complete
- [ ] Diagrams clear
- [ ] Examples accurate
- [ ] Proofread
- [ ] Indexed (if needed)

**Score Pads:**
- [ ] Format selected (A5-A6)
- [ ] Entry boxes sized
- [ ] Calculation tested
- [ ] Clear instructions
- [ ] Proofread

## Common Mistakes

| Component | Mistake | Solution |
|-----------|---------|----------|
| **Tokens** | Poor color coding | Add icons, test color blind |
| **Markers** | Too similar | Distinct shapes + colors |
| **Player aids** | Too much text | Edit ruthlessly, use icons |
| **Rulebooks** | Poor organization | Clear sections, TOC, index |
| **Score pads** | Insufficient space | Test with real gameplay |
| **Reference cards** | Inconsistent with game | Sync with final design |

## Quick Reference

### Token Sizes
- Small: 15mm diameter
- Medium: 22mm diameter (standard)
- Large: 30mm diameter

### Player Aid Sizes
- Quick reference: A6 (105×148mm)
- Standard aid: A5 (148×210mm)
- Large reference: A4 (210×297mm)

### Rulebook Specs
- Standard size: A5 (148×210mm)
- Page count: 16-32 pages
- Binding: Saddle stitch or perfect bound
- Interior stock: 100-130gsm

### Material Recommendations
- Tokens: 2mm grayboard
- Player aids: 300gsm cardstock
- Player mats: 2mm mounted board
- Rulebooks: 100-130gsm interior

## Case Studies

### Catan Reference Cards
- Size: A6 folded
- Content: Building costs, turn summary
- Style: Simple, icon-heavy
- Success: Clear, quick reference

### Ticket to Ride Scoring
- Format: Score pad
- Size: A5
- Content: Route scoring table
- Success: Organized, clear math

### Pandemic Player Cards
- Size: A6
- Content: Role abilities
- Style: Icon-based, minimal text
- Success: Quick role reference

## References

- **Parent skill**: print-design
- **Related skills**: boardgame-cards, boardgame-tiles, boardgame-boards
- **References**: `print-design/references/boardgame-specs.md`
- **Production specs**: `print-design/references/print-specs.md`

---

**Version**: 1.0.0
**Last Updated**: 2025-01-23
**Default Token Size**: 22mm diameter (unless otherwise specified)
