#!/bin/bash
# Start React Frontend on port 5173
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR" && pwd)"
mkdir -p "$ROOT_DIR/logs"
cd "$ROOT_DIR/infosecdairies"
export PATH="$ROOT_DIR/infosecdairies/node_modules/.bin:$PATH"
exec npm run dev -- --port 5173 >> "$ROOT_DIR/logs/frontend_5173.log" 2>&1