#!/bin/bash
# Sincroniza verbs.txt con el setting nativo spinnerVerbs de Claude Code
# (~/.claude/settings.json). Solo escribe si la lista difiere, para no
# tocar el fichero en cada arranque.
#
# Pensado para ejecutarse como hook SessionStart de Claude Code; install.sh
# registra el hook. Tambien puede ejecutarse a mano.
set -euo pipefail

SCRIPT_DIR=$(dirname "$(realpath "$0")")
VERBS_FILE="$SCRIPT_DIR/verbs.txt"
SETTINGS="$HOME/.claude/settings.json"

command -v jq >/dev/null || exit 0
[ -f "$VERBS_FILE" ] || exit 0
[ -f "$SETTINGS" ] || echo '{}' > "$SETTINGS"

new_verbs=$(jq -R -s 'split("\n") | map(select(length > 0))' "$VERBS_FILE")
current_verbs=$(jq '.spinnerVerbs.verbs // []' "$SETTINGS")

if [ "$new_verbs" != "$current_verbs" ]; then
    tmp=$(mktemp "$SETTINGS.XXXXXX")
    jq --argjson verbs "$new_verbs" \
        '.spinnerVerbs = {mode: "replace", verbs: $verbs}' \
        "$SETTINGS" > "$tmp"
    mv "$tmp" "$SETTINGS"
fi
