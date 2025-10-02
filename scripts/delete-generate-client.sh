#!/bin/bash

#on se place dans le dossier où est le script, indépendamment du dossier courant
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#variable
FRONTEND_DIR= "../frontend/src/client"

#DIR to clean
DIRS=(
    "$FRONTEND_DIR/services"
    "$FRONTEND_DIR/services/mock"
    "$FRONTEND_DIR/schemas"
    "$FRONTEND_DIR/schemas/mock"
)

for DIR in "${DIRS[@]}"; do
    if ([ -d "$DIR" ]); then
        rm -rf "$DIR"/*
        echo "$DIR: vidé"
    else
        echo "Dossier $DIR inexistant" 
    fi
done