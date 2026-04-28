#!/usr/bin/env python3
"""
patch_claude_verbs.py

Reemplaza los thinking labels de Claude Code con verbos personalizados.
Ejecutar después de cada actualización de Claude Code.

Uso:
    python3 patch_claude_verbs.py          # aplica los verbos definidos en VERBS
    python3 patch_claude_verbs.py --restore  # restaura el backup original
    python3 patch_claude_verbs.py --status  # muestra el array actual en cli.js
"""

import re
import os
import sys
import shutil
import subprocess

VERBS = [
    "Maldiciendo", "Pujando", "Farfullando", "Procrastinando",
    "Rezando", "Negociando", "Mintiendo", "Facturando",
    "Depurando", "Sobreviviendo", "Resignándose", "Improvisando",
    "Cafeinándose", "Rumiando", "Blasfemando", "Trampeando",
]

_JSON_ARRAY = r'\[(?:"[^"]+",)*"[^"]+"\]'


def find_cli_js():
    result = subprocess.run(["which", "claude"], capture_output=True, text=True)
    if result.returncode != 0:
        raise FileNotFoundError("'claude' no encontrado en PATH")
    claude_bin = result.stdout.strip()
    real_path = os.path.realpath(claude_bin)
    # El symlink apunta directamente a cli.js
    if real_path.endswith("cli.js") and os.path.exists(real_path):
        return real_path
    # Fallback: buscar cli.js relativo al binario
    node_base = os.path.dirname(os.path.dirname(real_path))
    cli_js = os.path.join(
        node_base, "lib", "node_modules", "@anthropic-ai", "claude-code", "cli.js"
    )
    if not os.path.exists(cli_js):
        raise FileNotFoundError(f"cli.js no encontrado: {cli_js}")
    return cli_js


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def find_verbs_array(content):
    """
    Localiza el array de thinking verbs en el bundle minificado.

    Estrategia: el bundle contiene `return[...VAR,...q.verbs]` donde VAR
    es la variable que almacena los verbos por defecto. Extraemos VAR y
    luego buscamos su asignación `VAR=[...]`.

    Devuelve (start, end) de los corchetes del array, o None.
    """
    # Paso 1: encontrar el nombre de la variable (ej: _L8)
    anchor = re.search(r'return\[\.\.\.([\w$]+),\.\.\.q\.verbs\]', content)
    if not anchor:
        return None
    var_name = re.escape(anchor.group(1))

    # Paso 2: encontrar la asignación VAR=[...] más cercana tras el anchor
    assignment = re.search(
        var_name + r'=(' + _JSON_ARRAY + r')',
        content[anchor.start():]
    )
    if not assignment:
        return None

    base = anchor.start()
    start = base + assignment.start(1)
    end = base + assignment.end(1)
    return start, end


def cmd_patch(cli_js, verbs):
    bak = cli_js + ".bak"
    if not os.path.exists(bak):
        shutil.copy2(cli_js, bak)
        print(f"Backup creado:  {bak}")
    else:
        print(f"Backup existente: {bak}  (no sobreescrito)")

    content = read(cli_js)
    result = find_verbs_array(content)
    if not result:
        print("Error: array de verbos no encontrado en cli.js")
        sys.exit(1)

    start, end = result
    old = content[start:end]
    new = "[" + ",".join(f'"{v}"' for v in verbs) + "]"

    print(f"Array anterior ({len(old)} chars): {old[:80]}...")
    write(cli_js, content[:start] + new + content[end:])
    print(f"Array nuevo: {new}")
    print("Listo.")


def cmd_restore(cli_js):
    bak = cli_js + ".bak"
    if not os.path.exists(bak):
        print(f"Error: no existe backup en {bak}")
        sys.exit(1)
    shutil.copy2(bak, cli_js)
    print(f"Restaurado desde {bak}")


def cmd_status(cli_js):
    content = read(cli_js)
    result = find_verbs_array(content)
    if not result:
        print("Array de verbos no encontrado.")
        return
    start, end = result
    array = content[start:end]
    verbs = re.findall(r'"([^"]+)"', array)
    print(f"Verbos actuales ({len(verbs)}):")
    for v in verbs:
        print(f"  - {v}")


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""

    cli_js = find_cli_js()
    print(f"cli.js: {cli_js}\n")

    if arg == "--restore":
        cmd_restore(cli_js)
    elif arg == "--status":
        cmd_status(cli_js)
    else:
        cmd_patch(cli_js, VERBS)


if __name__ == "__main__":
    main()
