# Domain-Specific Design Guide

## Rules Writing & Documentation

**Core question:** Can players learn and play the game without the designer?

### Rulebook Structure (Mandatory Sections)

| Section | Purpose | Best Practice |
|---------|---------|---------------|
| **Overview** | Set expectations | Play time, player count, age, complexity level |
| **Components** | What's in the box | Illustrated list with quantities |
| **Setup** | How to start | Step-by-step with diagrams |
| **Objective** | How to win | Clear victory conditions |
| **Turn Structure** | What to do on your turn | One-page reference |
| **Detailed Rules** | The meat of the game | Organized by topic, not chronology |
| **Edge Cases** | What if... | FAQ section for common questions |
| **Examples** | See it in action | At least one illustrated example per major mechanic |

### Terminology Rules

1. **One term, one meaning** - Never use the same word for different concepts
2. **One concept, one term** - Never use different words for the same concept
3. **Consistent capitalization** - Capitalize all game terms for easy identification
4. **Glossary** - Define every game term in one place
5. **Keywords** - Use bold for keywords, define on first use

### Writing Guidelines

- **Active voice:** "Draw 3 cards" not "3 cards are drawn"
- **Imperative mood:** "Place your worker" not "You should place your worker"
- **Step numbering:** Use numbered lists for sequences, bullets for options
- **Page references:** Always include page numbers for cross-references
- **Visual hierarchy:** Use headings, bold, and boxes to organize information

**Acceptance Test:** Can a new player set up and play the game correctly using only the rulebook?

---

## Game Pacing & Timing

**Core question:** How does the game flow from start to finish?

### Time Budgeting

| Phase | Target % of Total Time | Considerations |
|-------|------------------------|----------------|
| Setup | ≤10% | Minimize component sorting, use organized storage |
| Early game | 20-30% | Players learning mechanics, building foundations |
| Mid game | 40-50% | Main strategic decisions, competition heats up |
| End game | 10-20% | Race to finish, final scoring |

### Turn Structure Pacing

| Player Count | Turn Length | Downtime | Total Play Time |
|--------------|-------------|----------|-----------------|
| 2 players | 2-5 min | Minimal | 30-60 min |
| 3-4 players | 1-3 min | Acceptable | 45-90 min |
| 5+ players | ≤2 min | Critical | 60-120 min |

**Downtime Management Strategies:**
- Simultaneous action selection
- Reactive triggers during others' turns
- Planning phase during others' turns
- Quick actions with limited options

### Endgame Triggers

Choose ONE primary trigger:
- **Time-based:** Fixed number of rounds
- **Progress-based:** Someone reaches a threshold
- **Resource-exhaustion:** Deck runs out, certain components depleted
- **Achievement-based:** Specific goal accomplished

**Avoid:** Multiple competing endgame triggers that create confusion.

---

## Balance Systems

**Core question:** Is the game fair while allowing skill to matter?

### Types of Balance

| Balance Type | Description | Evaluation Method |
|--------------|-------------|-------------------|
| **Starting balance** | All players have equal starting positions | Symmetric setups OR tested asymmetric starts |
| **Strategic balance** | No dominant strategy | Playtest to identify optimal paths |
| **Progression balance** | Early advantages don't guarantee victory | Catch-up mechanisms, snowball prevention |
| **Player count balance** | Game works at all advertised player counts | Test at min, max, and recommended counts |

### Asymmetric Design

When players start with different abilities/positions:

| Requirement | Test Method |
|-------------|-------------|
| Win rate equity | 20+ games with random positions/abilities |
| Skill expression | Skilled players should win regardless of position |
| Fun equity | All positions/abilities should feel satisfying to play |
| Counterplay | No position should feel helpless against another |

### Economy Balancing

For games with resources, currency, or VP:

1. **Define the economy:** What flows in and out?
2. **Starting values:** Give everyone the same baseline
3. **Growth rate:** How fast can players generate resources?
4. **Constraints:** What limits economy growth?
5. **Variance:** What random elements affect the economy?

**Testing approach:** Track resource generation per turn across multiple playtests. Look for runaway leaders or stagnant economies.

---

## Player Interaction Design

**Core question:** How do players affect each other?

### Interaction Spectrum

| Type | Description | Examples | Pros | Cons |
|------|-------------|----------|------|------|
| **None** | Multiplayer solitaire | Splendor (base) | Low conflict, accessible | Can feel boring |
| **Indirect** | Race for same goals | Ticket to Ride | Tension without direct conflict | Limited engagement |
| **Market** | Trading/auctioning | Catan, Modern Art | High engagement, negotiation | Can drag on |
| **Direct Conflict** | Attack/take-that | Risk, Munchkin | Exciting, emotional | Can feel unfair |
| **Cooperation** | Win or lose together | Pandemic | Shared experience | Quarterbacking problem |

### Interaction Best Practices

- **Visible impact:** Players should see how they affect each other
- **Defensive options:** Give players ways to protect themselves
- **Timing:** Allow reaction to others' actions when possible
- **Proportionality:** Interactions should match the game's tone
- **Recovery:** Players should be able to recover from setbacks

**Acceptance Test:** At any point in the game, can each player name one way they're affected by or affecting another player?

---

## Component Design

**Core question:** Do the components serve the gameplay?

### Component Readability

| Component | Clarity Requirements |
|-----------|---------------------|
| **Cards** | Title, type, cost/power, effect text, art/icons all distinct |
| **Boards** | Clear spaces, intuitive layout, visible tracks/scores |
| **Tokens/Resources** | Distinct shapes/colors, tactile feedback, stackable |
| **Dice** | Readable symbols, color-coded if multiple types |
| **Meeples/Minis** | Fit spaces comfortably, stable, distinctive |

### Icon System Design

1. **Keep it simple:** Icons should be recognizable at a glance
2. **Use standards:** Build on existing conventions where possible
3. **Color code:** Combine icons with colors for accessibility
4. **Legend on board:** Don't make players reference the rulebook constantly
5. **Colorblind safe:** Use shapes + colors, not colors alone

### Storage & Setup

| Consideration | Best Practice |
|---------------|----------------|
| Component count | Fewer components = faster setup/teardown |
| Sorting | Group by type or player for quick setup |
| Storage | Include organizers or specify storage solution |
| Setup time | Should be ≤10% of total play time |
| Teardown | Easier than setup (bags help) |

---

## Randomness Management

**Core question:** Does randomness create excitement without undermining skill?

### Randomness Types

| Type | Examples | Skill Expression | Use When |
|------|----------|------------------|----------|
| **Input randomness** | Draw cards, roll dice at start of turn | Reacting to what you get | You want tactical play |
| **Output randomness** | Roll to see if action succeeds | Risk assessment | You want calculated risks |
| **Deck building** | Construct your deck before playing | Strategic deck construction | You want meta-game depth |
| **Hidden information** | Face-down cards, simultaneous selection | Bluffing, reading players | You want psychological play |

### Variance Control

| Problem | Solution |
|---------|----------|
| Too chaotic | Reduce random elements, add mitigation options |
| Too predictable | Add more randomness, increase information hidden |
| Unfair swings | Cap extremes, add catch-up mechanics |
| No impact of skill | Ensure decisions matter more than luck |

### Mitigation Mechanics

Give players tools to manage randomness:

- **Reroll abilities** (once per turn/game)
- **Card draw selection** (draw X, keep Y)
- **Resource conversion** (spend resources to adjust outcomes)
- **Risk/reward choices** (safe option vs. risky option)

**Acceptance Test:** In 10 games, does the less skilled player win more than 30% of the time solely due to luck?

---

## Setup & Teaching Time

**Core question:** Can players get to the fun quickly?

### Time Budgets

| Game Type | Setup Time | Teach Time | Play Time |
|-----------|------------|------------|-----------|
| Filler | ≤5 min | ≤5 min | 15-30 min |
| Medium | 5-10 min | 10-15 min | 45-90 min |
| Heavy | 10-20 min | 15-30 min | 90-180 min |

### Teaching Order

1. **Win condition** - How do you win? (Start with the goal)
2. **Turn structure** - What do you do? (The basic loop)
3. **Key mechanics** - How does it work? (The interesting parts)
4. **Edge cases** - What if... (As they come up, not upfront)

### First-Turn Advantage Testing

Test at least 5 games rotating starting player:
- Track win rate by starting position
- If first player wins >60%, add catch-up for later players
- Common solutions: Extra resources for later players, bid for start

---

## Scalability

**Core question:** How does the game change with player count?

### Player Count Testing Requirements

| Player Count | Required Tests | What to Watch For |
|--------------|----------------|-------------------|
| Minimum (2) | 10+ games | Is it too sparse? Too competitive? |
| Recommended (3-4) | 20+ games | Primary balance target |
| Maximum (5+) | 10+ games | Downtime? Chaos? Analysis paralysis? |

### Scaling Mechanisms

| Approach | How It Works | Best For |
|----------|--------------|----------|
| **Fixed board** | Board doesn't change | Games where area control isn't central |
| **Modular board** | Add/remove sections | Territorial games |
| **Scaled resources** | More/less components per player | Economy games |
| **Dummy player** | AI takes actions when needed | Games that break at low counts |
| **Hybrid turns** | Adjust turns per round | Player interaction games |

**Acceptance Test:** The game should feel like the same experience at all supported player counts.

---

## Core Loop Design

**Core question:** What do players do repeatedly, and why is it fun?

### Loop Structure

1. **Action:** What does the player do? (The verbs)
2. **Decision:** What choices do they make? (The strategy)
3. **Result:** happens immediately? (The feedback)
4. **Progress:** How does this advance them toward winning? (The arc)
5. **Return:** What brings them back to do it again? (The hook)

### Loop Evaluation Questions

- Is the loop clear and understandable?
- Does each loop iteration feel meaningful?
- Does the loop evolve over the course of the game?
- Is the loop satisfying to repeat?
- Does the loop create interesting decisions?

### Example Loops

| Game | Core Loop |
|------|-----------|
| Catan | Roll → Gather → Trade → Build |
| Ticket to Ride | Draw cards → Claim routes → Score tickets |
| Splendor | Take chips → Buy cards → Reserve bonuses → Claim nobles |

---

## Theme & Narrative Integration

**Core question:** Does the game tell its story?

### Integration Levels

| Level | Description | Example |
|-------|-------------|---------|
| **Pasted-on** | Theme could be anything | Abstract games with flavor text |
| **Illustrated** | Art and terminology match theme | Most eurogames |
| **Integrated** | Mechanics emerge from theme | Twilight Struggle |
| **Transformative** | Game creates the experience | Pandemic (panic), Betrayal (dread) |

### Thematic Consistency Checklist

- [ ] Mechanics match what would "really" happen in the theme
- [ ] Component art is consistent in style
- [ ] Terminology fits the setting (not game terms)
- [ ] Victory conditions make narrative sense
- [ ] Player roles are clear from components
- [ ] The game tells a beginning, middle, and end story

---

## Accessibility & Inclusivity

**Core question:** Who can play and enjoy this game?

### Accessibility Baseline

| Aspect | Consideration |
|--------|---------------|
| **Physical** | Component size, dexterity requirements, colorblindness |
| **Cognitive** | Rule complexity, memory requirements, reading level |
| **Sensory** | Visual clarity, audio cues (if any), tactile feedback |
| **Time** | Play length, downtime tolerance |
| **Social** | Conflict tolerance, cooperation requirements, player interaction |

### Inclusivity Best Practices

- **Colorblind-safe:** Use icons + colors, shapes + colors
- **Text size:** Minimum 10pt for rulebook, larger for card text
- **Component size:** No pieces smaller than 10mm (choke hazard for kids)
- **Dexterity:** Minimize fine motor requirements unless intentional
- **Memory:** Make critical information visible on the table
- **Language:** Write rules at 8th-grade reading level or simpler

**Acceptance Test:** Can someone with mild colorblindness, small hands, or no prior gaming experience enjoy the game?
