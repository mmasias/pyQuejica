# pyQuejica (a.k.a. The Whiner Project)

Customize the *thinking labels* of Claude Code — those status messages that appear while the model is reasoning or executing tools — by replacing them with your own expressive verbs and phrases.

<div align=center>

|![](images/maldiciendo.jpeg)|![](images/rezando.jpeg)<br>![](images/sudando.jpeg)|![](images/Firibicundiando.jpeg)|
|-|-|-|

</div>

The name comes from **Proyecto Quejica** (Project Whiner): the original idea of giving automatic vacuum cleaners a voice so they would clean while complaining.

## Requirements

- Claude Code installed (`claude`), accessible in your PATH.
- Python 3 (for `install.sh` and `sync-spinner-verbs.sh`).

## Installation

```bash
./install.sh
```

Registers a `SessionStart` hook in `~/.claude/settings.json` that runs `sync-spinner-verbs.sh` on every Claude Code startup. Safe to re-run: if the repo moves to a different path, it updates the hook.

## Usage

No action needed after installation: the hook syncs `verbs.txt` into the native `spinnerVerbs` setting of `~/.claude/settings.json` on every startup. Claude Code watches `settings.json` and hot-reloads its configuration, so new verbs apply even to sessions that are already open.

Manual sync:
```bash
./sync-spinner-verbs.sh
```

## Customization

Edit `verbs.txt` (one verb or phrase per line). New verbs go at the top of the file. The hook picks them up on the next startup; `sync-spinner-verbs.sh` applies them immediately.

## How it works

Claude Code reads the `spinnerVerbs` setting from `~/.claude/settings.json` (`mode: replace` uses only your verbs; `mode: append` adds them to the stock ones). `sync-spinner-verbs.sh` regenerates that setting from `verbs.txt` whenever they differ. Since this is configuration rather than a binary patch, it survives Claude Code updates.

## Legacy methods

The scripts in `deprecated/` are pyQuejica's original mechanism. They are kept as a reference and as a fallback in case the native Claude Code setting disappears in the future.

### patch_claude_verbs.py

Patched the gerund array directly in the Claude Code bundle (`cli.js`) or the ELF binary. Required manual execution after every Claude Code update. Became obsolete when Claude Code introduced the native `spinnerVerbs` setting.

Supports `--restore` to undo the patch and `--status` to inspect the current state.

### patch_gemini_verbs.py / parchar-llm.sh

The Gemini CLI bundle is split into chunks. The script searched for specific tool strings ("Thinking", "Searching the web") and replaced them with versions that have more personality. The structural problem: every `npm update` overwrites the bundle and erases the patch. There is no native equivalent in Gemini CLI to Claude Code's `spinnerVerbs`.
