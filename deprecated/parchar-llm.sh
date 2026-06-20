#!/bin/bash
echo "" >&2
echo "[AVISO] parchar-llm.sh es el método histórico de parcheo y ya no se recomienda." >&2
echo "        Ejecuta install.sh una vez para configurar el sistema recomendado:" >&2
echo "          - Claude Code: hook SessionStart que sincroniza verbs.txt con spinnerVerbs." >&2
echo "          - Gemini CLI:  este script de parche manual (se pierde con cada npm update)." >&2
echo "" >&2

SCRIPT_DIR=$(dirname "$(realpath "$0")")
python3 "$SCRIPT_DIR/patch_claude_verbs.py"
python3 "$SCRIPT_DIR/patch_gemini_verbs.py"
