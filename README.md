# pyQuejica (a.k.a. The Whiner Project)

Customize the *thinking labels* of Claude Code and Gemini CLI — those status messages that appear while the model is reasoning or executing tools — by replacing them with your own expressive verbs and phrases.

<div align=center>

|![](images/maldiciendo.jpeg)|![](images/rezando.jpeg)<br>![](images/sudando.jpeg)|![](images/Firibicundiando.jpeg)|
|-|-|-|

</div>

The name comes from **Proyecto Quejica** (Project Whiner): the original idea of giving automatic vacuum cleaners a voice so they would clean while complaining.

> The scripts are idempotent: running them multiple times won't cause any negative side effects.

## Requirements

- Claude Code installed (`claude`) and/or Gemini CLI installed (`gemini`), accessible in your PATH.
- `jq` (for the Claude Code sync).
- Python 3 (for the Gemini CLI patch).

## Installation

```bash
./install.sh
```

It does two things:

1. Creates the `parcharLLM` symlink in `~/.local/bin` (Gemini CLI patch).
2. Registers a `SessionStart` hook in `~/.claude/settings.json` that runs `sync-spinner-verbs.sh` on every Claude Code startup.

Safe to re-run: if the repo moves to a different path, it updates the hook.

## Usage

### For Claude Code

No action needed: the hook syncs `verbs.txt` into the native `spinnerVerbs` setting of `~/.claude/settings.json` on every startup. Claude Code watches `settings.json` and hot-reloads its configuration, so new verbs apply even to sessions that are already open.

Manual sync:
```bash
./sync-spinner-verbs.sh
```

### For Gemini CLI
```bash
# Applies custom status messages (Firibicundiando, Snooping around, Doing the dirty work...)
python3 patch_gemini_verbs.py

# Show patch status and restore backups
python3 patch_gemini_verbs.py --status
python3 patch_gemini_verbs.py --restore
```

## Customization

- **Claude:** Edit `verbs.txt` (one verb per line). New verbs go at the top of the file.
- **Gemini:** Edit the `TRANSLATIONS` dictionary in `patch_gemini_verbs.py` to change which message replaces which.

## How it works

### Claude Code
Claude Code reads the `spinnerVerbs` setting from `~/.claude/settings.json` (`mode: replace` uses only your verbs; `mode: append` adds them to the stock ones). `sync-spinner-verbs.sh` regenerates that setting from `verbs.txt` whenever they differ. Since this is configuration rather than a binary patch, it survives Claude Code updates.

Legacy method: `patch_claude_verbs.py` patched the gerund array directly in the bundle (`cli.js`) or the ELF binary. It is kept in case the native setting goes away (`--restore` undoes the patch).

### Gemini CLI
The bundle is split into several `chunks`. The script explores the bundle directory looking for specific tool-related strings (like "Searching the web" or "Thinking") and replaces them with versions that have more personality (like "Snooping around the web" or "Firibicundiando").

## After updating your CLI tools

- **Claude Code:** nothing to do; the setting and the hook survive updates.
- **Gemini CLI:** every `npm` update overwrites the files and removes the patch. Just run `patch_gemini_verbs.py` again (and delete the old `.bak` files if the script indicates they already exist).
