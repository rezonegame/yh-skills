---
name: boardgame-cards
description: Board game card design including layout hierarchy, icon systems, back alignment, and sheet imposition. Covers poker/mini/square sizes, readability standards, and print production for game cards.
version: 1.0.0
parent: print-design
tags: [boardgame, cards, print-design, game-components, layout]
triggers:
  - "设计桌游卡牌"
  - "卡牌布局"
  - "卡牌背面对齐"
  - "卡牌整版排版"
  - "游戏卡牌制作"
---

# Board Game Card Design

Complete guide to designing and producing board game cards, from layout hierarchy to print-ready files.

## Standard Card Sizes (标准卡牌尺寸)

| Type | Dimensions | Aspect Ratio | Common Uses | Cards per A4 |
|------|------------|--------------|-------------|--------------|
| **Poker** | 63 × 88 mm | 1:1.4 | Most board games, playing cards | 14-16 |
| **Bridge** | 57 × 89 mm | 1:1.56 | Traditional cards, Tarot | 16-18 |
| **Mini European** | 44 × 67 mm | 1:1.52 | Card games, small games | 20-24 |
| **Square** | 70 × 70 mm | 1:1 | Tile cards, some games | 12-14 |
| **Hexagonal** | 60 × 70 mm | ~1:1.2 | Special games, tile-cards | 12-14 |
| **Large** | 80 × 120 mm | 1:1.5 | Reference cards, oversized | 8-10 |

**Selection Guide:**
- **Poker size**: Default choice, versatile, standard card sleeves available
- **Mini European**: Games with many cards (100+), smaller box footprint
- **Square**: Tile-like cards, unique visual feel
- **Custom**: Match your game's specific needs

## Card Face Layout System (卡牌正面布局)

### Standard Layout Structure

```
┌──────────────────────────────┐
│  [Icon]  Title Text  [Badge]  │ ← Header (12-18% height)
├──────────────────────────────┤
│                              │
│      [Main Artwork Area]      │ ← Visual (30-45% height)
│                              │
├──────────────────────────────┤
│  [Ability/Effect Text]        │ ← Body (40-55% height)
│  • Icon-text integration       │     Readability priority
│  • Keywords highlighted        │     Clear hierarchy
│  • Supporting details          │
│                              │
└──────────────────────────────┘
```

### Poker Size Layout Dimensions (63×88mm)

**Zone Heights:**
- Header: 10-16mm (12-18%)
- Artwork: 27-40mm (30-45%)
- Body text: 35-48mm (40-55%)

**Margins:**
- Outer margin: 3-5mm
- Internal spacing: 2-3mm
- Safe zone: 1.5mm from edge (before bleed)

### Typography Scale (at poker size)

| Element | Font Size | Weight | Use Case |
|---------|-----------|--------|----------|
| **Title** | 10-12pt | Bold/Semibold | Card name, main identifier |
| **Body** | 7-9pt | Regular | Effect text, descriptions |
| **Keywords** | 8-10pt | Bold | Important terms, icons + text |
| **Flavor** | 6-7pt | Italic/Regular | Flavor text, non-critical |
| **Footer** | 5-6pt | Regular | Expansion symbols, icons |

**Scaling Rules:**
- Mini cards (70% of poker): Multiply by 0.7
- Large cards (150% of poker): Multiply by 1.5
- Always maintain readability at 50-80cm viewing distance

### Icon Placement Standards

```
Standard Icon Positions:
┌──────────────────────────────┐
│ ⚔️     ATTACK CARD        +3  │
│                              │
│       [Sword Artwork]         │
│                              │
│ Deal 3 damage to target.     │
│ ⚔️ If you have a weapon,     │
│   deal +2 damage.            │
│                              │
│              ⭐ Set 2         │
└──────────────────────────────┘

Top-left: Cost/Resource icons (3-5mm from corner)
Top-right: Score/strength/points badges
Bottom-left: Keyword/category icons
Bottom-right: Expansion set symbols, rarity icons
```

**Icon Size Standards (at poker size):**
- Primary icons: 8-10mm
- Secondary icons: 5-7mm
- Small inline icons: 3-4mm
- Minimum spacing: 1mm between icons

## Information Hierarchy (信息层级)

### Visual Hierarchy Principles

**1. Size Contrast (尺寸对比)**
```
Title: 100%
Body: 70-80%
Keywords: 80-90%
Footer: 50-60%
```

**2. Position Hierarchy (位置层级)**
```
Primary (title): Top-center or Top-left
Secondary (keywords): Top-right or highlight color
Tertiary (body): Main area, middle
Quaternary (footer): Bottom corners
```

**3. Weight Contrast (字重对比)**
```
Title: Bold (700)
Keywords: Semibold (600)
Body: Regular (400)
Flavor: Regular or Light (300-400)
```

**4. Color Coding (色彩编码)**
```
Critical information: High contrast, distinctive color
Supporting information: Medium contrast
Background: Neutral, low contrast
```

### Card Types & Their Hierarchy Needs

**Action Cards (行动卡):**
- Large action name
- Clear cost/value indicator
- Prominent effect text
- Icon-heavy if possible

**Resource Cards (资源卡):**
- Large resource icon
- Value prominently displayed
- Minimal text
- Symbol-heavy

**Character/Unit Cards (角色/单位卡):**
- Large character art
- Name and stats prominent
- Abilities secondary
- Visual appeal priority

**Reference Cards (参考卡):**
- Text-heavy
- Organized in sections
- Clear visual grouping
- Hierarchy through spacing

## Icon System Integration (图标系统集成)

### Standard Game Icon Sets

**Resource Icons (资源图标):**
```
⚔️ Attack/Combat
🛡️ Defense/Armor
💰 Gold/Money
🧱 Brick/Stone
🌿 Wood/Resource
💎 Gem/Precious
⚡ Energy/Power
🧪 Potion/Magic
```

**Action Icons (行动图标):**
```
👁️ Look/Inspect
🎯 Target/Aim
⚡ Activate/Trigger
🔑 Unlock/Open
📦 Draw/Collect
🔄 Refresh/Reset
⏸️ Pause/Hold
🚫 Forbidden/Cancel
```

**Number/Value Icons (数值图标):**
```
①②③④⑤⑥⑦⑧⑨⑩
ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ
⭐★☆ (points/stars)
```

### Icon Design Guidelines

**1. Consistency (一致性)**
- Unified line weight: 2-3pt at card size
- Single style: linear OR filled, not mixed
- Consistent corner radius: 15-25% of size

**2. Clarity (清晰性)**
- Test at minimum size (4mm @ poker card)
- Avoid fine details below 0.5mm
- Use high contrast against background

**3. Cultural Neutrality (文化中立性)**
- Prefer universal symbols
- Avoid text when possible
- Use multiple cues (color + shape + icon)

**4. Scalability (可缩放性)**
- Design for 15mm-60mm range
- Test at extreme sizes
- Maintain recognizability when scaled

### Icon-Text Integration

**Inline Icons (行内图标):**
```
⚔️ Deal 2 damage → icon left-aligned with text
🛡️ Block 1 → icon + number + action
Cost: 3⚡ → text + icon
```

**Badge Icons (徽章图标):**
```
┌─────┐
│  +3 │ → Circle or rounded rectangle
│  ⭐ │    background with icon
└─────┘
```

**Section Markers (章节标记):**
```
┌─────────────────┐
│ ⚔️ COMBAT       │ → Icon + divider line
├─────────────────┤
│ Text...         │
└─────────────────┘
```

## Card Back Design (卡牌背面设计)

### Alignment Criticality

**Why Alignment Matters:**
- Players can see card backs during shuffling
- Misaligned backs reveal card types (unfair advantage)
- Tournament play requires perfect alignment

**Alignment Tolerances:**
```
Center point: ±0.5mm
Rotation: <0.3°
Pattern repeat: ±0.2mm
Color matching: ΔE < 2 (imperceptible)
```

### Back Pattern Types

**1. Uniform Pattern (统一图案)**
- All cards share identical back
- Most common approach
- Prevents card identification

**2. Deck Differentiation (牌堆区分)**
- Different decks have different backs
- Common in games with multiple decks
- Must be clearly distinct

**3. Type Coding (类型编码 - controversial)**
- Different card types have different backs
- Some players consider this cheating
- Generally not recommended

### Back Design Elements

```
Recommended Back Structure:
┌──────────────────────────────┐
│                              │
│      [Game Logo/Title]       │ ← Centered, prominent
│                              │
│   [Pattern/Artwork Border]    │ ← Outer frame
│                              │
└──────────────────────────────┘

Key Principles:
- Center: Main logo or title
- Border: Repeating pattern or frame
- Avoid: Edge-only designs (misalignment visible)
- Test: Print proof and stack shuffle test
```

## Sheet Imposition (整版排版)

### A4 Layout Calculator

**Poker Size Cards (63×88mm):**

| Layout | Cards | Sheet Usage | Efficiency |
|--------|-------|-------------|------------|
| 2×7 | 14 | 210×297mm | 95% |
| 3×5 | 15 | 210×297mm | 98% (tight) |
| 4×4 | 16 | 210×297mm | 92% (mini cards) |

**Standard Layout (2×7 = 14 cards):**
```
┌────────────────────────────────────────┐
│ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ │
│ │ 1  │ │ 2  │ │ 3  │ │ 4  │ │ 5  │ │ 6  │ │ 7  │ │ ← Row 1
│ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ │
│ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ │
│ │ 8  │ │ 9  │ │10  │ │11  │ │12  │ │13  │ │14  │ │ ← Row 2
│ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ │
└────────────────────────────────────────┘

Dimensions:
Card: 63×88mm
Gutter: 3-5mm between cards
Bleed: 3mm on all sides
```

### Back Alignment Strategy

**Front/Back Registration (正背对齐):**

```
Front Sheet:          Back Sheet (rotated 180°):
┌────┐ ┌────┐        ┌────┐ ┌────┐
│ 1  │ │ 2  │        │ 2' │ │ 1' │ ← Rotated 180°
└────┘ └────┘        └────┘ └────┘

Why 180° rotation:
- Ensures perfect front/back alignment
- Compensates for sheet registration errors
- Standard industry practice
```

### Cutting and Bleed

**Bleed Requirements:**
- Add 3mm bleed on all sides
- Poker card with bleed: 69×94mm
- Critical content within safe zone: 3mm from trim

**Corner Radius:**
- Standard: 3-4mm radius
- Create corner die line
- Must match on front and back

## Readability Standards (可读性标准)

### Contrast Requirements

**WCAG AA Compliance (Web Content Accessibility Guidelines):**

| Element | Minimum Ratio | Recommended |
|---------|---------------|-------------|
| Body text | 4.5:1 | 7:1 or higher |
| Large text (18pt+) | 3:1 | 4.5:1 or higher |
| Icons/Graphics | 3:1 | 4.5:1 or higher |

**Testing:**
- Use WebAIM Contrast Checker
- Test in low light (café environment)
- Test with older players (presbyopia)

### Color Blindness Safety

**Dangerous Combinations:**

| Combination | Issue | Alternative |
|-------------|-------|-------------|
| Red vs Green | Protanopia/Deuteranopia | Red vs Blue |
| Red vs Brown | Protanopia | Yellow vs Purple |
| Green vs Brown | Deuteranopia | Blue vs Orange |
| Light Gray vs Light Blue | Low contrast | Darker values |

**Safe Combinations:**
- Red vs Blue
- Yellow vs Purple
- Orange vs Blue
- Always add icons/text as backup

**Testing Tools:**
- Sim Daltonism (macOS)
- Color Oracle (Windows/Linux/macOS)
- Coblis (online simulator)

### Font Selection Guidelines

**Print-Optimized Font Characteristics:**
- Clear terminals (not overly condensed)
- Distinguishable characters (1 vs l vs I, 0 vs O)
- Adequate x-height (readability)
- Multiple weights available

**Recommended Font Families:**
- **Sans-serif**: Source Sans Pro, Open Sans, Roboto, Inter
- **Serif**: Source Serif Pro, Merriweather, Georgia
- **Display**: Montserrat, Oswald, Bebas Neue (headers only)

**Avoid:**
- Web-only fonts (may not print well)
- System fonts (Arial, Times - overused)
- Overly decorative fonts (hard to read)
- Fonts with limited weight options

## Production Workflow (制作流程)

### Phase 1: Template Setup

```
1. Create card template file
   ├─ Set dimensions (63×88mm + 3mm bleed)
   ├─ Add guides (safe zone, trim, bleed)
   ├─ Create corner radius die line
   └─ Set up layers (background, art, text, overlay)

2. Define styles
   ├─ Typography scale
   ├─ Color swatches (CMYK)
   ├─ Icon library
   └─ Paragraph/character styles
```

### Phase 2: Card Design

```
1. Layout design
   ├─ Place artwork in visual zone
   ├─ Add title header
   ├─ Set body text
   └─ Add icons and badges

2. Hierarchy check
   ├─ Is title most prominent?
   ├─ Is body text readable?
   ├─ Do icons support understanding?
   └─ Is visual flow logical?

3. Accessibility check
   ├─ Contrast ≥ 4.5:1
   ├─ Color blind safe
   ├─ Font size ≥ 7pt (poker)
   └─ Test at 50-80cm distance
```

### Phase 3: Sheet Imposition

```
1. Create imposition sheet
   ├─ Set up A4 canvas
   ├─ Place cards in grid (2×7 for poker)
   ├─ Add 3-5mm gutters between cards
   └─ Add crop marks

2. Back alignment
   ├─ Rotate back sheet 180°
   ├─ Ensure perfect front/back registration
   └─ Test with proof print

3. Die lines
   ├─ Create separate die line layer
   ├─ Export as DXF or PDF
   └─ Include corner radius
```

### Phase 4: Export

```
1. Front faces export
   ├─ File: cards-front.pdf
   ├─ Mode: CMYK
   ├─ Resolution: 300 DPI
   ├─ Bleed: 3mm all sides
   ├─ Text: Convert to outlines
   └─ Standard: PDF/X-1a or PDF/X-4

2. Back faces export
   ├─ File: cards-back.pdf
   ├─ Same specs as front
   └─ Verify 180° rotation alignment

3. Die lines export
   ├─ File: cards-dielines.pdf or .dxf
   ├─ Vector format required
   └─ Include registration marks
```

### Phase 5: Proof and Test

```
1. Digital proof
   ├─ Check color conversion
   ├─ Verify text (typos, overflow)
   ├─ Check image resolution
   └─ Verify bleed and crop marks

2. Hard proof (if budget allows)
   ├─ Print test sheet
   ├─ Check color accuracy
   ├─ Verify front/back alignment
   ├─ Test corner radius
   └─ Shuffle test for backs

3. Play test
   ├─ Sleeve cards (if applicable)
   ├─ Test handling and shuffling
   ├─ Check readability during play
   ├─ Verify icon recognition
   └─ Test with multiple lighting conditions
```

## Common Mistakes (常见错误)

| Mistake | Consequence | Solution |
|---------|-------------|----------|
| **Text too small** | Unreadable, players squinting | Body ≥7pt @ poker size, test at 60cm |
| **Poor contrast** | Hard to read, especially low light | WCAG AA 4.5:1 minimum |
| **No bleed** | White edges when cut | Add 3mm bleed on all sides |
| **Back misalignment** | Players see card types | Strict 180° rotation, proof test |
| **Icons too detailed** | Unrecognizable at small size | Test at 4mm, simplify |
| **Too much text** | Overwhelming, slow gameplay | Edit ruthlessly, use icons |
| **Red/green coding** | Color blind players excluded | Use multiple cues (color + icon + text) |
| **Inconsistent style** | Confusing, unprofessional | Create style guide first |
| **Wrong color mode** | Color shift, dull prints | Design in CMYK from start |
| **Font not embedded** | Missing font warning | Convert to outlines before export |

## Card Type Templates (卡牌类型模板)

### Action/Event Card Template

```
┌──────────────────────────────┐
│ ⚡    SURGE                  │ ← Large icon + title
│                              │
│   [Lightning bolt artwork]    │ ← Simple, bold art
│                              │
│ Draw 2 cards.                │ ← Clear effect
│ ⚡ If you have an Energy card,│ ← Icon-text integration
│   draw +1 card.               │
└──────────────────────────────┘
```

### Resource Card Template

```
┌──────────────────────────────┐
│                              │
│      ⚔️  SWORD  ⚔️          │ ← Large icon + label
│                              │
│      Combat Resource         │
│                              │
│      Value: 3                │ ← Clear value
│                              │
└──────────────────────────────┘
```

### Character/Unit Card Template

```
┌──────────────────────────────┐
│ ⭐  WARRIOR        ATK 3     │ ← Name + stat badge
│                              │
│                              │
│    [Character portrait]       │ ← Large art
│                              │
│ ⚔️ 2 ATK                     │ ← Abilities
│ 🛡️ 2 DEF                     │   with icons
│                              │
│ "Frontline fighter"          │ ← Flavor text
└──────────────────────────────┘
```

## Quick Reference Card (快速参考卡)

### Pre-Press Checklist

```
Design:
□ Final dimensions set (with 3mm bleed)
□ CMYK mode
□ 300 DPI @ final size
□ Text converted to outlines
□ All images embedded

Layout:
□ Safe zone maintained (3mm from edge)
□ Hierarchy clear
□ Icons consistent
□ Typography correct

Imposition:
□ Card count verified
□ Gutters adequate (3-5mm)
□ Crop marks added
□ Front/back alignment checked

Accessibility:
□ Contrast ≥ 4.5:1
□ Color blind tested
□ Font size adequate
□ Readability tested

Export:
□ PDF/X-1a or PDF/X-4
□ Separate front/back files
□ Die line file created
□ File size < 2GB
```

### Standard Sheet Sizes

| Sheet | Cards (Poker) | Cards (Mini) | Efficiency |
|-------|---------------|--------------|------------|
| A4 | 14 (2×7) | 20-24 | 95% |
| A3 | 28-30 (2×15) | 40-48 | 95% |
| Letter | 12-14 | 18-20 | 90% |

### Common Card Quantities

| Game Type | Card Count | Sheets (A4) | Notes |
|-----------|------------|-------------|-------|
| Small game | 36-54 | 3-4 | Mini cards common |
| Medium game | 72-108 | 5-8 | Poker size typical |
| Large game | 150+ | 11+ | Consider mini cards |
| CCG/LCG | 200-400+ | 15-29 | Usually poker size |

## References

- **Parent skill**: print-design
- **Related skills**: boardgame-tiles, boardgame-boards, boardgame-components
- **References**: `print-design/references/boardgame-specs.md`
- **Icon resources**: boardgame-icons.com, Noun Project
- **Print specs**: `print-design/references/print-specs.md`

---

**Version**: 1.0.0
**Last Updated**: 2025-01-23
**Card Size Reference**: Poker (63×88mm) unless otherwise specified
