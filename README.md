# pyQuejica

Personaliza los *thinking labels* de Claude Code — esos textos que aparecen mientras el modelo razona ("Synthesizing", "Reflecting"...) — sustituyéndolos por verbos propios.

<div align=center>

|![](/images/maldiciendo.jpeg)|![](/images/rezando.jpeg)<br>![](/images/sudando.jpeg)|
|-|-|

</div>

El nombre viene del **Proyecto Quejica**: la idea original de dotar a las aspiradoras automáticas de voz para que limpiaran quejándose.

> El script es idempotente: ejecutarlo varias veces sobre un cli.js ya parcheado no produce efectos secundarios.

## Requisitos

- Python 3
- Claude Code instalado y accesible como `claude` en el PATH

## Uso

```bash
# Aplica los verbos definidos en VERBS
python3 patch_claude_verbs.py

# Muestra los verbos actualmente en cli.js
python3 patch_claude_verbs.py --status

# Restaura el backup original (los verbos de fábrica)
python3 patch_claude_verbs.py --restore
```

## Personalización

Edita la lista `VERBS` al inicio de `patch_claude_verbs.py`:

```python
VERBS = [
    "Maldiciendo", "Pujando", "Farfullando", "Procrastinando",
    "Rezando", "Negociando", "Mintiendo", "Facturando",
    "Depurando", "Sobreviviendo", "Resignándose", "Improvisando",
    "Cafeinándose", "Rumiando", "Blasfemando", "Trampeando",
]
```

## Tras actualizar Claude Code

Cada `npm update @anthropic-ai/claude-code` sobreescribe `cli.js` y borra el parche. Para reaplicarlo:

```bash
# Eliminar el backup obsoleto y volver a parchear
rm /ruta/a/claude-code/cli.js.bak
python3 patch_claude_verbs.py
```

La ruta exacta del backup se muestra al ejecutar el script.

## Cómo funciona

El bundle de Claude Code (`cli.js`) contiene un array de gerundios usado para elegir aleatoriamente el label de pensamiento. El script localiza ese array buscando el patrón `return[...VAR,...q.verbs]` en el bundle minificado, identifica la variable `VAR` y sustituye su inicialización por los verbos de `VERBS`. El archivo original se guarda en `cli.js.bak` la primera vez.
