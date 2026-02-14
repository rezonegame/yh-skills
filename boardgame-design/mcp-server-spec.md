# Board Game Design MCP Server Specification

MCP (Model Context Protocol) 服务器用于游戏设计的自动化测试追踪、平衡性分析和跨游戏比较。

---

## Overview

这个 MCP 服务器为 `boardgame-design` skill 和 `boardgame-designer` Agent 提供持久化存储、数据分析和自动化工具。

### 核心功能

1. **Playtest Data Storage** - 存储和管理测试数据
2. **Balance Analytics** - 经济和策略平衡分析
3. **Cross-Game Comparison** - 多游戏设计模式比较
4. **Evolution Tracking** - 设计进化压力追踪
5. **Fitness Metrics** - 适应度指标计算

---

## MCP Tools

### 1. `store_playtest_data`

存储 playtest 结果到数据库。

```typescript
{
  name: "store_playtest_data",
  description: "Store structured playtest data for later analysis",
  inputSchema: {
    type: "object",
    properties: {
      game_id: { type: "string", description: "Unique game identifier" },
      version: { type: "string", description: "Game version (e.g., v0.1.0)" },
      data: {
        type: "object",
        properties: {
          timestamp: { type: "string" },
          player_count: { type: "number" },
          duration: { type: "number" },
          winner: { type: "string" },
          scores: { type: "array" },
          issues: { type: "array" },
          feedback: { type: "object" }
        }
      }
    },
    required: ["game_id", "version", "data"]
  }
}
```

### 2. `analyze_balance`

分析游戏平衡性。

```typescript
{
  name: "analyze_balance",
  description: "Analyze game balance from stored playtest data",
  inputSchema: {
    type: "object",
    properties: {
      game_id: { type: "string" },
      version: { type: "string" },
      analysis_type: {
        type: "string",
        enum: ["economic", "strategic", "player_count", "all"]
      }
    },
    required: ["game_id", "version"]
  }
}
```

**返回示例：**
```json
{
  "economic": {
    "growth_rate": "12%",
    "scarcity_curve": "75%",
    "waste_ratio": "8%",
    "snowball_effect": "15%",
    "status": "HEALTHY"
  },
  "strategic": {
    "viable_strategies": 4,
    "win_rates": [52, 48, 51, 49],
    "dominant_strategy": null,
    "status": "BALANCED"
  },
  "player_count": {
    "2p": { rating: 3.5, recommended: true },
    "3p": { rating: 4.8, recommended: true },
    "4p": { rating: 3.2, recommended: false }
  }
}
```

### 3. `track_evolution`

追踪设计进化历史。

```typescript
{
  name: "track_evolution",
  description: "Track design evolution and fitness over iterations",
  inputSchema: {
    type: "object",
    properties: {
      game_id: { type: "string" },
      metrics: {
        type: "object",
        properties: {
          clarity_score: { type: "number" },
          strategy_score: { type: "number" },
          interaction_score: { type: "number" },
          balance_score: { type: "number" }
        }
      }
    },
    required: ["game_id", "metrics"]
  }
}
```

### 4. `compare_designs`

跨游戏设计比较。

```typescript
{
  name: "compare_designs",
  description: "Compare design patterns across multiple games",
  inputSchema: {
    type: "object",
    properties: {
      game_ids: {
        type: "array",
        items: { type: "string" }
      },
      comparison_dimensions: {
        type: "array",
        items: {
          type: "string",
          enum: ["mechanics", "balance", "player_count", "pacing", "complexity"]
        }
      }
    },
    required: ["game_ids"]
  }
}
```

**返回示例：**
```json
{
  "mechanics": {
    "resource_management": {
      "game_a": "worker_placement",
      "game_b": "deck_building",
      "game_c": "auction"
    },
    "similarity_score": 0.35
  },
  "balance": {
    "game_a": { score: 8.5, stable: true },
    "game_b": { score: 7.2, stable: false },
    "game_c": { score: 9.0, stable: true }
  }
}
```

### 5. `calculate_fitness`

计算设计适应度。

```typescript
{
  name: "calculate_fitness",
  description: "Calculate overall fitness score for a game design",
  inputSchema: {
    type: "object",
    properties: {
      game_id: { type: "string" },
      version: { type: "string" },
      fitness_dimensions: {
        type: "array",
        items: {
          type: "string",
          enum: ["compatibility", "activation", "token_efficiency", "triadic_balance"]
        }
      }
    },
    required: ["game_id", "version"]
  }
}
```

**返回示例：**
```json
{
  "overall_fitness": 8.7,
  "breakdown": {
    "compatibility": 1.0,
    "activation": 0.85,
    "token_efficiency": 0.9,
    "triadic_balance": 1.0
  },
  "recommendations": [
    "Add more trigger keywords for better activation",
    "Consider extracting large sections to references/"
  ]
}
```

### 6. `generate_test_scenarios`

自动生成测试场景。

```typescript
{
  name: "generate_test_scenarios",
  description: "Generate playtest scenarios based on game mechanics",
  inputSchema: {
    type: "object",
    properties: {
      mechanics: {
        type: "array",
        items: { type: "string" }
      },
      focus_areas: {
        type: "array",
        items: {
          type: "string",
          enum: ["rule_learning", "mechanic_execution", "strategy", "interaction", "edge_cases", "balance"]
        }
      }
    },
    required: ["mechanics"]
  }
}
```

---

## Database Schema

### Playtest Data Table

```sql
CREATE TABLE playtest_data (
  id SERIAL PRIMARY KEY,
  game_id VARCHAR(255) NOT NULL,
  version VARCHAR(50) NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  player_count INTEGER NOT NULL,
  duration INTEGER NOT NULL,
  winner VARCHAR(100),
  scores JSONB,
  issues JSONB,
  feedback JSONB,
  metrics JSONB,
  INDEX idx_game_version (game_id, version),
  INDEX idx_timestamp (timestamp)
);
```

### Evolution Tracking Table

```sql
CREATE TABLE evolution_tracking (
  id SERIAL PRIMARY KEY,
  game_id VARCHAR(255) NOT NULL,
  version VARCHAR(50) NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  clarity_score DECIMAL(3,2),
  strategy_score DECIMAL(3,2),
  interaction_score DECIMAL(3,2),
  balance_score DECIMAL(3,2),
  fitness_score DECIMAL(3,2),
  changes_made TEXT[],
  INDEX idx_game_evolution (game_id, version)
);
```

### Cross-Game Comparison Table

```sql
CREATE TABLE game_designs (
  id SERIAL PRIMARY KEY,
  game_id VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  mechanics JSONB,
  balance_data JSONB,
  player_count_data JSONB,
  complexity_score DECIMAL(3,2),
  tags VARCHAR(255)[]
);
```

---

## Server Configuration

### package.json

```json
{
  "name": "boardgame-design-mcp-server",
  "version": "1.0.0",
  "description": "MCP server for board game design analytics",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx src/index.ts"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "pg": "^8.11.0",
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0",
    "tsx": "^4.0.0"
  }
}
```

---

## Usage Examples

### Example 1: Store Playtest Data

```typescript
// After a playtest session
await client.callTool({
  name: "store_playtest_data",
  arguments: {
    game_id: "dragon-valley",
    version: "v0.1.0",
    data: {
      timestamp: "2025-01-23T20:00:00Z",
      player_count: 3,
      duration: 62,
      winner: "Player 2",
      scores: [45, 52, 38],
      issues: [
        { type: "Clarity", severity: "Medium", description: "Card text unclear" }
      ],
      feedback: {
        enjoyment: 8,
        clarity: 6,
        replay_interest: true
      }
    }
  }
});
```

### Example 2: Analyze Balance

```typescript
const balance = await client.callTool({
  name: "analyze_balance",
  arguments: {
    game_id: "dragon-valley",
    version: "v0.1.0",
    analysis_type: "all"
  }
});

console.log(balance);
// { economic: {...}, strategic: {...}, player_count: {...} }
```

### Example 3: Track Evolution

```typescript
await client.callTool({
  name: "track_evolution",
  arguments: {
    game_id: "dragon-valley",
    metrics: {
      clarity_score: 7.5,
      strategy_score: 8.0,
      interaction_score: 7.0,
      balance_score: 6.5
    }
  }
});
```

### Example 4: Compare Designs

```typescript
const comparison = await client.callTool({
  name: "compare_designs",
  arguments: {
    game_ids: ["dragon-valley", "crystal-mines", "forest-legends"],
    comparison_dimensions: ["mechanics", "balance", "player_count"]
  }
});
```

---

## Evolutionary Pressure Framework

### Fitness Landscape Navigation

```typescript
interface FitnessLandscape {
  games: Map<string, FitnessPoint>;
}

interface FitnessPoint {
  effectiveness: number;  // 0-1
  generality: number;     // 0-1
  fitness: number;        // calculated
  neighbors: string[];    // similar designs
}

// Avoid local optima
function navigateLandscape(
  current: FitnessPoint,
  population: FitnessPoint[]
): FitnessPoint {
  // Calculate pressure toward global optimum
  const pressure = calculateEvolutionaryPressure(population);

  // Apply mutation
  const mutated = applyMutation(current, pressure);

  // Validate fitness
  return validateFitness(mutated) ? mutated : current;
}
```

### Selection Pressure Implementation

```typescript
interface SelectionPressure {
  natural: {
    activation_rate: number;
    success_rate: number;
  };
  artificial: {
    validation_passed: boolean;
    compatibility_score: number;
  };
  sexual: {
    composition_count: number;
    triadic_balance: number;
  };
}

function calculateSelectionPressure(
  skill: SkillData
): SelectionPressure {
  return {
    natural: {
      activation_rate: skill.usage_count / total_usage,
      success_rate: skill.successful_uses / skill.total_uses
    },
    artificial: {
      validation_passed: skill.validation_result === "PASS",
      compatibility_score: skill.compatibility_score
    },
    sexual: {
      composition_count: skill.triad_compositions.length,
      triadic_balance: skill.triadic_balance_score
    }
  };
}
```

---

## Integration with Skill

### Skill Configuration

```yaml
# boardgame-design/skill.md
mcp_servers:
  boardgame-analytics:
    command: node
    args: ["path/to/mcp-server/dist/index.js"]
    env:
      DATABASE_URL: postgresql://localhost/boardgame_design
      PORT: 3000
```

### Usage in Agent

```typescript
// In boardgame-designer Agent
async function analyzeGameBalance(gameId: string, version: string) {
  const result = await this.mcp.callTool({
    name: "analyze_balance",
    arguments: { game_id: gameId, version, analysis_type: "all" }
  });

  // Use results for recommendations
  return generateBalanceRecommendations(result);
}
```

---

## Deployment

### Docker Compose

```yaml
version: '3.8'
services:
  boardgame-mcp:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/boardgame
      - NODE_ENV=production
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      - POSTGRES_DB=boardgame
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## Monitoring

### Health Metrics

```typescript
interface HealthMetrics {
  total_playtests: number;
  unique_games: number;
  average_fitness: number;
  active_iterations: number;
  error_rate: number;
}

async function getHealthMetrics(): Promise<HealthMetrics> {
  // Query database for aggregate metrics
  return {
    total_playtests: await db.playtest_data.count(),
    unique_games: await db.game_designs.count(),
    average_fitness: await db.evolution_tracking.avg('fitness_score'),
    active_iterations: await getActiveIterationCount(),
    error_rate: await calculateErrorRate()
  };
}
```

---

**See Also:**
- `balance-analysis.md` - 平衡性分析方法
- `playtest-framework.md` - 测试框架
- `FITNESS_ANALYSIS.md` - 适应度分析
