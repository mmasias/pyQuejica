#!/bin/bash
# Instala pyQuejica en esta maquina:
#   Registra un hook SessionStart en ~/.claude/settings.json que sincroniza
#   verbs.txt con el setting nativo spinnerVerbs de Claude Code en cada arranque.
# Idempotente: re-ejecutar actualiza el hook si el repo cambio de ruta.
set -euo pipefail

REPO=$(dirname "$(realpath "$0")")

chmod +x "$REPO/sync-spinner-verbs.sh"

SETTINGS="$HOME/.claude/settings.json"
HOOK_CMD="$REPO/sync-spinner-verbs.sh"
mkdir -p "$HOME/.claude"

python3 - "$HOOK_CMD" "$SETTINGS" <<'EOF'
import json, sys
from pathlib import Path

hook_cmd = sys.argv[1]
settings_path = Path(sys.argv[2])

settings = json.loads(settings_path.read_text()) if settings_path.exists() else {}

session_start = settings.get('hooks', {}).get('SessionStart', [])
session_start = [
    e for e in session_start
    if not e.get('hooks', [{}])[0].get('command', '').endswith('sync-spinner-verbs.sh')
]
session_start.append({
    'hooks': [{
        'type': 'command',
        'command': hook_cmd,
        'timeout': 15,
        'statusMessage': 'Sincronizando verbos de pyQuejica'
    }]
})
settings.setdefault('hooks', {})['SessionStart'] = session_start

tmp = settings_path.with_suffix('.tmp')
tmp.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + '\n')
tmp.replace(settings_path)
EOF

echo "Hook SessionStart registrado: $HOOK_CMD"

"$REPO/sync-spinner-verbs.sh"
echo "spinnerVerbs sincronizado desde $REPO/verbs.txt"
