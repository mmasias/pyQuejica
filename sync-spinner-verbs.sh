#!/bin/bash
# Sincroniza verbs.txt con el setting nativo spinnerVerbs de Claude Code
# (~/.claude/settings.json). Solo escribe si la lista difiere, para no
# tocar el fichero en cada arranque.
#
# Pensado para ejecutarse como hook SessionStart de Claude Code; install.sh
# registra el hook. Tambien puede ejecutarse a mano.
set -euo pipefail

SCRIPT_DIR=$(dirname "$(realpath "$0")")

python3 - "$SCRIPT_DIR" <<'EOF'
import json, sys
from pathlib import Path

script_dir = Path(sys.argv[1])
verbs_file = script_dir / 'verbs.txt'
settings_path = Path.home() / '.claude' / 'settings.json'

if not verbs_file.exists():
    sys.exit(0)

new_verbs = [l for l in verbs_file.read_text().splitlines() if l.strip()]

settings = json.loads(settings_path.read_text()) if settings_path.exists() else {}

if new_verbs != settings.get('spinnerVerbs', {}).get('verbs', []):
    settings['spinnerVerbs'] = {'mode': 'replace', 'verbs': new_verbs}
    tmp = settings_path.with_suffix('.tmp')
    tmp.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + '\n')
    tmp.replace(settings_path)
EOF
