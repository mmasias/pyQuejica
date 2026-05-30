#!/bin/bash
SCRIPT_DIR=$(dirname "$(realpath "$0")")
python3 "$SCRIPT_DIR/patch_claude_verbs.py"
python3 "$SCRIPT_DIR/patch_gemini_verbs.py"
