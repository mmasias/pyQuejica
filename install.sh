#!/bin/bash
# Instala pyQuejica en esta maquina:
#   1. Symlink parcharLLM en ~/.local/bin (parche de Gemini CLI).
#   2. Hook SessionStart en ~/.claude/settings.json que sincroniza verbs.txt
#      con el setting nativo spinnerVerbs de Claude Code en cada arranque.
# Idempotente: re-ejecutar actualiza el hook si el repo cambio de ruta.
set -euo pipefail

REPO=$(dirname "$(realpath "$0")")

mkdir -p ~/.local/bin
chmod +x "$REPO/parchar-llm.sh" "$REPO/sync-spinner-verbs.sh"
ln -sf "$REPO/parchar-llm.sh" ~/.local/bin/parcharLLM
echo "parcharLLM disponible en ~/.local/bin/parcharLLM"

if ! command -v jq >/dev/null; then
    echo "Aviso: jq no encontrado; no se registra el hook de Claude Code." >&2
    echo "Instalar jq (apt/dnf/brew) y re-ejecutar install.sh." >&2
    exit 0
fi

SETTINGS="$HOME/.claude/settings.json"
HOOK_CMD="$REPO/sync-spinner-verbs.sh"
mkdir -p "$HOME/.claude"
[ -f "$SETTINGS" ] || echo '{}' > "$SETTINGS"

tmp=$(mktemp "$SETTINGS.XXXXXX")
jq --arg cmd "$HOOK_CMD" '
    .hooks.SessionStart = (
        ((.hooks.SessionStart // [])
         | map(select(((.hooks[0].command // "") | endswith("sync-spinner-verbs.sh")) | not)))
        + [{hooks: [{type: "command", command: $cmd, timeout: 15,
                     statusMessage: "Sincronizando verbos de pyQuejica"}]}]
    )' "$SETTINGS" > "$tmp"
mv "$tmp" "$SETTINGS"
echo "Hook SessionStart registrado: $HOOK_CMD"

"$HOOK_CMD"
echo "spinnerVerbs sincronizado desde $REPO/verbs.txt"
