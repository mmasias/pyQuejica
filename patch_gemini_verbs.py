#!/usr/bin/env python3
"""
patch_gemini_verbs.py

Personaliza los mensajes de estado de Gemini CLI con un toque "quejica".
A diferencia de Claude, Gemini no usa un array centralizado, por lo que este script
busca y reemplaza patrones de mensajes de herramientas en los chunks del bundle.

Uso:
    python3 patch_gemini_verbs.py          # Aplica el parche
    python3 patch_gemini_verbs.py --restore  # Restaura desde el backup (.bak)
    python3 patch_gemini_verbs.py --status   # Muestra el estado actual
"""

import os
import re
import sys
import shutil
import subprocess

# Diccionario de "traducción" Quejica para Gemini
# (Original exacto -> Nuevo mensaje)
TRANSLATIONS = {
    'Thinking': 'Firibicundiando',
    'Searching the web for:': 'Chismorreando en internet sobre:',
    'Reading from file': 'Cotilleando el archivo',
    'Executing command': 'Haciendo el trabajo sucio:',
    'Searching for files matching': 'Rastreando como un sabueso:',
    'Reading and returning the content of': 'Leyendo (y juzgando) el contenido de',
    'Replaces text within a file': 'Metiendo mano en el archivo',
    'Writes the complete content to a file': 'Escribiendo el testamento en',
    'Analyzes and extracts information from': 'Analizando y criticando la info de',
}

def find_gemini_bundle_dir():
    result = subprocess.run(["which", "gemini"], capture_output=True, text=True)
    if result.returncode != 0:
        raise FileNotFoundError("'gemini' no encontrado en PATH")
    gemini_bin = result.stdout.strip()
    real_path = os.path.realpath(gemini_bin)
    
    # Si real_path es .../bundle/gemini.js, el dir es os.path.dirname(real_path)
    current_dir = os.path.dirname(real_path)
    if os.path.basename(current_dir) == "bundle":
        return current_dir
    
    # Fallback si por alguna razón el binario no está en /bundle/
    bundle_dir = os.path.join(current_dir, "bundle")
    if os.path.exists(bundle_dir):
        return bundle_dir
        
    # Segundo fallback para instalaciones NVM o globales estándar
    node_modules_path = os.path.join(os.path.dirname(os.path.dirname(real_path)), "lib", "node_modules", "@google", "gemini-cli", "bundle")
    if os.path.exists(node_modules_path):
        return node_modules_path
        
    raise FileNotFoundError(f"No se pudo localizar el directorio de bundle. Path real: {real_path}")

def get_bundle_files(bundle_dir):
    files = []
    for f in os.listdir(bundle_dir):
        if f.endswith(".js"):
            files.append(os.path.join(bundle_dir, f))
    return files

def cmd_patch(files):
    patched_count = 0
    for file_path in files:
        # Solo parcheamos si encontramos alguna coincidencia
        content = None
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        needs_patch = False
        new_content = content
        for old, new in TRANSLATIONS.items():
            if old in content:
                needs_patch = True
                new_content = new_content.replace(old, new)
        
        if needs_patch:
            # Crear backup si no existe
            bak = file_path + ".bak"
            if not os.path.exists(bak):
                shutil.copy2(file_path, bak)
                print(f"Backup creado: {os.path.basename(bak)}")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Archivo parcheado: {os.path.basename(file_path)}")
            patched_count += 1
            
    if patched_count == 0:
        print("No se encontraron cadenas para parchear. ¿Quizás ya está parcheado?")
    else:
        print(f"\nListo. {patched_count} archivos modificados.")

def cmd_restore(files):
    restored_count = 0
    for file_path in files:
        bak = file_path + ".bak"
        if os.path.exists(bak):
            shutil.copy2(bak, file_path)
            print(f"Restaurado: {os.path.basename(file_path)}")
            restored_count += 1
    
    if restored_count == 0:
        print("No se encontraron archivos de backup para restaurar.")
    else:
        print(f"\nListo. {restored_count} archivos restaurados.")

def cmd_status(files):
    print("Estado de los mensajes de Gemini CLI:\n")
    found_any = False
    for file_path in files:
        content = None
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for old, new in TRANSLATIONS.items():
            if new in content and new != old:
                print(f"[PARCHEADO] '{new}' encontrado en {os.path.basename(file_path)}")
                found_any = True
            elif old in content:
                print(f"[ORIGINAL]  '{old}' encontrado en {os.path.basename(file_path)}")
                found_any = True
                
    if not found_any:
        print("No se encontraron mensajes conocidos. Comprueba la versión de Gemini CLI.")

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    
    try:
        bundle_dir = find_gemini_bundle_dir()
        print(f"Directorio de bundle: {bundle_dir}\n")
        files = get_bundle_files(bundle_dir)
        
        if arg == "--restore":
            cmd_restore(files)
        elif arg == "--status":
            cmd_status(files)
        else:
            cmd_patch(files)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
