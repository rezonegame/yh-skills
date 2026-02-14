# Game Iteration Tracker

A companion system for `boardgame-design` skill that enables iterative playtesting with automatic change tracking.

---

## How to Use This System

### Setup

1. Create a folder for your game: `C:\Users\wudao\BoardGameProjects\[GameName]\`
2. Copy this file as `ITERATION_LOG.md`
3. Create `CHANGELOG.md` for version history
4. After each playtest, update the log

### The Iteration Workflow

```
Playtest → Record Results → Ask Claude for Analysis → Implement Changes → Repeat
```

---

## Iteration Log Template

Copy this section for each playtest:

```markdown
## Playtest Session #[Number]

**Date:** YYYY-MM-DD
**Version:** vX.X.X
**Players:** [Count, names/experience levels]
**Player Count:** [2/3/4/5]
**Testing Focus:** [What we're testing this session]

### Pre-Playtest Notes
- Previous changes made:
- Specific questions to answer:
- Concerns to watch for:

### Session Results

#### What Happened
[Brief summary of how the game played]

#### Observations
| Time | Event | Observation |
|------|-------|-------------|
| | | |

#### Body Language Notes
- Engagement level: High/Medium/Low
- Confusion moments:
- Excitement moments:
- Frustration points:

### Feedback Summary

#### Most Fun Part:
#### Least Fun Part:
#### 5% Improvement (Magic Question):
#### Agency/Choices: Did players feel they had meaningful decisions?
#### Would Play Again: Yes/No/Maybe

### Quantitative Metrics
- Game length: ___ minutes (target: ___)
- Rules questions: ___ (target: <3)
- Analysis paralysis incidents: ___
- Winner: [Starting position if asymmetric]

### Identified Issues

| Priority | Issue | Category | Affected Component |
|----------|-------|----------|-------------------|
| High | | | |
| Medium | | | |
| Low | | | |

**Categories:** Clarity / Strategy / Interaction / Satisfaction / Fit

### Analysis

#### Root Cause (5 Whys)
1. What's the problem?
2. Why?
3. Why?
4. Why?
5. Why? (Root cause)

#### What This Tells Us
[What the feedback and observations reveal about the game]

### Changes for Next Version

#### Change 1
- **What:** [Description of change]
- **Why:** [How it addresses the root cause]
- **Expected Impact:** [What should improve]
- **Revert Difficulty:** Easy/Medium/Hard

#### Change 2
- **What:**
- **Why:**
- **Expected Impact:**
- **Revert Difficulty:**

### What We're NOT Changing (and Why)
- [Thing]: [Why we're keeping it despite feedback]
- [Thing]: [Reason]

### Next Playtest Goals
1.
2.
3.

### Next Version
**From:** vX.X.X
**To:** vX.X.X
**Changes:** [Brief summary]
```

---

## Claude Prompt Template

After each playtest, use this prompt to get iteration suggestions:

```
I'm using the boardgame-design skill. I just completed a playtest session for my game. Here are the results:

[Playtest Session Summary - paste from above]

Based on the boardgame-design framework, please:
1. Analyze the feedback using the 5-Component Filter
2. Identify the root cause using the 5-Whys technique
3. Suggest specific changes following the Single-Change Rule
4. Prioritize changes using the Change Impact Matrix
5. Tell me what the next version should be (semantic versioning)

Also check the feedback against:
- Player Experience First principles
- Psychology of Choice (loss aversion, endowment effect, etc.)
- Common iteration traps
```

---

## Change Log Template

```markdown
# Change Log

All notable changes to [Game Name] will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- [New feature]

### Changed
- [Changed thing]

### Removed
- [Removed thing]

### Fixed
- [Bug fix]

---

## [0.5.0] - 2024-01-15

### Added
- New "Trade" action
- Setup diagram to rulebook

### Changed
- Turn order from fixed to progressive
- Starting resources from 5 to 6
- Clarified wording on "scoring" section

### Removed
- "Lucky" card (too confusing)

### Fixed
- Typo in setup instructions
- Ambiguous timing for "End of Round" effects

### Playtested
- 4 games with 3 different groups
- All groups reported clearer rules
- Trade action well-received

### Known Issues
- Balance still needs work at 5 players
- Endgame sometimes feels abrupt

---

## [0.4.0] - 2024-01-08
[etc...]
```

---

## Quick Reference: Version Number Decisions

```
Should I increment:
- MAJOR (X.0.0)? Complete overhaul, nearly a different game
- MINOR (0.X.0)? Significant new mechanic or rule change
- PATCH (0.0.X)? Small numbers tweak, wording clarification
```

---

## The "Ask Claude" Prompts by Situation

### When Feedback is Conflicting

```
I received conflicting feedback from my playtesters:

[Quote conflicting feedback]

Using the boardgame-design framework:
1. Help me categorize this feedback (Surface/Balance/Systemic/Experience)
2. Filter by source credibility and frequency
3. Determine which feedback aligns with my game's vision
4. What should I actually change?
```

### When You Don't Know What to Change

```
My playtest revealed this issue:

[Describe the issue]

Using the boardgame-design framework:
1. Apply the 5-Whys technique to find the root cause
2. Suggest ONE change (Single-Change Rule) that addresses it
3. Tell me the expected impact and revert difficulty
4. What should I test in the next playtest?
```

### When Testing a Specific Mechanic

```
I'm testing this mechanic:

[Describe mechanic]

Using the boardgame-design framework and mechanics encyclopedia:
1. What category does this belong in?
2. What are common pitfalls with this type of mechanic?
3. What specific questions should I ask playtesters?
4. What metrics should I track?
```

### When You Think You're Done

```
I think my game might be done. Here's the status:

[Check off items from Definition of Done]

Using the boardgame-design framework:
1. Have I met all the done criteria?
2. Am I falling into any iteration traps?
3. Am I at the point of diminishing returns?
4. Should I publish or keep iterating?
```

---

## Tracking Folder Structure

```
[GameName]/
├── ITERATION_LOG.md          # This file - detailed playtest logs
├── CHANGELOG.md              # Version history
├── RULEBOOK_vX.X.X.md        # Current rules
├── RULEBOOK_DRAFT.md         # Work-in-progress rules
├── FEEDBACK/                 # Raw feedback forms
│   ├── playtest_001.pdf
│   ├── playtest_002.pdf
│   └── ...
├── PROTOTYPES/               # Component files
│   ├── cards_vX.X.X.pdf
│   ├── board_vX.X.X.pdf
│   └── ...
└── ANALYSIS/                 # Claude's analysis outputs
    ├── session_001_analysis.md
    ├── session_002_analysis.md
    └── ...
```

---

## Example: First Playtest

```markdown
## Playtest Session #1

**Date:** 2024-01-15
**Version:** v0.1.0
**Players:** 3 (2 experienced gamers, 1 casual)
**Player Count:** 3
**Testing Focus:** Core game loop - is it fun?

### Pre-Playtest Notes
- This is our first real playtest
- Using hand-drawn components
- Main question: Is there a fun game here?

### Session Results

#### What Happened
Game took 75 minutes. Players picked up rules quickly but got confused
by the "scoring" phase. Winner was Player 2 (starting player).

#### Observations
| Time | Event | Observation |
|------|-------|-------------|
| 0:15 | Rules explanation | Took 10 minutes, seemed clear |
| 0:30 | First round | Players unsure what to do |
| 0:45 | Mid-game | Engagement picked up |
| 1:10 | End game | Confusion about final scoring |

#### Body Language Notes
- Engagement level: Medium (improved as game progressed)
- Confusion moments: Scoring phase, card interactions
- Excitement moments: When a clever combo was discovered
- Frustration points: Not understanding card synergy

### Feedback Summary

#### Most Fun Part:
"Discovering how cards combo together"

#### Least Fun Part:
"The final scoring - I didn't understand what was happening"

#### 5% Improvement:
"Make it clearer how cards score"

#### Agency/Choices:
Yes - players felt they had meaningful decisions

#### Would Play Again:
All 3 said yes

### Identified Issues

| Priority | Issue | Category | Component |
|----------|-------|----------|-----------|
| High | Scoring rules unclear | Clarity | Rulebook |
| Medium | First player advantage | Strategy | Turn order |
| Low | Card text hard to read | Clarity | Components |

### Analysis

#### Root Cause (5 Whys)
1. Scoring was confusing
2. Rules were on page 7, not referenced during game
3. No scoring example provided
4. Scoring happens all at once
5. **Root:** Scoring phase needs better visibility and examples

#### What This Tells Us
Core gameplay is working (engagement improved, choices felt meaningful).
Main issue is Clarity around scoring. First player advantage needs
more data to confirm.

### Changes for Next Version

#### Change 1
- **What:** Add scoring example to rulebook and quick reference card
- **Why:** Addresses root cause - players couldn't see scoring during game
- **Expected Impact:** Less confusion, faster scoring phase
- **Revert Difficulty:** Easy

#### Change 2
- **What:** Track starting positions more carefully
- **Why:** Need data on first player advantage before making changes
- **Expected Impact:** Better information for balance decisions
- **Revert Difficulty:** N/A (just tracking)

### What We're NOT Changing
- Core card combo mechanic: Players loved it
- Game length: 75 min is acceptable for this weight

### Next Playtest Goals
1. Verify scoring is clearer
2. Watch for first player advantage patterns
3. Test at 4 players

### Next Version
**From:** v0.1.0
**To:** v0.1.1 (PATCH - wording clarification)
**Changes:** Added scoring example and quick reference card
```

---

## Remember

**Each playtest should answer ONE specific question.** Don't try to test everything at once.

**Use Claude as your iteration partner.** After each playtest, share the results and get targeted analysis based on the boardgame-design framework.

**Version control is your friend.** Keep track of what changed and why. When something doesn't work, you can always revert.
