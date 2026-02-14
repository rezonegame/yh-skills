#!/bin/bash
# Board Game Ralph Loop - Autonomous Iteration Script
# Usage: ./ralph-loop.sh [max_iterations]

set -e

# 配置
MAX_ITERATIONS=${1:-30}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   Board Game Ralph Loop${NC}"
echo -e "${GREEN}   Autonomous Design Iteration${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Max iterations: ${YELLOW}${MAX_ITERATIONS}${NC}"
echo -e "Project root: ${YELLOW}${PROJECT_ROOT}${NC}"
echo ""

# 检查必要文件
if [ ! -f "$PROJECT_ROOT/prompt.md" ]; then
    echo -e "${RED}Error: prompt.md not found!${NC}"
    exit 1
fi

if [ ! -f "$PROJECT_ROOT/grd.json" ]; then
    echo -e "${RED}Error: grd.json not found!${NC}"
    exit 1
fi

# 显示初始状态
echo -e "${BLUE}Initial Status:${NC}"
cat "$PROJECT_ROOT/grd.json" | grep -E '"(passes|title|id)"' | head -20
echo ""

# 主循环
for i in $(seq 1 $MAX_ITERATIONS); do
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${BLUE}   Iteration ${i} / ${MAX_ITERATIONS}${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo ""

    # 运行 Claude Code
    OUTPUT=$(cat "$PROJECT_ROOT/prompt.md" | claude --dangerously-skip-permissions 2>&1) || true

    # 检查是否完成
    if echo "$OUTPUT" | grep -q "<promise>DESIGN_COMPLETE</promise>"; then
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}   🎮 Game Design Complete! 🎲${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""

        # 显示最终状态
        echo -e "${BLUE}Final Fitness Scores:${NC}"
        cat "$PROJECT_ROOT/grd.json" | grep -A 5 '"fitnessGoals"'
        echo ""

        # 显示完成的任务
        echo -e "${BLUE}Completed Tasks:${NC}"
        cat "$PROJECT_ROOT/grd.json" | grep -E '"(id|title|passes)"'
        echo ""

        exit 0
    fi

    # 检查是否需要停止（可选：基于某些条件）
    if [ $i -eq $MAX_ITERATIONS ]; then
        echo ""
        echo -e "${YELLOW}⚠️  Max iterations reached${NC}"
        echo -e "${YELLOW}Check grd.json for remaining tasks${NC}"
        echo ""

        # 显示当前状态
        echo -e "${BLUE}Current Progress:${NC}"
        cat "$PROJECT_ROOT/grd.json" | grep -E '"(passes|title|id)"'
        echo ""

        exit 1
    fi

    # 短暂暂停
    sleep 2
done
