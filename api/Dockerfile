FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application dans le container
COPY . /app

# Installer les dépendances de l'application
RUN pip install -r requirements.txt

# Installer Nginx
RUN apt-get update && apt-get install -y nginx

# Copier la configuration de Nginx dans le container
COPY .platform/nginx/conf.d/proxy.conf /etc/nginx/sites-available/default

# Exposer le port pour Nginx (80) et Gunicorn (8000)
EXPOSE 80 8000

# Lancer Gunicorn et Nginx
CMD service nginx start && gunicorn -w 4 -b 0.0.0.0:8000 application:application