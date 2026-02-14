---
name: boardgame-boards
description: Game board and map design including layout systems, information density, folding patterns, path clarity, and print production for board game boards and player mats.
version: 1.0.0
parent: print-design
tags: [boardgame, boards, maps, print-design, game-components, player-mats]
triggers:
  - "设计游戏板"
  - "桌游地图设计"
  - "玩家垫板设计"
  - "游戏板折叠"
  - "路径和区域设计"
---

# Board Game Board Design

Complete guide to designing and producing game boards, maps, and player mats, from layout systems and folding patterns to information density and path clarity.

## Board Types and Standards (游戏板类型和标准)

### Standard Board Sizes

**Folded Board Dimensions:**

| Board Type | Folded | Unfolded | Panels | Play Area | Thickness |
|------------|--------|----------|--------|-----------|-----------|
| **Small** | A5 (148×210mm) | A4 (210×297mm) | 1 | 190×270mm | 2mm |
| **Standard** | A4 (210×297mm) | A3 (420×297mm) | 2 | 400×270mm | 2mm |
| **Large** | A3 (420×297mm) | A2 (594×420mm) | 2 | 570×390mm | 2.5mm |
| **Extra Large** | A2 (594×420mm) | A1 (841×594mm) | 2-4 | 800×550mm | 2.5-3mm |
| **Jumbo** | Custom | Custom | 4+ | Varies | 3mm |

**Panel Configurations:**

```
2-Panel Fold (A3 → A4):
┌─────────────┬─────────────┐
│   Panel 1   │   Panel 2   │  ← Unfolded (A3)
└─────────────┴─────────────┘
        ↓ fold
┌─────────────────────────┐
│      Folded (A4)        │
└─────────────────────────┘

4-Panel Fold (A2 → A3 → A4):
┌─────┬─────┬─────┬─────┐
│  1  │  2  │  3  │  4  │  ← Unfolded (A2)
└─────┴─────┴─────┴─────┘
    ↓ folds → folds ↓
┌─────────────┬─────────────┐
│     1+2     │     3+4     │  ← Folded once (A3)
└─────────────┴─────────────┘
        ↓ fold
┌─────────────────────────┐
│      All 4 panels       │  ← Folded twice (A4)
└─────────────────────────┘
```

### Player Mats (玩家垫板)

**Standard Mat Sizes:**

| Mat Type | Dimensions | Use Case | Thickness |
|----------|------------|----------|-----------|
| **Small** | A6 (105×148mm) | Reference cards, player aids | 1.5-2mm |
| **Standard** | A5 (148×210mm) | Individual player boards | 2mm |
| **Large** | A4 (210×297mm) | Complex player mats | 2-2.5mm |
| **Oversized** | Custom | Special mats | 2.5mm |

**Mat Functions:**
- Resource tracking
- Action reference
- Building placement
- Technology trees
- Score tracking

### Board vs Mats

| Characteristic | Game Board | Player Mats |
|----------------|------------|-------------|
| **Players** | Shared by all | Individual |
| **Viewing distance** | 80-120cm | 30-50cm |
| **Information density** | Lower | Higher |
| **Component placement** | Heavy | Light-medium |
| **Folding** | Often folded | Usually flat |

## Layout Systems (布局系统)

### Grid-Based Layout

**Hex Grid System (六边形网格):**

```
     ◄  Column width  ►
        ╱╲╱╲╱╲╱╲
       ╱  ╲  ╲  ╲  ╲
      ╱    ╲    ╲    ╲
     ╱      ╲      ╲
    ╱        ╲      ╲
   ╲        ╱      ╱
    ╲      ╱      ╱
     ╲    ╱    ╱
      ╲  ╱  ╱
       ╲╱╲╱

Grid spacing:
- Horizontal: flat-to-flat distance × 1.5
- Vertical: flat-to-flat distance × √3
```

**Square Grid System (方格网格):**

```
┌───┬───┬───┬───┐
│   │   │   │   │
├───┼───┼───┼───┤
│   │   │   │   │
├───┼───┼───┼───┤
│   │   │   │   │
└───┴───┴───┴───┘

Grid spacing:
- Cell size: 30-50mm typical
- Gutter: 2-5mm between cells
- Border: 10-20mm from edge
```

**Irregular Grid (不规则网格):**

```
┌─────┐   ┌───────┐
│     │   │       │   ┌───┐
│     ├───┤       │   │   │
└─────┘   └───────┤   ├───┘
  ┌─┐              │   │
  │ │   ┌──────┐   └───┘
  └─┘   │      │
        └──────┘

Use: Regional maps, non-uniform spaces
```

### Zone-Based Layout

**Central Zone Design:**

```
┌─────────────────────────────────┐
│  [Header/Legend Area - 15%]    │
├─────────────────────────────────┤
│  [Side Zone]   [Central Zone]   │
│    20%           60%            │  ← Main play area
│  [Score Track]  [Map/Terrain]   │
│                                 │
├─────────────────────────────────┤
│  [Footer Area - 10%]            │
│  [Player colors, turn order]    │
└─────────────────────────────────┘
```

**Multi-Zone Layout:**

```
┌─────────────┬─────────────┬─────────────┐
│  Zone A     │  Zone B     │  Zone C     │
│  (Scoring)  │  (Action)   │  (Resource) │
├─────────────┼─────────────┼─────────────┤
│             │             │             │
│   Main Play Area (Map/Terrain)        │
│             │             │             │
│   60% of board, central placement     │
└───────────────────────────────────────┘
```

### Information Hierarchy

**Visual Priority Levels:**

```
Level 1 (Most Important):
- Board title/logo
- Main play area
- Critical scoring tracks
- Turn order indicator

Level 2 (Important):
- Secondary scoring
- Resource tracks
- Action spaces
- Legend/key

Level 3 (Supporting):
- Decorative elements
- Flavor text
- Background details
- Secondary icons
```

**Hierarchy Implementation:**

| Technique | Use | Effect |
|-----------|-----|--------|
| **Size** | Primary elements larger | Instant recognition |
| **Color** | Bright colors for important | Draws attention |
| **Position** | Center/top for important | Natural viewing path |
| **Contrast** | High contrast for critical | Stand out |
| **Borders** | Frame important areas | Visual separation |

## Information Density (信息密度)

### Density Standards

**Viewing Distance Guidelines:**

| Distance | Minimum Element | Recommended | Maximum |
|----------|-----------------|-------------|---------|
| **30-50cm** (mats) | 3mm | 5-8mm | 15mm |
| **50-80cm** (close board) | 5mm | 8-12mm | 20mm |
| **80-120cm** (standard) | 8mm | 12-18mm | 30mm |
| **120cm+** (large boards) | 12mm | 18-25mm | 40mm |

**Typography Scale:**

| Element | Mats (30-50cm) | Board (80-120cm) |
|---------|----------------|------------------|
| **Title** | 14-18pt | 24-36pt |
| **Headers** | 10-12pt | 18-24pt |
| **Body** | 8-10pt | 14-18pt |
| **Captions** | 6-8pt | 10-14pt |
| **Numbers** | 10-14pt | 18-24pt |

### Content Capacity

**Maximum Content Guidelines:**

```
Small Board (A4):
- Main areas: 3-5 zones
- Tracks: 2-3 tracks
- Icons per zone: 5-8
- Text blocks: 1-2

Standard Board (A3):
- Main areas: 5-8 zones
- Tracks: 3-5 tracks
- Icons per zone: 8-12
- Text blocks: 2-3

Large Board (A2):
- Main areas: 8-12 zones
- Tracks: 5-8 tracks
- Icons per zone: 12-15
- Text blocks: 3-4
```

**Density Formula:**
```
Information Density = Elements / Area

Good density: 0.5-1.0 elements per 10cm²
High density: 1.0-2.0 elements per 10cm²
Extreme density: 2.0+ elements per 10cm² (avoid)
```

### Clutter Prevention

**Strategies:**

1. **White Space (留白):**
   - Minimum 20-30% of board
   - Between zones: 15-25mm
   - Around critical elements: 10-15mm

2. **Visual Grouping:**
   - Related elements close together
   - Use borders or backgrounds
   - Clear separation between zones

3. **Layering:**
   - Background: Subtle texture
   - Midground: Main elements
   - Foreground: Critical information

4. **Progressive Disclosure:**
   - Show only essential on board
   - Details in reference cards
   - Rules in rulebook

## Path and Area Design (路径和区域设计)

### Path Systems

**Linear Path (线性路径):**

```
Start → ─ → ─ → ─ → ─ → End

Use:
- Race tracks
- Campaign progression
- Technology trees
- Skill trees

Characteristics:
- Clear direction
- Limited choices
- Easy to understand
```

**Branching Path (分支路径):**

```
    Start
      ├ → A → ┐
      │       ├ → End
      └ → B → ┘

Use:
- Adventure games
- Skill advancement
- Story progression

Characteristics:
- Player choice
- Multiple routes
- Some backtracking
```

**Network Path (网络路径):**

```
    A ─── B
    │     │
    C ─── D ─── E
          │
          F

Use:
- Map movement
- Trade routes
- Connection games

Characteristics:
- Multiple connections
- Open-ended
- Strategic planning
```

**Area Movement (区域移动):**

```
┌─────┬─────┬─────┐
│  A  │  B  │  C  │
├─────┼─────┼─────┤
│  D  │  E  │  F  │
└─────┴─────┴─────┘

Use:
- Regional maps
- Territory control
- Area influence

Characteristics:
- Free movement
- Area-based
- Flexible
```

### Area Design

**Zone Types:**

| Zone Type | Description | Use Case | Size |
|-----------|-------------|----------|------|
| **Resource zones** | Production areas | Resource generation | 40-80mm |
| **Action spaces** | Player actions | Worker placement | 30-50mm |
| **Scoring areas** | Point tracks | Score tracking | 20-40mm wide |
| **Storage areas** | Component placement | Token/card spots | 30-60mm |
| **Information areas** | Reference | Rules reminder | Variable |

**Zone Boundary Styles:**

```
Solid Border:
┌─────────────┐
│             │
│   Zone      │
│             │
└─────────────┘
Use: Distinct areas

Dashed Border:
┌ - - - - - - ┐
│             │
│   Zone      │
│             │
└ - - - - - - ┘
Use: Related areas

Color Background:
░░░░░░░░░░░░░
░     Zone     ░
░░░░░░░░░░░░░
Use: Visual grouping

No Boundary (Proximity):
[Zone A]  [Zone B]
Use: Seamless areas
```

### Path Clarity

**Visual Indicators:**

```
Arrows (→): Direction
Dotted line (---): Optional route
Solid line (───): Main route
Color coding: Route types
Numbers: Order of traversal
Icons: Path features
```

**Clarity Principles:**

1. **Single Entry Point:**
   - Clear starting position
   - Visual marker (Start icon, color)
   - Position in logical location

2. **Directional Cues:**
   - Arrows for direction
   - Numbered steps
   - Progressive sizing
   - Color gradients

3. **Decision Points:**
   - Clearly marked branches
   - Visual separation
   - Distinct options

4. **End Points:**
   - Clear destinations
   - Visual markers
   - Reward indicators

## Folding Patterns (折叠模式)

### Fold Line Placement

**Critical Rules:**

1. **Avoid Content on Folds:**
   - Keep 15-20mm from fold line
   - Critical content: 25mm+ from fold
   - Test with prototype

2. **Fold Orientation:**
   ```
   Landscape fold:
   ┌─────────┬─────────┐
   │         │         │
   │  Left   │  Right  │
   │         │         │
   └─────────┴─────────┘
           ↑ fold

   Portrait fold:
   ┌─────────┐
   │   Top   │
   ├─────────┤
   │ Bottom  │
   └─────────┘
       ↑ fold
   ```

3. **Fold Line Visibility:**
   - Can be decorative (map feature)
   - Can be hidden (between zones)
   - Avoid crossing critical elements

### Multi-Panel Boards

**2-Panel (Standard):**

```
┌─────────────┬─────────────┐
│   Panel 1   │   Panel 2   │
│             │             │
│   210×297mm │   210×297mm │
│             │             │
└─────────────┴─────────────┘
        ↓ fold line at center
┌─────────────────────────┐
│     Folded: A4          │
│     210×297mm           │
└─────────────────────────┘
```

**4-Panel (Double Fold):**

```
┌──────┬──────┬──────┬──────┐
│  1   │  2   │  3   │  4   │
│      │      │      │      │
└──────┴──────┴──────┴──────┘
  ↓ fold        ↓ fold
┌──────────┬──────────┐
│    1+2   │    3+4   │
└──────────┴──────────┘
       ↓ fold
┌──────────────────────┐
│      All 4 Panels    │
└──────────────────────┘

Fold positions:
- First fold: Between 2 and 3
- Second fold: Between 1+2 and 3+4
```

**6-Panel (Triple Fold):**

```
┌────┬────┬────┬────┬────┬────┐
│ 1  │ 2  │ 3  │ 4  │ 5  │ 6  │
└────┴────┴────┴────┴────┴────┘
  ↓    ↓         ↓    ↓
┌────┬────┬────┬────┬────┬────┐
│1+2 │3+4 │5+6 │    │    │    │
└────┴────┴────┴────┴────┴────┘
       ↓         ↓
┌────────┬────────┬────────┐
│ 1+2+3  │ 4+5+6  │        │
└────────┴────────┴────────┘
         ↓
┌─────────────────────┐
│   All 6 Panels      │
└─────────────────────┘
```

### Board Thickness Considerations

**Thickness vs Panel Count:**

| Thickness | Max Panels | Folding | Durability |
|-----------|------------|---------|------------|
| **1.5mm** | 2 | Easy | Fair |
| **2mm** | 2-4 | Standard | Good |
| **2.5mm** | 4-6 | Stiff | Very Good |
| **3mm** | 6+ | Difficult | Excellent |

**Folding Formula:**
```
Fold resistance = Thickness² × Panels

Example:
2mm × 4 panels = 16 (manageable)
3mm × 6 panels = 54 (very stiff)
```

## Scoring Systems (计分系统)

### Track Design

**Linear Track (线性轨道):**

```
0 ───── 10 ───── 20 ───── 30 ───── 40
│                    │
Player marker      Player marker

Use:
- Point accumulation
- Resource tracking
- Progress measurement

Specs:
- Width: 8-12mm
- Height: 150-250mm
- Interval: 10-20mm per point
- Numbers: 8-12pt
```

**Circular Track (环形轨道):**

```
        10
    9       11
  8           12
  7     ⊕     1  ← Center marker
  6           2
    5       3
        4

Use:
- Round counting (calendar)
- Cycle tracking
- Limited space

Specs:
- Diameter: 80-120mm
- Interval: Equal spacing
- Numbers: Orient toward center
```

**Multi-Lane Track (多道轨道):**

```
Player 1:  ────●────
Player 2:  ───────●─
Player 3:  ──●──────

Use:
- Multiple player tracking
- Comparative scoring
- Race games

Specs:
- Lane height: 10-15mm each
- Total height: 40-80mm
- Player colors: Distinct per lane
```

### Scoring Zones

**Area-Based Scoring:**

```
┌─────────┬─────────┬─────────┐
│  1pt    │  2pt    │  3pt    │
│ Zone    │ Zone    │ Zone    │
└─────────┴─────────┴─────────┘

Use:
- Territory control
- Area majority
- Placement bonuses

Specs:
- Zone size: 40-80mm
- Value indicator: Prominent
- Boundary: Clear visual separation
```

**Tiered Scoring:**

```
┌─────────────────────────┐
│  ★★★ 10+  (3 stars)    │
│  ★★☆ 6-9   (2 stars)   │
│  ★☆☆ 3-5   (1 star)    │
│  ☆☆☆ 0-2   (0 stars)   │
└─────────────────────────┘

Use:
- Achievement levels
- Bonus thresholds
- Tier rewards
```

## Component Integration (组件集成)

### Placement Areas

**Card Slots:**

```
┌─────────┐
│  Card   │  ← Card placement area
│  Here   │
└─────────┘

Specs:
- Size: Card dimensions + 5mm
- Outline: Dashed or colored
- Label: Clear text/icon
- Capacity: Single or stack
```

**Token Wells:**

```
   ╱╲
  ╱  ╲  ← Token placement
 ╱    ╲
 ╲    ╱
  ╲  ╱
   ╲╱

Specs:
- Size: Token diameter + 3mm
- Shape: Match token shape
- Outline: Subtle
- Label: Small, nearby
```

**Player Positions:**

```
┌─────────────────────────┐
│  P1     P2     P3     P4 │
│  ⊕     ⊕     ⊕     ⊕   │
└─────────────────────────┘

Specs:
- Spacing: Even distribution
- Marker: Player color
- Label: Player number/name
- Size: 20-30mm diameter
```

### Storage Integration

**Built-in Storage:**

```
┌─────────────────────────┐
│  [Playing Area]         │
│                         │
├─────────────────────────┤
│  [Token Tray]           │  ← Integrated storage
│  ══════════           │
└─────────────────────────┘

Considerations:
- Tray depth: 5-15mm
- Separate compartments
- Lid closure possible?
- Accessibility during play
```

**Box Integration:**

```
Box Layout:
┌─────────────────┐
│  [Board]        │  ← Board in box lid
│                 │
├─────────────────┤
│  [Components]   │  ← Components in base
└─────────────────┘

Or:

┌─────────────────┐
│  [Components]   │  ← Components on board
│  ══════        │
│                 │
└─────────────────┘
```

## Visual Design (视觉设计)

### Art Style Guidelines

**Map Styles:**

| Style | Characteristics | Use Case | Complexity |
|-------|-----------------|----------|------------|
| **Realistic** | Detailed, accurate | Historical games | High |
| **Stylized** | Simplified, iconic | Most games | Medium |
| **Abstract** | Geometric, minimal | Strategy games | Low |
| **Illustrated** | Artistic, thematic | Adventure games | High |

**Color Schemes:**

```
Natural:
- Earth tones (greens, browns)
- Water (blues)
- Sky (light blues)
- Terrain variety

Fantasy:
- Magical colors (purples, teals)
- Enhanced saturation
- Dramatic contrasts
- Thematic palette

Sci-Fi:
- Cool tones (blues, grays)
- Neon accents
- High contrast
- Metallic colors
```

### Icon Integration

**Icon Placement:**

```
Corner placement:
┌─────────────────┐
│ ⊕             ⊕ │  ← Corners (unobtrusive)
│                 │
│                 │
│ ⊕             ⊕ │  ← Corners (unobtrusive)
└─────────────────┘

Edge placement:
┌─────────────────┐
│ ⊕ ⊕ ⊕ ⊕ ⊕ ⊕ ⊕ ⊕ │  ← Top/bottom edges
│                 │
│                 │
│ ⊕ ⊕ ⊕ ⊕ ⊕ ⊕ ⊕ ⊕ │  ← Top/bottom edges
└─────────────────┘

Scattered:
┌─────────────────┐
│     ⊕     ⊕     │  ← Strategic locations
│  ⊕        ⊕    │
│                 │
│     ⊕     ⊕     │
└─────────────────┘
```

**Icon Sizing:**

| Board Size | Primary Icons | Secondary Icons | Text |
|------------|---------------|-----------------|------|
| A4 | 12-15mm | 8-10mm | 8-10pt |
| A3 | 15-20mm | 10-12mm | 12-14pt |
| A2 | 20-25mm | 12-15mm | 14-18pt |

### Typography

**Font Selection:**

| Board Type | Font Style | Examples |
|------------|-----------|----------|
| **Fantasy** | Decorative, serifs | Cinzel, MedievalSharp |
| **Sci-Fi** | Geometric, sans | Orbitron, Exo 2 |
| **Modern** | Clean, sans | Montserrat, Raleway |
| **Historical** | Classic serifs | Garamond, Caslon |
| **Abstract** | Simple, geometric | Archivo Black, Saira |

**Text Placement:**

```
Titles:
- Position: Top center or top left
- Size: 24-48pt
- Weight: Bold
- Color: High contrast

Labels:
- Position: Near referenced element
- Size: 10-18pt
- Weight: Regular/Semibold
- Color: Medium-high contrast

Instructions:
- Position: Dedicated area
- Size: 8-12pt
- Weight: Regular
- Color: Medium contrast
```

## Production Specifications (制作规范)

### Board Construction

**Layer Structure:**

```
Top to Bottom:
1. Printed paper (150-200gsm)
2. Mounting adhesive
3. Core: Grayboard/Chipboard (2-3mm)
4. Mounting adhesive
5. Backing paper (150-200gsm)
6. Optional: Lamination/finish
```

**Thickness Options:**

| Thickness | Panels | Durability | Cost | Use Case |
|-----------|--------|------------|------|----------|
| **1.5mm** | 1-2 | Fair | Low | Small games |
| **2mm** | 2-4 | Good | Medium | Standard (most common) |
| **2.5mm** | 4-6 | Very Good | Medium-High | Large games |
| **3mm** | 6+ | Excellent | High | Premium games |

### Finishing Options

**Surface Finishes:**

| Finish | Durability | Glare | Texture | Write-on | Cost |
|--------|------------|-------|----------|----------|------|
| **Uncoated** | Low | None | Smooth | Yes (pencil) | Low |
| **Matte varnish** | Medium | Low | Slight | Yes (pencil) | Medium |
| **Gloss varnish** | High | High | Smooth | No | Medium |
| **Linen texture** | Very High | Low | Textured | No | High |
| **UV coating** | Extreme | High | Smooth | No | High |

**Edge Finishing:**

- **Raw cut**: Basic, may fray
- **Taped edges**: Durable, clean look
- **Wrapped**: Paper wraps around edges
- **Sealed**: Edge sealing prevents wear

### File Specifications

**Resolution:**
- 300 DPI @ final size
- Vector art preferred for text and icons
- Raster images: 300 DPI minimum

**Color Mode:**
- CMYK for printing
- Color profile: FOGRA39 (coated) or FOGRA51 (uncoated)
- Convert all spot colors if needed

**Bleed:**
- Standard: 5mm all sides (thick stock requires more)
- Critical content: 15mm from trim edge
- Keep 20mm from fold lines

**File Format:**
- PDF/X-4 recommended
- Include crop marks
- Include registration marks
- Separate layers for dielines if needed

### Folding and Assembly

**Scoring:**

```
Score types:
- Blind emboss: Groove on one side
- Channel score: V-shaped groove
- Perforation: Partial cuts (for punch-out)

Score depth:
- Standard: 50% of thickness
- Heavy stock: 60-70%
- Test with prototype
```

**Assembly Methods:**

| Method | Complexity | Durability | Cost |
|--------|------------|------------|------|
| **Tape hinge** | Low | Medium | Low |
| **Cloth tape** | Medium | High | Medium |
- **Hinged sheet** | High | Very High | High |
| **Separate panels** | Low | Low (can separate) | Low |

## Quality Control (质量控制)

### Pre-Press Checklist

**Design Phase:**
- [ ] Final dimensions confirmed (unfolded + folded)
- [ ] Panel arrangement optimized
- [ ] Fold line positions verified
- [ ] Content cleared from fold lines (15-20mm)
- [ ] Bleed added (5mm)
- [ ] Safe zones maintained (15mm from trim)

**Artwork Phase:**
- [ ] Resolution 300 DPI
- [ ] CMYK mode
- [ ] Color proof created
- [ ] Typography legible at viewing distance
- [ ] Icons appropriately sized
- [ ] Style consistency maintained

**Production Phase:**
- [ ] Thickness specified (2mm standard)
- [ ] Finish specified (matte/gloss/linen)
- [ ] Scoring positions marked
- [ ] Assembly method specified
- [ ] Prototype ordered

**Proof Phase:**
- [ ] Color accuracy verified
- [ ] Content checked for errors
- [ ] Fold lines tested
- [ ] Board flatness checked
- [ ] Component fit verified
- [ ] Durability tested (handle, fold)

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| **Content on fold** | Poor layout planning | Keep 15-20mm from folds |
| **Board warps** | Uneven lamination, humidity | Condition board, use thicker core |
| **Colors dull** | Uncoated stock absorbs ink | Adjust colors, use coated stock |
| **Fold misaligned** | Scoring error | Verify score positions |
| **White edges** | Insufficient bleed | Add 5mm bleed |
| **Text illegible** | Font too small | Increase size (12-18pt minimum) |
| **Peeling layers** | Poor adhesive quality | Specify better materials |

## Player Mat Special Considerations

### Mat vs Board Differences

**Player Mats:**
- Higher information density
- Closer viewing distance (30-50cm)
- Individual ownership
- Usually no folding
- Often reference-heavy

**Game Boards:**
- Lower information density
- Farther viewing distance (80-120cm)
- Shared ownership
- Often folded
- Component placement focus

### Mat Layout Patterns

**Resource Tracking Mat:**

```
┌─────────────────────────┐
│  [Player Name/Color]     │
├─────────────────────────┤
│  Resources:              │
│  ⚔️ 🛡️ 💰 🧪           │
│  [3] [2] [5] [1]         │
├─────────────────────────┤
│  Buildings/Units:        │
│  ☐ ☐ ☐ ☐ ☐             │
├─────────────────────────┤
│  Score Track:            │
│  0 ──●── 10 ─── 20      │
└─────────────────────────┘
```

**Action Reference Mats:**

```
┌─────────────────────────┐
│  Action Cost & Effects   │
├─────────────────────────┤
│  Action 1:              │
│  Cost: 💰💰            │
│  Effect: Draw 2 cards   │
├─────────────────────────┤
│  Action 2:              │
│  Cost: ⚔️              │
│  Effect: +1 attack      │
├─────────────────────────┤
│  Action 3:              │
│  Cost: 🧪🧪           │
│  Effect: Build +1       │
└─────────────────────────┘
```

**Technology Tree Mats:**

```
┌─────────────────────────┐
│  Technology:            │
│  Level 1:  ☐  ☐  ☐     │
│     │      │   │        │
│  Level 2:  ☐  ☐  ☐     │
│     │      │   │        │
│  Level 3:  ☐  ☐  ☐     │
└─────────────────────────┘
```

## Quick Reference (快速参考)

### Standard Board Sizes

| Folded | Unfolded | Panels | Play Area | Thickness |
|--------|----------|--------|-----------|-----------|
| A5 | A4 | 1 | 190×270mm | 2mm |
| A4 | A3 | 2 | 400×270mm | 2mm |
| A3 | A2 | 2 | 570×390mm | 2.5mm |

### Typography Scale

| Board Size | Title | Headers | Body | Numbers |
|------------|-------|---------|------|---------|
| A4 | 24-36pt | 18-24pt | 14-18pt | 18-24pt |
| A3 | 36-48pt | 24-36pt | 18-24pt | 24-36pt |
| A2 | 48-72pt | 36-48pt | 24-36pt | 36-48pt |

### Minimum Sizes (at 80-120cm viewing)

- Text: 14pt minimum
- Icons: 12mm minimum
- Numbers: 18pt minimum
- Track spacing: 15mm minimum

### Folding Guidelines

- Content: 15-20mm from fold lines
- Critical content: 25mm+ from folds
- Bleed: 5mm all sides
- Safe zone: 15mm from trim

### Material Recommendations

- Standard: 2mm grayboard
- Large boards: 2.5mm grayboard
- Premium: 3mm with linen finish
- Eco-friendly: Recycled grayboard

## Case Studies

### Catan-Style Board

**Specs:**
- Size: Assembly of hex tiles
- No fixed board
- Tiles form modular board
- Random arrangement each game

**What Works:**
- High replayability
- Modular design
- No fold line constraints
- Component integration

### Ticket to Ride Board

**Specs:**
- Size: Large folded board
- Map-based design
- Route connections
- City placement

**What Works:**
- Clear visual style
- Route clarity
- Color coding
- Strategic layout

### Pandemic Board

**Specs:**
- Size: Standard folded board
- Disease tracking
- City connections
- Player roles

**What Works:**
- Information density balance
- Color coding
- Icon system
- Clean design

## References

- **Parent skill**: print-design
- **Related skills**: boardgame-cards, boardgame-tiles, boardgame-components
- **References**: `print-design/references/boardgame-specs.md`
- **Production specs**: `print-design/references/print-specs.md`

---

**Version**: 1.0.0
**Last Updated**: 2025-01-23
**Default Size**: A3 unfolded (420×297mm) unless otherwise specified
