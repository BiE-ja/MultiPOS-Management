FROM python:3.13-slim

# crée le dossier de travail
WORKDIR /app

# Copie les fichiers nécessaires dans le dossier de travail
COPY ./requirements.txt ./requirements.txt
COPY ./app /app/app    
COPY .env /app/.env                                                                        
# Update system packages to fix vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean

RUN pip install --no-cache-dir -r requirements.txt



CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--workers", "1"]

