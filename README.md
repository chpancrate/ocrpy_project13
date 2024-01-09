## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

## Déploiement en production

### Architecture

Le système de production est composé de trois conteneurs dockers contenant :
- nginx
- posgredsql
- l'application django

Ils sont hébergés sur une machine EC2 t2 micro chez AWS.

### Procédure d'installation

#### Prérequis

Il est nécessaire d'avoir un compte chez AWS et de créer une instance AWS EC2 t2 micro avec un disque de 20 Go et utilisant Amazon linux.

Il faut prévoir des outils permettant de se connecter avec un terminal à la machine et d'y transférer des fichiers. Dans un environnement Windows il est possible d'utiliser :
- putty : https://www.putty.org
- winscp : https://winscp.net/eng/index.php

Dans la suite des instruction nous assumerons que l'utilisateur utiliser pour se connecter à AWS est ec2-user. Si ce n'est pas votre cas remplacez-le par votre utilisateur.

!!!!!!!!!!!!!!!!  PARAMETRAGE de l'EC2 !!!!!!!!!!!!!!!

#### Installation de Docker

Les conteneurs nécessitent l'installation de Docker sur la machine. Pour cela il faut :

Se connecter à la machine avec un terminal.

Vérifier que les package de la machine sont bien à jour.
```
sudo yum update -y
```
Installer Docker.
```
sudo yum install docker
sudo usermod -a -G docker ec2-user
newgrp docker
```
Les 2 dernières commande permettent à l'utilisateur de ec2-user de lancer Docker sans utiliser sudo.

Pour vérifier la bonne installation de Docker utiliser ``` docker version ```.

Les conteneurs sont lancés avec Docker Compose. Voici comment l'installer:
```
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
Il faut paramétrer les permissions afin que l'on puisse exécuter docker compose:
```
sudo chmod +x /usr/local/bin/docker-compose
```
Pour vérifier la bonne installation de Docker Compose utiliser ``` docker-compose version ```.

Il faut maintenant démarrer le service Docker :
```
sudo service docker start
```
Et s'assurer qu'il sera lancé au démarrage de la machine :
```
sudo systemctl enable docker
```
La machine est maintenant prête à recevoir notre application.

#### Installation de l'application

Se placer dans le répertoire home/ec2-user.

A partir du repository copier les fichiers suivant :
- compose.yml
- le répertoire nginx

Créez un fichier .env avec le format suivant :
```
# sentry configuration
SENTRY_DSN= 

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY=

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=False

ALLOWED_HOSTS=localhost,127.0.0.1,nginx

# database configuration
DB_ENGINE=django.db.backends.postgresql
# DB_ENGINE=django.db.backends.sqlite3
DB_NAME=ocldb
# DB_NAME=oc-lettings-site.sqlite3
DB_USER=ocluser
DB_PASSWORD=
DB_HOST=pg_db
DB_PORT=5432
POSTGRES_PASSWORD=
```
Il faut personaliser les valeurs suivantes :
- SENTRY_DSN : DSN du projet Sentry lié à votre déploiement
- SECRET_KEY : clé secrête utilisée par Django
- ALLOWED_HOSTS : ajouter à la suite l'IP et le DSN de votre instance EC2 (ne pas oublier les virgules de séparation)
- DB_NAME : Nom de votre base de donnée
- DB_USER : nom de votre utilisateur postgresql
- DB_PASSWORD : mot de passe de votre utilisateur postgresql
- POSTGRES_PASSWORD : mot de passe de l'utilisateur "postgres"

Créer les dockers
```
docker-compose up -d
```

Vérifier que la page d'accueil du site s’affiche bien en allant sur l'IP ou le DSN de votre site. Attention à ce stade la base de donnée n'existe pas donc seul la page d'accueil marche.

#### mise à jour de la base 

Avec la commande ```docker ps``` récupérer l'id du Docker postgres et s'y connecter avec :
```docker exec -it iddudockerpostgres bash```

Une fois sur le terminal se connecter à postgresql
```psql -d postgres -U postgres```
Créer l'utilisateur ocluser avec un mot de passe et l'utiliser pour créer la base de donnée

```
CREATE USER ocluser WITH PASSWORD votremotdepasse;
ALTER USER ocluser WITH NOCREATEDB NOCREATEROLE;
CREATE DATABASE ocldb OWNER = ocluser;
```
Sortir de la session postgres avec ```.q``` et du terminal du docker avec ```exit```.

Mettre à jour le fichier .env avec le mot de passe du l'utilisateur ocluser.

Se connecter au docker de l'application.
```
docker exec -it iddudockerapp /bin/sh
```
Une fois sur le terminal effectuer les migrations.
```
python manage.py migrate
```
Charger les données.
```
python manage.py loaddata datadump.json
```

**Le site est maintenant opérationnel.**

#### Automatisation de la mise à jour du site

Nous allons maintenant automatiser la mise à jour du Docker de l'application quand le repository est mis à jour.

Dans le répertoire home/ec2-user créer un fichier deploy.sh :
```
#!/bin/bash
# script run when webhooks from Docker Hub detected
# get the new application image and update the docker accordingly

echo "Received webhook event."

# Pull the application new version
docker pull chpancrate/ocrp13-pgsql:latest

# Restart the Docker containers using the specific image
docker-compose -f docker-compose.yml up -d --no-deps oc_lettings_site
```
Ce script sera utiliser pour mettre à jour le Docker de l'application.

Rendre le script executable ```sudo chmod +x deploy.sh```

Sur le site du Docker hub dans le repository ajouter un webhook vers votre instance, il sera déclenché à chaque création d'une nouvelle image.

payload url : http://your-ec2-instance-ip:8001

payload : application/json

De retour sur votre instance EC2 installer nc pour écouter le Webhook.
```
sudo yum install nc
```

Créer un script webhook_receiver.sh avec le contenu :
```
#!/bin/bash

log_file="./webhook_receiver.log"

echo "Starting webhook receiver..."

while true; do
    # Listen for incoming webhook events on port 8001
    request=$(nc -l -p 8001)

    # Log the received payload to the file
    echo "Received webhook event: $request" >> "$log_file"

    # Trigger the deployment script and log the result
    echo "Running deployment script..." >> "$log_file"
    ./deploy.sh >> "$log_file" 2>&1

    echo "------------  END OF DEPLOYMENT  ------------" >> "$log_file"
done
```
Ce script utilise nc pour écouter le webhook et quand il le reçoit, il lance le fichier deploy.sh qui met à jour le Docker de l'application.

Rendre le script executable ```sudo chmod +x webhook_receiver.sh```

Toutes les actions sont logguées dans webhook_receiver.log

Lancer le script ```./webhook_receiver.sh &```

Lors de la mise à jour de l'image, le Docker de l'application sera maintenant mis à jour.