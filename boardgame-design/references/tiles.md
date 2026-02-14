---
name: boardgame-tiles
description: Board game tile design including hexagonal/square/circular tiles, edge connection systems, rotation compatibility, die-cut considerations, and print production for game tiles.
version: 1.0.0
parent: print-design
tags: [boardgame, tiles, print-design, game-components, hex-tiles]
triggers:
  - "设计桌游方块"
  - "六边形方块设计"
  - "方块边缘连接"
  - "板块拼接设计"
  - "卡坦岛风格方块"
---

# Board Game Tile Design

Complete guide to designing and producing board game tiles, from hexagonal and square tiles to edge connection systems and die-cut specifications.

## Tile Types and Standards (方块类型和标准)

### Hexagonal Tiles (六边形方块)

The most common tile shape in board games, popularized by games like Catan.

**Standard Hex Sizes:**

| Name | Flat-to-Flat | Point-to-Point | Thickness | Use Case |
|------|--------------|----------------|-----------|----------|
| **Small** | 30mm | 34.6mm | 1.5mm | Catan-style, small games |
| **Medium** | 40mm | 46.2mm | 2mm | Standard size, most games |
| **Large** | 50mm | 57.7mm | 2mm | Premium, detailed art |
| **Extra Large** | 60mm | 69.3mm | 2.5mm | Oversized, special games |

**Hex Mathematics:**
```
Width (point-to-point) = Flat-to-Flat × 1.1547
Height (flat-to-flat) = Side length × 2
Area = (3√3 / 2) × side² ≈ 2.598 × side²
```

**Why Hexagons?**
- 6 edges (more connection options than squares)
- Natural tessellation (no gaps when placed together)
- Creates organic, map-like layouts
- Proven in countless games

### Square Tiles (方形方块)

Classic tile shape used in games like Carcassonne.

**Standard Square Sizes:**

| Name | Width × Height | Thickness | Corner Radius | Use Case |
|------|----------------|-----------|---------------|----------|
| **Small** | 25-30mm | 1.5-2mm | 2-3mm | Tokens, small tiles |
| **Medium** | 40-45mm | 2mm | 3-4mm | Standard size (Carcassonne) |
| **Large** | 50-60mm | 2-2.5mm | 4-5mm | Premium, detailed |

**Square Tile Advantages:**
- Simple grid layout
- Easy to design and manufacture
- Familiar to players
- 4-way connections (simpler than hex)

**Corner Radius:**
- Small tiles: 2-3mm (8-10% of side)
- Medium tiles: 3-4mm (7-9% of side)
- Large tiles: 4-5mm (7-9% of side)
- Purpose: Prevents chipping, easier handling

### Other Tile Shapes

**Circular Tiles (圆形):**

| Diameter | Thickness | Use Case |
|----------|-----------|----------|
| 25mm | 2mm | Small tokens |
| 35mm | 2mm | Medium markers |
| 40-50mm | 2.5mm | Large game pieces |

**Double Hexes (双六边形):**
- Two hexes joined together
- Creates larger pieces
- Used in some train games
- Dimensions vary by design

**Custom Shapes:**
- Formed by combining basic shapes
- Requires custom die-cut
- Higher tooling cost
- Creates unique visual identity

## Edge Connection Systems (边缘连接系统)

### Hexagon Edge Patterns

**All Edges Connect (全连接):**
```
    ╱╲
  ╱    ╲  ← All 6 edges can connect
 ╱  ╲  ╱ ╲
╱    ╲╱    ╲
╲    ╱╲    ╱
 ╲  ╱  ╲  ╱
  ╲    ╱  ← All edges identical
    ╲╱
```
- Use: Generic terrain tiles
- Advantage: Maximum flexibility
- Disadvantage: Can feel repetitive

**Variable Edges (可变边缘):**
```
    ╱╲
  ╱ 🌲╲  ← Edge features (roads, cities)
 ╱  ╲  ╱ ╲
╱ 🛣️ ╲╱ 🏔️╲
╲    ╱╲    ╱
 ╲  ╱  ╲  ╱
  ╲ 💧╱
    ╲╱
```
- Use: Terrain with features (Catan, Carcassonne)
- Advantage: Creates strategic gameplay
- Disadvantage: Requires careful edge matching

**Edge Coding Options:**

| Method | Description | Visibility | Complexity |
|--------|-------------|------------|------------|
| **Color coding** | Different edge colors | High | Low |
| **Symbol matching** | Roads, cities, resources | High | Medium |
| **Shape interlocking** | Physical shapes | Very High | High |
| **Number coding** | Numbers on edges | Low | Low |

### Square Edge Patterns

**4-Way Connections (四方连接):**
```
┌─────┬─────┬─────┐
│     │     │     │
├─────┼─────┼─────┤  ← All 4 sides connect
│     │     │     │
├─────┼─────┼─────┤
│     │     │     │
└─────┴─────┴─────┘
```
- Use: Generic tiles, open terrain
- Advantage: Simple, flexible
- Disadvantage: Can feel generic

**Half-Edge Connections (半边连接):**
```
┌─────┬─────┬─────┐
│ ╲   │   ╱│   ╲│
│  ╲  │  ╱ │  ╲ │  ← Roads/cities connect to edges
│   ╲ │╱   │   ╲│
├─────┼─────┼─────┤
│   ╱ │╲   │   ╱│
│  ╱  │  ╲ │  ╱ │
│ ╱   │   ╲│   ╱│
└─────┴─────┴─────┘
```
- Use: Carcassonne-style features
- Advantage: Creates complex networks
- Disadvantage: Requires careful matching

**Edge Entry Points:**

| Entry Type | Description | Placement | Use Case |
|------------|-------------|-----------|----------|
| **Center** | Feature at tile center | Middle of edge | Roads, paths |
| **Offset** | Feature offset from center | 1/3 from edge | Cities, fields |
| **Multiple** | More than one per edge | Evenly spaced | Complex features |

### Edge Design Principles

**Visual Clarity (视觉清晰度):**
- Edge features must be instantly recognizable
- Test at 60-80cm viewing distance
- Use high contrast colors
- Avoid small details (<2mm)

**Alignment Tolerance (对齐容差):**
- Design for ±0.5mm misalignment
- Make connections forgiving
- Visual continuity is more important than perfect alignment
- Test with physical prototype

**Color Consistency (色彩一致性):**
- Edge colors must match exactly across tiles
- Use Pantone colors for critical edge matches
- Test printed samples for color accuracy
- Consider lighting variations

## Tile Layout Design (方块布局设计)

### Visual Hierarchy

**Layer Structure:**

```
┌─────────────────────┐
│  [Terrain Base]      ← Layer 1: Background color/texture
│  ┌───────────────┐  │
│  │ [Main Feature]│  ← Layer 2: Roads, cities, rivers
│  │  ┌─────────┐  │  │
│  │  │[Detail] │  │  ← Layer 3: Small details, icons
│  │  └─────────┘  │  │
│  └───────────────┘  │
│  [Number/Symbol]    ← Layer 4: Game information
└─────────────────────┘
```

**Information Priority:**
1. **Terrain type** - Must be instantly recognizable
2. **Edge connections** - Critical for gameplay
3. **Special features** - Resources, bonuses
4. **Numbers/symbols** - Game mechanics

### Hexagon Layout Zones

**Critical Areas:**

```
        ╱╲
      ╱    ╲
    ╱  ╲  ╱ ╲
  ╱ 中心区  ╲  ← Center: Primary feature
╱  (40%直径)  ╲
╲    ╱╲    ╱
 ╲  ╱  ╲  ╱
  ╲边缘区╱  ← Edges: Connection features
    ╲  ╱
      ╲╱
```

**Zone Guidelines:**
- **Center zone (40% of diameter)**: Main visual, primary feature
- **Middle zone (30% of diameter)**: Secondary details, decorations
- **Edge zone (30% of diameter)**: Connection features, edge coding

**Content Placement:**
- Numbers: Center or prominent location
- Icons: Near relevant features
- Text: Minimum 3mm height, sans-serif
- Small details: Avoid central area

### Square Tile Layout

**Grid-Based Layout:**

```
┌─────────────────┐
│  ┌───────────┐  │
│  │  Feature  │  │  ← Main feature in center
│  │    (50%)  │  │
│  └───────────┘  │
│  ┌─┐┌─┐┌─┐┌─┐  │
│  │ ││ ││ ││ │  │  ← Edge connections (25% zones)
│  └─┘└─┘└─┘└─┘  │
└─────────────────┘
```

**Zoning:**
- Center: 50% area for main feature
- Edges: 25% from each edge for connections
- Corners: Can be used for diagonal features

## Rotation Compatibility (旋转兼容性)

### Rotation-Sensitive Designs

**When Rotation Matters:**
- Tiles with directional features
- Asymmetric edge connections
- Numbered placement (hex corners)
- Specific orientation required

**Rotation Indicators:**

| Method | Description | Example |
|--------|-------------|---------|
| **Orientation marks** | Small marks indicating top | Catan number placement |
| **Asymmetric art** | Art only works one way | Landscape tiles |
| **Edge coding** | Edges differ per side | City/route tiles |
| **Number placement** | Numbers in specific corners | Catan-style |

### Rotation-Independent Designs

**When Rotation Doesn't Matter:**
- Symmetrical terrain
- All edges identical
- Pure resource tiles
- Generic tiles

**Design Strategies:**
```
Rotational Symmetry (60° for hex, 90° for square):
     ╱╲           ╱╲
   ╱    ╲       ╱    ╲
  ╱  ╲  ╱ ╲     ╲  ╱  ╲ ╱  ← Looks same when rotated
 ╱    ╲╱    ╲     ╲╱    ╱╲
╲    ╱╲    ╱       ╲    ╱
 ╲  ╱  ╲  ╱
     ╲╱

Radial Symmetry:
     ╱╲
   ╱  ⭐  ╲  ← Same from center outward
  ╱   ⭐   ╲
 ╲    ⭐    ╱
  ╲   ⭐   ╱
   ╲  ⭐  ╱
     ╲╱
```

**Advantages:**
- Players can place tiles in any orientation
- Faster gameplay
- Easier to design
- Reduces tile count needed

### Mixed Rotation Strategies

**Hybrid Approach:**
- Base terrain: Rotation-independent
- Features: Rotation-sensitive
- Numbers: Placed after placement

**Example:**
```
Tile: Forest + Road
- Forest: Rotation-independent (all sides forest)
- Road: Rotation-sensitive (one side has road)
- Number: Placed after road orientation chosen
```

## Icon and Symbol Integration (图标和符号集成)

### Icon Scale Standards

**Hexagonal Tiles:**

| Tile Size | Primary Icon | Secondary Icon | Text |
|-----------|--------------|----------------|------|
| 30mm | 8-10mm | 5-7mm | 2.5-3mm |
| 40mm | 10-14mm | 6-8mm | 3-4mm |
| 50mm | 14-18mm | 8-10mm | 4-5mm |
| 60mm | 16-20mm | 10-12mm | 5-6mm |

**Square Tiles:**

| Tile Size | Primary Icon | Secondary Icon | Text |
|-----------|--------------|----------------|------|
| 30mm | 8-10mm | 5-7mm | 2.5-3mm |
| 40mm | 12-16mm | 7-9mm | 3-4mm |
| 50mm | 16-20mm | 9-12mm | 4-5mm |

### Icon Placement

**Center Placement:**
```
     ╱╲
   ╱    ╲
  ╱  [图标]  ╲  ← Icon in center
 ╲         ╱
  ╲       ╱
     ╲╱
```
- Use: Primary resource, main feature
- Advantage: Most visible
- Disadvantage: Can interfere with edge connections

**Offset Placement:**
```
     ╱╲
   ╱    ╲
  ╱  ╲  ╱ ╲
╲ [图标]  ╱  ← Icon offset from center
 ╲  ╱  ╲  ╱
  ╲    ╱
     ╲╱
```
- Use: Secondary features, numbers
- Advantage: Doesn't block center
- Disadvantage: Less prominent

**Multiple Icons:**
```
     ╱╲
   ╱ ⭐╲  ← Multiple icons evenly spaced
  ╱  *  ╲
╲  ⭐  ╱  ← Triangle formation for 3 icons
 ╲  ╱  ╲  ╱
     ╲╱
```
- Use: Multiple resources, bonuses
- Rule: Even spacing, visual balance
- Maximum: 3-4 icons per tile

### Number Systems

**Hex Corner Numbers:**
```
      ╱1╲
    ╱    ╲
  6╱      ╲2
  ╲      ╱
  5╲    ╱3
     ╲4╱
```
- Catan-style number placement
- Numbers placed at hex corners
- Used for resource generation
- Requires number tokens

**Center Numbers:**
```
     ╱╲
   ╱    ╲
  ╱   6   ╲  ← Number in center
 ╲         ╱
  ╲       ╱
     ╲╱
```
- Simple, prominent
- Use: Value, cost, strength
- Minimum size: 4mm at 40mm tile

**Edge Numbers:**
```
     ╱╲
   ╱ 3  ╲  ← Numbers near edges
  ╱  ╲  ╱ ╲
╲    ╱╲    ╱
 ╲  ╱  ╲  ╱
  ╲    ╱
     ╲╱
```
- Use: Edge values, connection costs
- Align with edge features

## Color Strategy (色彩策略)

### Terrain Color Coding

**Standard Terrain Colors:**

| Terrain | CMYK | Pantone | Association |
|---------|------|---------|-------------|
| **Forest** | C60 M0 Y100 K40 | PMS 5595 | Green, nature |
| **Mountain** | C0 M0 Y0 K60 | PMS 424 | Gray, stone |
| **Hill** | C0 M20 Y40 K10 | PMS 4685 | Brown, earth |
| **Field/Pasture** | C20 M0 Y100 K0 | PMS 5845 | Light green |
| **Desert** | C0 M30 Y60 K10 | PMS 4695 | Sandy |
| **Water** | C100 M30 Y0 K10 | PMS 2985 | Blue |
| **Swamp** | C40 M20 Y40 K20 | PMS 5605 | Murky green |

**Color Accessibility:**
- Test color blind combinations
- Avoid red/green terrain distinctions
- Use symbols + color for clarity
- Ensure contrast ≥ 3:1

### Edge Color Coding

**Matching System:**
```
Road edges: Gray/Black (C0 M0 Y0 K70)
Water edges: Blue (C100 M30 Y0 K10)
Forest edges: Green (C60 M0 Y100 K40)
City edges: Red (C0 M100 Y100 K10)
```

**Best Practices:**
- Edge colors must match exactly
- Use Pantone for critical matches
- Test printed samples
- Consider lighting variations

## Production Specifications (制作规范)

### Material Selection

**Common Materials:**

| Material | Thickness | Durability | Cost | Best For |
|----------|-----------|------------|------|----------|
| **Grayboard/Chipboard** | 1.5-2mm | Good | Low | Standard tiles |
| **Mounting board** | 2mm | Very Good | Medium | Premium tiles |
| **Pressboard** | 2.5-3mm | Excellent | High | Heavy use |
| **Cardstock** | 0.3-0.4mm | Fair | Low | Thin tiles, inserts |

**Recommendation:** 2mm grayboard for most games

### Die-Cut Specifications

**Cutting Tolerances:**
- Die-cut position: ±0.3mm
- Edge straightness: ±0.2mm
- Corner radius: ±0.2mm
- Registration: ±0.5mm

**Bleed Requirements:**
- Standard bleed: 2-3mm beyond cut line
- Thick stock (2mm+): 3-5mm bleed
- Critical content: 2mm from cut edge

**Die Line Creation:**
```
Example Hex Die Line (40mm flat-to-flat):
- Vector path required
- Corner radius: 3-4mm
- Include registration marks
- Test cut before production
```

### Sheet Imposition

**A4 Sheet Layout (40mm hex tiles):**

```
┌────────────────────────────────┐
│  ╱╲ ╱╲ ╱╲ ╱╲ ╱╲              │
│ ╱  ╲╱  ╲╱  ╲╱  ╲╱  ╲          │  Row 1: 5 tiles
│╱    ╲    ╲    ╲    ╲          │
╲    ╱    ╱    ╱    ╱          │
 ╲  ╱  ╲╱  ╲╱  ╲╱  ╲          │  Row 2: 4 tiles (offset)
│╱    ╲    ╲    ╲              │
│ ╲    ╱    ╱    ╱              │
│  ╲  ╱  ╲╱  ╲╱                │  Row 3: 5 tiles
└────────────────────────────────┘
```

**Tile Count per A4:**

| Tile Size | Hex Count | Square Count | Efficiency |
|-----------|-----------|--------------|------------|
| 30mm | 50-60 | 64-81 | 85-90% |
| 40mm | 35-40 | 36-49 | 85-90% |
| 50mm | 20-25 | 20-25 | 80-85% |

**Spacing:**
- Between tiles: 2-3mm
- From sheet edge: 5mm
- Registration marks: 5mm from tiles

### Front-to-Back Registration

**When Tiles Are Double-Sided:**

```
Front:           Back (rotated 180°):
╱╲ ╱╲           ╱╲ ╱╲
╲╱ ╲╱  ← rotate  ╲╱ ╲╱
```

**Alignment Tolerance:**
- Center-to-center: ±0.5mm
- Rotation: <0.3°
- Color matching: ΔE < 3

**Testing:**
- Always create proof sheet
- Test front/back alignment
- Check opacity (show-through)
- Verify edge registration

## Artwork Guidelines (美术指南)

### Resolution and Scale

**Resolution Requirements:**
- 300 DPI @ final print size
- Vector artwork preferred
- Raster images: 300 DPI minimum
- Line art: 600-1200 DPI for crispness

**Scale Considerations:**
```
Art at 40mm tile:
- Main feature: 15-20mm high
- Small details: Minimum 0.5mm
- Text: Minimum 3mm high
- Icons: Minimum 5mm
```

### Style Consistency

**Art Style Guide:**
```
Establish:
- Color palette (specific CMYK values)
- Line weights (consistent across tiles)
- Perspective (isometric, top-down, etc.)
- Level of detail (match across all tiles)
- Rendering technique (painted, illustrated, etc.)
```

**Reference Creation:**
- Create style guide before production
- Include examples of each terrain type
- Define edge connection styles
- Specify icon treatments

### File Organization

**Layer Structure:**
```
1. Background (terrain base)
2. Texture/Pattern
3. Main Features
4. Edge Connections
5. Details/Decorations
6. Numbers/Symbols
7. Die Line (separate file)
```

**File Formats:**
- Working files: AI, PSD, or INDD
- Print files: PDF/X-4
- Die lines: DXF or PDF
- Organize by tile type

## Quality Control (质量控制)

### Pre-Press Checklist

**Design Phase:**
- [ ] Final dimensions confirmed
- [ ] CMYK color mode
- [ ] 300 DPI resolution
- [ ] Bleed added (2-3mm)
- [ ] Safe zone maintained
- [ ] Die line created
- [ ] Color palette defined

**Artwork Phase:**
- [ ] Style guide followed
- [ ] All terrains represented
- [ ] Edge connections match
- [ ] Icons consistent
- [ ] Text legible
- [ ] Numbers/_symbols clear

**Production Phase:**
- [ ] Sheet layout optimized
- [ ] Die line verified
- [ ] Registration marks added
- [ ] Color proofs created
- [ ] Test cut requested
- [ ] Front/back alignment checked

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| **Colors don't match** | RGB mode or wrong profile | Use CMYK, correct profile |
| **Edges misaligned** | Poor die cutting | Check tolerance, request new die |
| **Show-through** | Thin stock, dark colors | Use thicker stock, lighter colors |
| **Tiles curl** | Humidity, uneven drying | Condition tiles, use thicker stock |
| **Ink rubs off** | Insufficient coating | Add varnish or coating |
| **Colors dull** | Uncoated stock | Adjust for paper absorbency |

## Game Design Considerations (游戏设计考量)

### Tile Count Planning

**Minimum Tile Count:**
- Hex tiles: 30-50 for small game
- Hex tiles: 50-100 for standard game
- Square tiles: 80-120 for standard game
- Adjust based on map size and variety

**Distribution Formula:**
```
Tiles needed = (Map area / Tile area) × Variety factor

Example (Catan-style map):
- Map: 6×6 hex grid (36 tiles)
- Ocean: 6 tiles
- Number tokens: 36
- Variety factor: 1.5-2 (for variety)
- Total tiles: 36 + 6 + 36 = 78 tiles
```

### Gameplay Balance

**Resource Distribution:**
```
Balanced distribution (Catan model):
- Common resources: 6 tiles each
- Uncommon resources: 4 tiles each
- Rare resources: 2 tiles each
- Desert: 1 tile (none)
```

**Number Distribution:**
- High numbers (6, 8): Few tiles
- Medium numbers (4-10): Many tiles
- Low numbers (2, 12): Few tiles
- Use probability curve

### Storage and Components

**Box Storage:**
- Tile count × tile area = storage area
- Add 20% for spacing and bags
- Consider bag vs box storage
- Account for thickness

**Component Integration:**
- Tiles work with other components?
- Compatible with player mats?
- Need storage trays?
- Consider assembly time

## Quick Reference (快速参考)

### Standard Sizes

**Hexagons:**
- Small: 30mm flat-to-flat
- Medium: 40mm flat-to-flat (most common)
- Large: 50mm flat-to-flat

**Squares:**
- Small: 30×30mm
- Medium: 40×40mm (most common)
- Large: 50×50mm

### Standard Thickness

- Grayboard: 1.5-2mm (standard)
- Mounting board: 2mm (premium)
- Pressboard: 2.5-3mm (heavy duty)

### Minimum Sizes

- Small details: 0.5mm
- Icons: 5mm
- Text: 3mm height
- Numbers: 4mm height

### Common Quantities

- Small game: 30-50 tiles
- Standard game: 50-100 tiles
- Large game: 100-200 tiles

### Sheet Yield (A4)

- 30mm hex: ~50-60 tiles
- 40mm hex: ~35-40 tiles
- 50mm hex: ~20-25 tiles
- 40mm square: ~36 tiles
- 50mm square: ~25 tiles

## Case Studies

### Catan-Style Hexes

**Specs:**
- Size: 40mm flat-to-flat
- Thickness: 2mm grayboard
- Art: Printed, full bleed
- Numbers: Separate tokens

**Features:**
- 6 edge types (roads)
- 6 terrain types
- Ports on edge tiles
- Number placement on hex corners

**What Works:**
- Iconic terrain design
- Simple color coding
- Modular board building
- Number token system

### Carcassonne-Style Squares

**Specs:**
- Size: 45×45mm
- Thickness: 2mm grayboard
- Art: Detailed illustrations
- Edge features: Roads, cities, fields

**Features:**
- 4 edge connections
- Mix of terrain types
- Scoring on edges
- Meeple placement

**What Works:**
- Edge matching gameplay
- Detailed art creates world
- Simple placement rules
- Expansions add new tiles

## References

- **Parent skill**: print-design
- **Related skills**: boardgame-cards, boardgame-boards, boardgame-components
- **References**: `print-design/references/boardgame-specs.md`
- **Die cutting**: `print-design/references/print-specs.md`

---

**Version**: 1.0.0
**Last Updated**: 2025-01-23
**Default Size**: 40mm flat-to-flat hex (unless otherwise specified)
