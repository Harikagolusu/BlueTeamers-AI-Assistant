#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
mkdir -p "$ROOT_DIR/logs"
cd "$SCRIPT_DIR"
export PATH="$SCRIPT_DIR/node_modules/.bin:$PATH"
exec npm run dev >> "$ROOT_DIR/logs/frontend_8081.log" 2>&1
