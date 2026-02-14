# Templates & Checklists

## Edge Case Enumeration Template

For mechanics, rules, or systems, complete:

| Scenario | Expected Behavior | Implemented? | Notes |
|----------|-------------------|--------------|-------|
| At minimum player count | | | |
| At maximum player count | | | |
| With empty draw deck | | | |
| At zero resources | | | |
| At maximum resources/cap | | | |
| During final round | | | |
| When multiple effects trigger | | | |
| With conflicting card text | | | |
| During setup errors | | | |
| With missing/damaged components | | | |
| Tied scores | | | |
| First player advantage | | | |

---

## Extended Debugging Protocol

When told "it feels wrong/boring/clunky/unbalanced," diagnose in order:

| Symptom | Check First | Before Tuning Numbers |
|---------|-------------|----------------------|
| "I don't understand the rules" | Clarity | Rewrite rulebook section, add examples, clarify terminology |
| "I don't care what happens" | Strategy | Connect decisions to long-term goals, increase stakes |
| "I'm just doing my own thing" | Interaction | Add trading, conflict, shared resources |
| "Winning feels empty" | Satisfaction | Add visual/tactile feedback, make progress visible |
| "The theme doesn't match" | Fit | Rename components, adjust art, modify mechanics |
| "This takes forever to set up" | Components | Reduce component count, improve storage |
| "I'm bored during others' turns" | Interaction/Downtime | Add reactive mechanics, reduce turn length |

**Rule:** Do not tune card costs/scoring values until Clarity and Strategy are verified as not the root cause.

---

## Playtest Script Template

### 1. New Player Test (Rules Learnability)
- **Setup:** New player(s), rulebook only, no prior teaching
- **Task:** Set up and play a complete game using only the rulebook
- **Pass:** Players complete the game without major rules errors OR identify where confusion occurred
- **Observe:** What questions do they ask? Where do they get stuck? How long to learn?
- **Metrics:**
  - Time to setup correctly: _____
  - Rules questions during play: _____
  - Major rules errors: _____

### 2. Rules Reference Test
- **Setup:** Ongoing game, questions arise
- **Task:** Find answers in rulebook within 30 seconds
- **Pass:** Players can locate answers without designer help
- **Observe:** What sections are hard to find? What terms are unclear?
- **Metrics:**
  - Average time to find answer: _____
  - Answers found without help: _____%

### 3. Player Count Test
- **Player Count:** [2 / 3 / 4 / 5 / 6] players
- **Focus:** Downtime, interaction, game length, balance
- **Pass:** Game feels complete and balanced at this count
- **Observe:** How long are turns? Do players engage with each other?
- **Metrics:**
  - Average turn length: _____
  - Average downtime between turns: _____
  - Total play time: _____
  - Would you play again at this count? Yes/No

### 4. Strategy Test
- **Setup:** Mix of experienced and new players
- **Task:** Play 5+ games and track win rates by player experience
- **Pass:** Skilled players win significantly more than chance
- **Observe:** What strategies emerge? Is there a dominant path?
- **Metrics:**
  - Experienced player win rate: _____%
  - Different strategies used: _____
  - Close games (final score within 10%): _____%

### 5. Balance Test
- **Setup:** 10+ games with random starting positions/factions
- **Task:** Track win rates by starting position
- **Pass:** All positions win within 40-60% range
- **Observe:** Does any starting position feel over/underpowered?
- **Metrics:**
  - Win rate by position: _____
  - Ban/avoid rate by position: _____%

### 6. Downtime Test
- **Setup:** 4+ players, timing each turn
- **Task:** Measure engagement between turns
- **Pass:** Players remain attentive during others' turns
- **Observe:** What do players do when it's not their turn?
- **Metrics:**
  - Turn length: _____
  - Downtime between meaningful actions: _____
  - Attention lost (on phone, distracted): _____ times/game

### 7. Blind Playtest (Final Validation)
- **Setup:** New players, rulebook only, no designer present
- **Task:** Complete game and fill out feedback form
- **Pass:** Game works without any designer intervention
- **Observe:** What confused them? What did they enjoy/hate?
- **Feedback Questions:**
  1. What was confusing about the rules?
  2. What was the most/least fun part?
  3. Would you play again? Why/why not?
  4. What would you change?
  5. Score the game 1-10: _____

---

## Game Proposal Template

```markdown
## Game: [Name]

### Player Experience Goal
What should players feel when playing? (e.g., tense, clever, cooperative, frantic)

### Overview
- Player Count: [min-max]
- Play Time: [minutes]
- Age: [recommended]
- Complexity: [light/medium/heavy]

### Core Mechanics
List the main systems: [e.g., worker placement, deck building, area control]

### 5-Component Evaluation

| Component | Rating (1-5) | Notes |
|-----------|--------------|-------|
| Clarity | | |
| Strategy | | |
| Interaction | | |
| Satisfaction | | |
| Fit | | |

### Game Flow
1. Setup
2. Turn structure
3. Endgame trigger
4. Scoring

### Components List
| Component | Quantity | Notes |
|-----------|----------|-------|
| | | |

### Risks & Concerns
- Potential balance issues:
- Rules complexity concerns:
- Component production challenges:

### Playtest Results
| Date | Players | Count | Key Feedback | Changes Made |
|------|---------|-------|--------------|--------------|
| | | | | |

### Next Steps
1.
2.
3.
```

---

## Rulebook Template

```markdown
# [GAME NAME] Rulebook

## Contents
- Overview
- Components
- Setup
- Gameplay
- End of Game
- Appendix

## Overview
[2-3 sentences describing the game]
- **Players:** X-Y
- **Time:** Z minutes
- **Age:** A+
- **Author:** Your Name

## Objective
[How to win in 1-2 sentences]

## Components
[List with illustrated quantities]

## Setup
[Step-by-step setup with diagrams]

## Gameplay Overview
[One-page turn structure reference]

## Detailed Rules
### Turn Structure
1. Phase One
2. Phase Two
3. Phase Three

### Key Mechanics
#### Mechanic Name
[Explanation with example]

## End of Game
[Trigger and final scoring]

## FAQ
[Common questions]

## Glossary
[All game terms defined]
```

---

## Card/Component Text Template

```markdown
[Card Title] - [Type]

[COST/STATS]

[Effect Text]

[Flavor Text]
```

### Card Writing Guidelines
1. **Use keywords:** Define complex abilities as keywords
2. **Timing is everything:** Specify when effects trigger
3. **Be precise:** Avoid ambiguous words like "may" unless intentional
4. **Use standard template:** Cost → Effect → Timing → Duration
5. **Test edge cases:** What happens with multiple copies? With empty board?

---

## State Machine Documentation Template

```markdown
## Game State: [Name]

### Entry Conditions
- From [State A]: when [condition]
- From [State B]: when [condition]
- NOT from: [forbidden states]

### Exit Conditions
- To [State A]: when [condition]
- To [State B]: when [condition]
- Trigger: [automatic / player action / external event]

### During State
- Players can: [list allowed actions]
- Players cannot: [list forbidden actions]
- What happens: [state behavior]

### Resource Interaction
- On entry: [resources gained/lost]
- During state: [ongoing effects]
- On exit: [cleanup/transition]

### Edge Cases
| Condition | Behavior |
|-----------|----------|
| Multiple players enter | |
| State interrupted | |
| State overlaps with | |
| At minimum/maximum players | |
```

---

## Balance Tracking Template

```markdown
## Balance Test: [Date]

### Players
[Name, experience level, starting position]

### Game Flow
| Turn | Player | Key Action | Score/Resources |
|------|--------|------------|-----------------|
| 1 | | | |
| 2 | | | |

### Final Scores
| Player | Starting Position | Final Score | Notes |
|--------|------------------|-------------|-------|
| | | | |

### Observations
- What worked well:
- What felt unbalanced:
- Dominant strategies observed:
- Player interaction level:
- Downtime experienced:

### Changes to Make
1.
2.
3.
```

---

## Post-Playtest Feedback Form

Give this to playtesters after the game:

```markdown
## [GAME NAME] Feedback

### About You
- How many times have you played this game? _____
- Your experience level: [New / Casual / Hobbyist / Expert]

### Rules & Learning
1. Were the rules clear? [Yes/No/Somewhat]
2. What was confusing?
3. How long did it take to learn? _____

### Gameplay
4. What was your favorite part?
5. What was your least favorite part?
6. Did you feel you had meaningful choices? [Yes/No/Somewhat]
7. How was the downtime between your turns? [Too long / Fine / Didn't notice]
8. Did the game feel balanced? [Yes/No/Somewhat]
9. Did the theme match the mechanics? [Yes/No/Somewhat]

### Experience
10. What emotion did you feel while playing?
11. Would you play again? [Yes/No/Maybe]
12. Would you recommend this game? [Yes/No/Maybe]
13. What would you change?

### Additional Comments

Thank you for playtesting!
```

---

## Iteration Log Template

Track changes across playtest versions:

```markdown
## Version History

### v1.0 - [Date]
**Changes:** Initial prototype
**Playtested by:** [names]
**Feedback:**
**Next changes:**

### v1.1 - [Date]
**Changes:**
**Playtested by:** [names]
**Feedback:**
**Next changes:**

### v1.2 - [Date]
**Changes:**
**Playtested by:** [names]
**Feedback:**
**Next changes:**
```

---

## Final Checklist

Before declaring a game "done," verify:

### Rules Documentation
- [ ] Rulebook is clear and consistent
- [ ] All terms defined in glossary
- [ ] Examples provided for complex mechanics
- [ ] FAQ covers common questions
- [ ] Component list is accurate

### Component Design
- [ ] All components accounted for
- [ ] Icons are clear and consistent
- [ ] Text is readable at playing distance
- [ ] Colorblind-friendly where possible
- [ ] Components fit in planned box/packaging

### Balance Testing
- [ ] Tested at minimum player count
- [ ] Tested at maximum player count
- [ ] Tested at recommended player count
- [ ] 20+ total playtests completed
- [ ] Win rates tracked for all starting positions
- [ ] No dominant strategy identified

### Player Experience
- [ ] Player experience goal is achieved
- [ ] Game length matches target
- [ ] Setup time is reasonable
- [ ] Downtime is acceptable
- [ ] Endgame is satisfying

### Production Ready
- [ ] Component costs calculated
- [ ] Box size determined
- [ ] Rulebook layout done
- [ ] Art direction complete
- [ ] Prototype for publisher/playtest ready

**The game is done when:** Further changes don't improve the player experience, and playtesters request to play again.
