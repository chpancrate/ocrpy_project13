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

- Le code se trouve ici : https://github.com/chpancrate/ocrpy_project13
- Faire un fork du projet
- `cd /path/to/put/project/in
- `git clone referencedevotrerepository.git

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

#### Paramétrer les variables d'environnement
- Créez un fichier .env avec le format suivant:
```
# sentry configuration
SENTRY_DSN= "DSN de votre projet Sentry"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY= "Clé secrête à definir et ne pas divulguer"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=False

ALLOWED_HOSTS=localhost,127.0.0.1,nginx

# database configuration
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=oc-lettings-site.sqlite3
```
-  Ce fichier permet au package python-dotenv de définir les variables d'environnement nécessaires et d'utiliser la base sqlite de développement.

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

Pour le déploiement en production le code à utiliser est celui du repository créer dans la partie développement.

### Architecture

Le système de production est composé de trois conteneurs Docker contenant :
- nginx
- posgresql
- l'application django

La definition des conteneurs se trouve dans le fichier compose.yml à la racine du projet.

Un workflow CI/CD est créé chez CircleCI afin de tester le code et de générer une image Docker de l'application sur un repository hébergé sur Docker Hub. 

Les conteneurs sont hébergés sur une machine EC2 t2 micro chez AWS. En utilisant un webhook paramétré sur Docker Hub, le conteneur de l'application est mis à jour automatiquement lors de la génération d'une nouvelle image sur le repository Docker Hub.

Il y a également un suivi grace à Sentry.

Il est donc nécessaire d'avoir des comptes sur les sites suivants:
- Sentry (Créer un projet pour l'application et noter le DSN correspondant)
- CircleCI
- Docker Hub (créer un repository pour l'application)
- AWS

### CircleCI

Avant le paramétrage du projet sur CircleCi, il faut mettre à jour le fichier config.yml situé dans le répertoire .circleci et remplacer chpancrate/ocrp13-pgsql par la référence de votre repository sur Docker Hub.

Lors de la création du projet dans CircleCI, il suffit de donner l'adresse du repository Github du projet pour que CircleCI récupère le fichier de workflow et lance celui-ci.

La première exécution (lancèe automatiquement à la création) se finira en erreur car il faut definir les variables d'environnement ci-dessous pour que le workflow se termine normalement.

| variable | valeur |
|----------|--------|
| ALLOWED_HOSTS | localhost,127.0.0.1,nginx |
| DEBUG | False |
| DOCKER_USER | votre utilisateur Docker Hub |
| DOCKER_PASS | votre mot de passe Docker Hub |
| SECRET_KEY | phrase secrête |
| SENTRY_DSN | le DSN de votre projet Sentry de suivi |


ATTENTION : lors des tests du workflow CircleCI, si le titre de la page web est modifié, il est important que le titre du site contienne toujours 'Welcome to Holiday Homes', sinon certains tests échoueront.

### Procédure d'installation chez AWS

#### Prérequis

Il est nécessaire d'avoir un compte chez AWS et de créer une instance AWS EC2 t2 micro avec un disque de 20 Go et utilisant Amazon linux.
A la création de l'instance, il faut s'assurer que le traffic est accepter depuis internet pour les 2 ports suivant :
- 80 : pour le site web
- 8001 : pour le webhook de Docker Hub

Il est possible de se connecter à l'instance directement à partir du site d'AWS.

Dans un environnement Windows il est possible d'utiliser :
- putty : https://www.putty.org, pour la connexion en terminal
- winscp : https://winscp.net/eng/index.php, pour le transfert de fichier

Dans la suite des instructions nous assumerons que l'utilisateur utilisé pour se connecter à AWS est ec2-user. Si ce n'est pas votre cas remplacez-le par votre utilisateur.

#### Installation de Docker

Les conteneurs nécessitent l'installation de Docker sur la machine. Pour cela il faut :

Se connecter à la machine avec un terminal.

Vérifier que les packages de la machine sont bien à jour.
```
sudo yum update -y
```
Installer Docker.
```
sudo yum install docker
sudo usermod -a -G docker ec2-user
newgrp docker
```
Les 2 dernières commandes permettent à l'utilisateur de ec2-user de lancer Docker sans utiliser sudo.

Pour vérifier la bonne installation de Docker utiliser la commande ``` docker version ```.

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

Modifier le fichier compose.yml pour remplacer chpancrate/ocrp13-pgsql:latest par la source de votre image.

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
- ALLOWED_HOSTS : ajouter à la suite l'IP et le DNS de votre instance EC2 (ne pas oublier les virgules de séparation)
- DB_NAME : Nom de votre base de donnée ci-dessous nous utilisons ocldb
- DB_USER : nom de votre utilisateur postgresql ci-dessous nous utilisons ocluser
- DB_PASSWORD : mot de passe de votre utilisateur postgresql
- POSTGRES_PASSWORD : mot de passe de l'utilisateur "postgres"

Créer et lancer les conteneurs Docker :
```
docker-compose up -d
```

Vérifier que la page d'accueil du site s’affiche bien en allant sur l'IP ou le DSN de votre site. Attention, à ce stade la base de donnée n'existe pas donc seule la page d'accueil marche.

#### Mise à jour de la base 

Avec la commande ```docker ps``` récupérer l'id du Docker postgres et s'y connecter avec :
```
docker exec -it idDuDockerPostgres bash
```

Une fois sur le terminal se connecter à postgresql.
```
psql -d postgres -U postgres
```

Créer l'utilisateur ocluser avec un mot de passe et l'utiliser pour créer la base de donnée

```
CREATE USER ocluser WITH PASSWORD votremotdepasse;
ALTER USER ocluser WITH NOCREATEDB NOCREATEROLE;
CREATE DATABASE ocldb OWNER = ocluser;
```
Sortir de la session postgres avec ```.q``` et du terminal du docker avec ```exit```.

Mettre à jour le fichier .env avec le mot de passe du l'utilisateur ocluser. Les conteneurs Docker doivent être redémarrés pour prendre en compte les changement du fichier .env 

Se connecter au docker de l'application.
```
docker exec -it idDuDockerApp /bin/sh
```
Une fois sur le terminal, effectuer les migrations.
```
python manage.py migrate
```
Charger les données.
```
python manage.py loaddata datadump.json
```

**Le site est maintenant opérationnel.**

#### Automatisation de la mise à jour du site

Nous allons maintenant automatiser la mise à jour du Docker de l'application quand le repository est mis à jour. Les scripts décrits ci-dessous peuvent être trouvés dans le répertoire /deployment.  

Dans le répertoire home/ec2-user créer un fichier deploy.sh :
```
#!/bin/bash
# script run when webhooks from Docker Hub detected
# get the new application image and update the docker accordingly

echo "Received webhook event."

# Pull the application new version
docker pull "yourDockerHubRepositoryReference":latest

# Restart the Docker containers using the specific image
docker-compose -f compose.yml up -d --no-deps oc_lettings_site
```
Ce script sera utilisé pour mettre à jour le Docker de l'application. "yourDockerHubRepositoryReference" correspond à la reference que vous avez utilisée dans .circleci/config.yml à la place de chpancrate/ocrp13-pgsql.

Rendre le script executable ```sudo chmod +x deploy.sh```

Sur le site du Docker hub dans le repository ajouter un webhook vers votre instance, il sera déclenché à chaque création d'une nouvelle image.

- payload url : http://your-ec2-instance-ip:8001

De retour sur l'instance EC2 installer nc pour écouter le Webhook.
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
Toutes les actions sont logguées dans webhook_receiver.log

Rendre le script executable ```sudo chmod +x webhook_receiver.sh```

Lancer le script ```./webhook_receiver.sh &```

Lors de la mise à jour de l'image, le Docker de l'application sera maintenant mis à jour.

## Documentation

Une documentation complète (en anglais) peut-être trouvée ici : https://ocrpy-project13.readthedocs.io/en/latest/index.html