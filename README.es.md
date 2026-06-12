# pyQuejica

Personaliza los *thinking labels* de Claude Code y Gemini CLI — esos textos que aparecen mientras el modelo razona o ejecuta herramientas — sustituyéndolos por verbos y mensajes propios.

<div align=center>

|![](images/maldiciendo.jpeg)|![](images/rezando.jpeg)<br>![](images/sudando.jpeg)|![](images/Firibicundiando.jpeg)|
|-|-|-|

</div>

El nombre viene del **Proyecto Quejica**: la idea original de dotar a las aspiradoras automáticas de voz para que limpiaran quejándose.

> Los scripts son idempotentes: ejecutarlos varias veces no produce efectos secundarios negativos.

## Requisitos

- Claude Code instalado (`claude`) y/o Gemini CLI instalado (`gemini`) y accesibles en el PATH.
- `jq` (para la sincronización con Claude Code).
- Python 3 (para el parche de Gemini CLI).

## Instalación

```bash
./install.sh
```

Hace dos cosas:

1. Crea el symlink `parcharLLM` en `~/.local/bin` (parche de Gemini CLI).
2. Registra un hook `SessionStart` en `~/.claude/settings.json` que ejecuta `sync-spinner-verbs.sh` en cada arranque de Claude Code.

Re-ejecutable sin efectos secundarios: si el repo cambia de ruta, actualiza el hook.

## Uso

### Para Claude Code

No requiere acción: el hook sincroniza `verbs.txt` con el setting nativo `spinnerVerbs` de `~/.claude/settings.json` en cada arranque. Claude Code vigila `settings.json` y recarga la configuración en caliente, así que los verbos nuevos se aplican incluso a las sesiones ya abiertas.

Sincronización manual:
```bash
./sync-spinner-verbs.sh
```

### Para Gemini CLI
```bash
# Aplica los mensajes personalizados (Firibicundiando, Chismorreando...)
python3 patch_gemini_verbs.py

# Muestra el estado del parche y restaura los backups
python3 patch_gemini_verbs.py --status
python3 patch_gemini_verbs.py --restore
```

## Personalización

- **Claude:** Edita `verbs.txt` (un verbo por línea). Los nuevos van al principio del archivo.
- **Gemini:** Edita el diccionario `TRANSLATIONS` en `patch_gemini_verbs.py` para cambiar qué mensaje sustituye a cuál.

## Cómo funciona

### Claude Code
Claude Code lee el setting `spinnerVerbs` de `~/.claude/settings.json` (`mode: replace` usa solo los verbos propios; `mode: append` los añade a los de serie). `sync-spinner-verbs.sh` regenera ese setting desde `verbs.txt` cuando difieren. Al ser configuración y no parche del binario, sobrevive a las actualizaciones de Claude Code.

Método histórico: `patch_claude_verbs.py` parcheaba el array de gerundios directamente en el bundle (`cli.js`) o el binario ELF. Se conserva por si el setting nativo desaparece (`--restore` deshace el parche).

### Gemini CLI
El bundle está dividido en `chunks`. El script explora el directorio del bundle buscando cadenas específicas de las herramientas (como "Searching the web" o "Thinking") y las reemplaza por versiones con más personalidad (como "Chismorreando en internet" o "Firibicundiando").

## Tras actualizar las herramientas

- **Claude Code:** nada que hacer; el setting y el hook sobreviven a las actualizaciones.
- **Gemini CLI:** cada actualización via `npm` sobreescribe los archivos y borra el parche. Volver a ejecutar `patch_gemini_verbs.py` (y borrar los `.bak` viejos si el script indica que ya existen).
