#!/bin/bash

# Charger les variables d’environnement depuis le fichier .env
export $(grep -v '^#' .env | xargs)

# Par sécurité (si certaines variables manquent)
DB_NAME=${DB_NAME:-pos_management}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-Jarina&586}
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}

# Attendre que Postgres soit prêt
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  echo "⏳ En attente de la base de données PostgreSQL..."
  sleep 2
done

# Créer la base si elle n'existe pas déjà
echo "🚀 Vérification/création de la base $DB_NAME..."
psql -h "$DB_HOST" -U "$DB_USER" -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
  psql -h "$DB_HOST" -U "$DB_USER" -c "CREATE DATABASE $DB_NAME"

# Appliquer les migrations
echo "🔧 Application des migrations Alembic..."
alembic upgrade head

# Create initial data in DB
python app/initial_data.py

# Lancer l'application
echo "🎉 Démarrage de l'application..."
# Démarrage de FastAPI avec uvicorn
echo "🚀 Démarrage de FastAPI..."
exec "$@"