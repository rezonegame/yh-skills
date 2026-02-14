#!/bin/bash
set -e

MAX_ITERATIONS=${1:-20}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================="
echo "   Board Game Ralph Loop Starting..."
echo "   Max iterations: $MAX_ITERATIONS"
echo "========================================="

for i in $(seq 1 $MAX_ITERATIONS); do
  echo ""
  echo "═══════════════════════════════════════"
  echo "   Iteration $i / $MAX_ITERATIONS"
  echo "═══════════════════════════════════════"

  OUTPUT=$(cat "$SCRIPT_DIR/../prompt.md" | claude --dangerously-skip-permissions 2>&1 | tee /dev/stderr) || true

  if echo "$OUTPUT" | grep -q "<promise>DESIGN_COMPLETE</promise>"; then
    echo ""
    echo "========================================="
    echo "   🎮 Game Design Complete! 🎲"
    echo "========================================="
    exit 0
  fi

  sleep 2
done

echo ""
echo "⚠️  Max iterations reached. Check grd.json for remaining tasks."
exit 1
