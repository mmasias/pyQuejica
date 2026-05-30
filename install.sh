#!/bin/bash
REPO=$(dirname "$(realpath "$0")")
mkdir -p ~/.local/bin
chmod +x "$REPO/parchar-llm.sh"
ln -sf "$REPO/parchar-llm.sh" ~/.local/bin/parcharLLM
echo "parcharLLM disponible en ~/.local/bin/parcharLLM"
