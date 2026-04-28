# pyQuejica

Personaliza los *thinking labels* de Claude Code y Gemini CLI — esos textos que aparecen mientras el modelo razona o ejecuta herramientas — sustituyéndolos por verbos y mensajes propios.

<div align=center>

|![](/images/maldiciendo.jpeg)|![](/images/rezando.jpeg)<br>![](/images/sudando.jpeg)|![](/images/Firibicundiando.jpeg)|
|-|-|-|

</div>

El nombre viene del **Proyecto Quejica**: la idea original de dotar a las aspiradoras automáticas de voz para que limpiaran quejándose.

> Los scripts son idempotentes: ejecutarlos varias veces sobre archivos ya parcheados no produce efectos secundarios negativos.

## Requisitos

- Python 3
- Claude Code instalado (`claude`) y/o Gemini CLI instalado (`gemini`) y accesibles en el PATH.

## Uso

### Para Claude Code
```bash
# Aplica los verbos definidos en VERBS (Maldiciendo, Pujando...)
python3 patch_claude_verbs.py

# Muestra los verbos actuales y restaura el original
python3 patch_claude_verbs.py --status
python3 patch_claude_verbs.py --restore
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

- **Claude:** Edita la lista `VERBS` al inicio de `patch_claude_verbs.py`.
- **Gemini:** Edita el diccionario `TRANSLATIONS` en `patch_gemini_verbs.py` para cambiar qué mensaje sustituye a cuál.

## Cómo funciona

### Claude Code
El bundle (`cli.js`) contiene un array de gerundios. El script localiza el patrón `return[...VAR,...q.verbs]` en el bundle minificado, identifica la variable y sustituye su inicialización.

### Gemini CLI
El bundle está dividido en `chunks`. El script explora el directorio del bundle buscando cadenas específicas de las herramientas (como "Searching the web" o "Thinking") y las reemplaza por versiones con más personalidad (como "Chismorreando en internet" o "Firibicundiando").

## Tras actualizar las herramientas
Cada actualización via `npm` sobreescribe los archivos y borra el parche. Solo hay que volver a ejecutar los scripts (y borrar los `.bak` viejos si el script indica que ya existen).
