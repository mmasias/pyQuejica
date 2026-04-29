#!/usr/bin/env python3
"""
patch_claude_verbs.py

Reemplaza los thinking labels de Claude Code con verbos personalizados.
Compatible con instalaciones basadas en cli.js (texto) y claude.exe (binario ELF).
Ejecutar después de cada actualización de Claude Code.

Uso:
    python3 patch_claude_verbs.py          # aplica los verbos definidos en VERBS
    python3 patch_claude_verbs.py --restore  # restaura el backup original
    python3 patch_claude_verbs.py --status  # muestra el array actual
"""

import re
import os
import sys
import shutil
import subprocess

VERBS = [
  "Maldiciendo",
  "Pujando",
  "Farfullando",
  "Procrastinando",
  "Rezando",
  "Negociando",
  "Mintiendo",
  "Facturando",
  "Depurando",
  "Sobreviviendo",
  "Resignándose",
  "Improvisando",
  "Cafeinándose",
  "Rumiando",
  "Blasfemando",
  "Trampeando",
  "Bufando",
  "Resoplando",
  "Jadeando",
  "Gruñendo",
  "Pataleando",
  "Apechugando",
  "Braceando",
  "Cojeando",
  "Empujando",
  "Cargando",
  "Tirando",
  "Arrastrándose",
  "Cavilando",
  "Mascullando",
  "Titubeando",
  "Divagando",
  "Desvariando",
  "Alucinando",
  "Delirando",
  "Filosofando",
  "Conjeturando",
  "Elucubrando",
  "Maquinando",
  "Fraguando",
  "Intuyendo",
  "Barajando",
  "Especulando",
  "Lamentándose",
  "Capitulando",
  "Claudicando",
  "Derrumbándose",
  "Naufragando",
  "Hundiéndose",
  "Expirando",
  "Agonizando",
  "Resucitando",
  "Rindiéndose",
  "Desmoronándose",
  "Recomponiéndose",
  "Sobreponiéndose",
  "Arrepintiéndose",
  "Refactorizando",
  "Compilando",
  "Mergeando",
  "Commiteando",
  "Hackeando",
  "Debuggeando",
  "Desplegando",
  "Rollbackeando",
  "Parchando",
  "Testeando",
  "Pusheando",
  "Cacheando",
  "Parseando",
  "Pivotando",
  "Iterando",
  "Defragmentando",
  "Rebooteando",
  "Formateando",
  "Renderizando",
  "Bufferizando",
  "Pixelando",
  "Escaneando",
  "Recalentándose",
  "Cortocircuitándose",
  "Cascando",
  "Corrigiendo",
  "Calificando",
  "Suspendiendo",
  "Evaluando",
  "Deliberando",
  "Pontificando",
  "Discrepando",
  "Rebatiendo",
  "Disertando",
  "Documentando",
  "Disonando",
  "Afinando",
  "Destemplándose",
  "Sincopando",
  "Distorsionando",
  "Modulando",
  "Ensayando",
  "Componiendo",
  "Armonizando",
  "Gestionando",
  "Alineando",
  "Optimizando",
  "Escalando",
  "Delegando",
  "Reportando",
  "Reuniéndose",
  "Priorizando",
  "Stakeholdeando",
  "Onboardeando",
  "Cuestionándose",
  "Relativizando",
  "Contemplando",
  "Introspectando",
  "Epifaniando",
  "Iluminándose",
  "Existiendo",
  "Absurdizando",
  "Meditando",
  "Nihilizando",
  "Fingiendo",
  "Actuando",
  "Simulando",
  "Aparentando",
  "Blofando",
  "Cobrando",
  "Excusándose",
  "Justificándose",
  "Contemporizando",
  "Vendiendo",
  "Apañando",
  "Chapuceando",
  "Escaqueándose",
  "Escurriéndose",
  "Evadiéndose",
  "Culebreando",
  "Floreando",
  "Liándola",
  "Embrollando",
  "Enredándose",
  "Vibrando",
  "Oxidándose",
  "Descalibrándose",
  "Fundiéndose",
  "Petando",
  "Chirriando",
  "Humeando",
  "Sobrecargándose",
  "Herrumbrándose",
  "Chisporroteando",
  "Encomendándose",
  "Santiguándose",
  "Confesándose",
  "Expiando",
  "Mortificándose",
  "Penitenciando",
  "Flagelándose",
  "Conspirando",
  "Tramando",
  "Presagiando",
  "Cotorreando",
  "Balbuceando",
  "Tartamudeando",
  "Vaticinando",
  "Augurando",
  "Palpitando",
  "Apostando",
  "Empantanándose",
  "Atascándose",
  "Zumbando",
  "Jalando",
  "Gambeteando",
  "Trabándose",
  "Eternizándose"
]

# Matches a JSON array of strings, with optional whitespace before the closing bracket
# (el whitespace puede quedar del padding de ejecuciones anteriores)
_JSON_ARRAY = rb'\[(?:"[^"]+",)*"[^"]+"\s*\]'


def find_claude_target():
    """Returns (path, is_binary) for the Claude Code patchable file."""
    result = subprocess.run(["which", "claude"], capture_output=True, text=True)
    if result.returncode != 0:
        raise FileNotFoundError("'claude' no encontrado en PATH")
    real_path = os.path.realpath(result.stdout.strip())

    # Nuevo formato: binario ELF compilado
    if real_path.endswith("claude.exe") and os.path.exists(real_path):
        return real_path, True

    # Formato clásico: symlink directo a cli.js
    if real_path.endswith("cli.js") and os.path.exists(real_path):
        return real_path, False

    # Fallback: buscar cli.js subiendo desde el binario
    search_dir = os.path.dirname(real_path)
    for _ in range(4):
        candidate = os.path.join(search_dir, "cli.js")
        if os.path.exists(candidate):
            return candidate, False
        search_dir = os.path.dirname(search_dir)

    raise FileNotFoundError(
        f"No se encontró cli.js ni claude.exe. Ruta real del binario: {real_path}"
    )


def find_verbs_array(data: bytes):
    """
    Localiza el array de thinking verbs en el bundle (texto o binario).

    Anchor: return[...VAR,...X.verbs] donde X puede ser q, $ u otro identificador JS.
    Devuelve lista de (start, end) para cada ocurrencia del array.
    """
    anchor = re.search(
        rb'return\[\.\.\.([\w$]+),\.\.\.[a-zA-Z_$][\w$]*\.verbs\]', data
    )
    if not anchor:
        return []
    var_name = re.escape(anchor.group(1))
    pattern = var_name + rb"=(" + _JSON_ARRAY + rb")"
    return [(m.start(1), m.end(1)) for m in re.finditer(pattern, data)]


def build_padded_array(verbs: list, target_len: int) -> bytes:
    """
    Construye un array JS de exactamente target_len bytes ciclando verbs.
    El array resultante es JS válido: los espacios de relleno van entre la
    última entrada y el cierre de corchete (whitespace ignorado por el parser).
    """
    entries = []
    while True:
        v = verbs[len(entries) % len(verbs)]
        candidate = '["' + '","'.join(entries + [v]) + '"]'
        if len(candidate.encode("utf-8")) > target_len:
            break
        entries.append(v)
    if not entries:
        raise ValueError(f"Los verbos son demasiado largos para caber en {target_len} bytes")
    base = '["' + '","'.join(entries) + '"'
    base_b = base.encode("utf-8")
    padding = target_len - len(base_b) - 1  # -1 por el cierre "]"
    return base_b + b" " * padding + b"]"


def cmd_patch(target: str, is_binary: bool, verbs: list):
    bak = target + ".bak"
    if not os.path.exists(bak):
        shutil.copy2(target, bak)
        print(f"Backup creado:  {bak}")
    else:
        print(f"Backup existente: {bak}  (no sobreescrito)")

    with open(target, "rb") as f:
        data = f.read()

    matches = find_verbs_array(data)
    if not matches:
        print("Error: array de verbos no encontrado")
        sys.exit(1)

    first_new = None
    # De derecha a izquierda para no desplazar los offsets anteriores
    for start, end in sorted(matches, reverse=True):
        old_len = end - start
        old_preview = data[start:start + 60].decode("utf-8", errors="replace")
        if is_binary:
            new_arr = build_padded_array(verbs, old_len)
        else:
            new_arr = ("[" + ",".join(f'"{v}"' for v in verbs) + "]").encode("utf-8")
        print(f"Offset {start}: {old_preview}...")
        data = data[:start] + new_arr + data[end:]
        first_new = new_arr  # la última iteración es el offset más bajo

    with open(target, "wb") as f:
        f.write(data)
    print(f"Array nuevo: {first_new[:80].decode('utf-8', errors='replace')}...")

    if sys.platform == "darwin":
        result = subprocess.run(
            ["codesign", "-s", "-", "--force", target],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            print("Firma ad-hoc aplicada (macOS).")
        else:
            print(f"Aviso: codesign falló — {result.stderr.strip()}")

    print("Listo.")


def cmd_restore(target: str):
    bak = target + ".bak"
    if not os.path.exists(bak):
        print(f"Error: no existe backup en {bak}")
        sys.exit(1)
    shutil.copy2(bak, target)
    print(f"Restaurado desde {bak}")


def cmd_status(target: str):
    with open(target, "rb") as f:
        data = f.read()
    matches = find_verbs_array(data)
    if not matches:
        print("Array de verbos no encontrado.")
        return
    start, end = matches[0]
    array_str = data[start:end].decode("utf-8")
    # Eliminar el padding de espacios antes del cierre ] para no contar entradas vacías
    array_str = re.sub(r"\s+\]$", "]", array_str)
    verbs = re.findall(r'"([^"]+)"', array_str)
    print(f"Verbos actuales ({len(verbs)}):")
    for v in verbs:
        print(f"  - {v}")


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""

    target, is_binary = find_claude_target()
    print(f"Target: {target} ({'binario ELF' if is_binary else 'JS'})\n")

    if arg == "--restore":
        cmd_restore(target)
    elif arg == "--status":
        cmd_status(target)
    else:
        cmd_patch(target, is_binary, VERBS)


if __name__ == "__main__":
    main()
