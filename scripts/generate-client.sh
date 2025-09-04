#! /usr/bin/env bash

set -e
set -x

# Active ton venv si nécessaire (ex: .venv)
source backend/venv/Scripts/activate

cd backend
PYTHONPATH=.. python -c "import app.main; import json; print(json.dumps(app.main.app.openapi()))" > ../openapi.json
cd ..

mv openapi.json frontend/

# Script de nettoyage : supprime les anciennes générations de client openapi
#bash  scripts/delete-generate-client.sh

cd frontend

npm run generate-client

npx biome format --write frontend/src/client/services
npx biome format --write frontend/src/client/schemas

# Déplace les fichiers mocks dans un répertoire dédié
#python frontend/src/mock/move-mocks.ts
