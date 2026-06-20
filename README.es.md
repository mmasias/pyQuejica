# pyQuejica

Personaliza los *thinking labels* de Claude Code — esos textos que aparecen mientras el modelo razona o ejecuta herramientas — sustituyéndolos por verbos y mensajes propios.

<div align=center>

|![](images/maldiciendo.jpeg)|![](images/rezando.jpeg)<br>![](images/sudando.jpeg)|![](images/Firibicundiando.jpeg)|
|-|-|-|

</div>

El nombre viene del **Proyecto Quejica**: la idea original de dotar a las aspiradoras automáticas de voz para que limpiaran quejándose.

## Requisitos

- Claude Code instalado (`claude`) y accesible en el PATH.
- Python 3 (para `install.sh` y `sync-spinner-verbs.sh`).

## Instalación

```bash
./install.sh
```

Registra un hook `SessionStart` en `~/.claude/settings.json` que ejecuta `sync-spinner-verbs.sh` en cada arranque de Claude Code. Re-ejecutable sin efectos secundarios: si el repo cambia de ruta, actualiza el hook.

## Uso

No requiere acción tras la instalación: el hook sincroniza `verbs.txt` con el setting nativo `spinnerVerbs` de `~/.claude/settings.json` en cada arranque. Claude Code vigila `settings.json` y recarga la configuración en caliente, así que los verbos nuevos se aplican incluso a las sesiones ya abiertas.

Sincronización manual:
```bash
./sync-spinner-verbs.sh
```

## Personalización

Edita `verbs.txt` (un verbo o frase por línea). Los nuevos van al principio del archivo. El hook los sincroniza en el siguiente arranque; `sync-spinner-verbs.sh` los aplica de inmediato.

## Cómo funciona

Claude Code lee el setting `spinnerVerbs` de `~/.claude/settings.json` (`mode: replace` usa solo los verbos propios; `mode: append` los añade a los de serie). `sync-spinner-verbs.sh` regenera ese setting desde `verbs.txt` cuando difieren. Al ser configuración y no parche del binario, sobrevive a las actualizaciones de Claude Code.

## Métodos históricos

Los scripts en `deprecated/` son el mecanismo original de pyQuejica. Se conservan como referencia y como red de seguridad si el setting nativo de Claude Code desapareciera en el futuro.

### patch_claude_verbs.py

Parcheaba el array de gerundios directamente en el bundle de Claude Code (`cli.js`) o en el binario ELF. Requería ejecutarse manualmente tras cada actualización. Quedó obsoleto cuando Claude Code introdujo el setting nativo `spinnerVerbs`.

Dispone de `--restore` para deshacer el parche y `--status` para inspeccionar el estado actual.

### patch_gemini_verbs.py / parchar-llm.sh

El bundle de Gemini CLI está dividido en chunks. El script buscaba cadenas específicas de herramientas ("Thinking", "Searching the web") y las reemplazaba con versiones con más personalidad. El problema estructural: cada `npm update` sobreescribe el bundle y borra el parche. No existe equivalente nativo en Gemini CLI al `spinnerVerbs` de Claude Code.
