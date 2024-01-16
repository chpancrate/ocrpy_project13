Deployment
==========

The code repository to be used in this this part is the one created in the :doc:`development` chapter.

Architecture
------------

The production system uses 3 Docker containers :

- nginx
- posgresql
- the django application (OC lettings site)

The containers definition is located in the compose.yml file at the root of the project.

.. image:: ./images/docker_architecture.png

A CI/CD workflow is created with CircleCI to test the code and build an image of the application Docker container
which is then uploaded in a Docker Hub repository.

The containers are loaded on a EC2 t2 micro VM in AWS. Using a webhook setup on Docker Hub, 
the application container is automatically updated each time a new application image is loaded on the Docker Hub repository.

There is also a Sentry logging service.

Accounts are needed for the following sites:

- Sentry (Create a project for the application and note the DSN)
- CircleCI
- Docker Hub (create a repository for  the application)
- AWS

.. figure:: ./images/CICD_Workflow.png

    Summary of the CI/CD workflow

CircleCI
--------

Before setting up the project in CircleCi, the config.yml located in ./.circleci must be updated
by replacing chpancrate/ocrp13-pgsql by your own Docker Hub repository.

During the CircleCI project creation, you just need to give the github repository address.
CircleCI will read the workflow file and launch it.

The first run (launched at creation) will fail because the following environment variables must be defined.

.. list-table::
    :widths: 25 50
    :header-rows: 1

    * - variable
      - value
    * - ALLOWED_HOSTS
      - localhost,127.0.0.1,nginx
    * - DEBUG
      - False
    * - DOCKER_USER
      - your Docker Hub user
    * - DOCKER_PASS
      - your Docker Hub password
    * - SECRET_KEY
      - secret passphrase
    * - SENTRY_DSN
      - DSN from your Sentry project

AWS Installation
----------------

Prerequisite
""""""""""""

You need to create an AWS EC2 t2 micro instance with 20 Gb storage and Amazon linux as OS.
Ensure the following ports are opened to internet traffic :

- 80 : for the website
- 8001 : for the Docker Hub webhook

You can connect to the instance from AWS website.

Using Windows you can also use :

- putty : https://www.putty.org, for terminal connection
- winscp : https://winscp.net/eng/index.php, for file transfer

In the following instructions we will consider that the user used to connect to the AWS instance is ec2-user.
If you are using another user do not forget to replace ec2-user by the proper user.

Docker installation
"""""""""""""""""""

The containers need Docker.

Connect to the instance.

Check the all packages on the instance are uptodate.

.. code-block::

    sudo yum update -y

Install Docker.

.. code-block::

    sudo yum install docker
    sudo usermod -a -G docker ec2-user
    newgrp docker

The last 2 commands allows the user ec2-user to launch Docker without sudo.

To check Docker installation use the command ``docker version``.

The containers are launched with Docker Compose. Here is how to install it:

.. code-block::

    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

Setup permissions in order to execute docker compose:

.. code-block::

    sudo chmod +x /usr/local/bin/docker-compose

To check the Docker Compose installation use ``docker-compose version``.

Start Docker service:

.. code-block::

    sudo service docker start

Setup the service to start at the instance startup:

.. code-block::

    sudo systemctl enable docker

**The instance is now ready for the application.**

Application installation
""""""""""""""""""""""""

Go in home/ec2-user.

From the git hub repository copy the following files :
- compose.yml
- ./nginx

Create a .env file with the following content :

.. code-block::

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

You need to personalize the following variables :

- SENTRY_DSN : DSN of you Sentry project
- SECRET_KEY : secret passphrase used by Django
- ALLOWED_HOSTS : add the IP and DNS from your EC2 instance (do not forget the commas between the values)
- DB_NAME : your database name we use ocldb below
- DB_USER : your postgresql user we ocluser below
- DB_PASSWORD : you postgresql user password
- POSTGRES_PASSWORD : "postgres" user password

Create and start the Docker containers :

.. code-block::

    docker-compose up -d


Check the website homepage by accessing your instance IP or DNS in a browser.
Beware : the database is empty only the homepage works.

Database update 
"""""""""""""""

With the command ``docker ps`` get the id from the postgres container and use it to connect to the container :

.. code-block::

    docker exec -it "PostgresDockerId" bash


Once in the container, connect to postgresql.

.. code-block::

    psql -d postgres -U postgres


Create the user ocluser with a password and create a database.

.. code-block::

    CREATE USER ocluser WITH PASSWORD votremotdepasse;
    ALTER USER ocluser WITH NOCREATEDB NOCREATEROLE;
    CREATE DATABASE ocldb OWNER = ocluser;

Exit from the postgres session with ``.q`` and the container terminal with ``exit``.

If needed, update the .env file with the password and user for the database.

Connect to the application container.

.. code-block::

    docker exec -it "DockerAppId" /bin/sh

Run the migrations.

.. code-block::

    python manage.py migrate

Upload the data.

.. code-block::

    python manage.py loaddata datadump.json


**The site now works.**

Site update automation
""""""""""""""""""""""

The goal is now to automate the update of the application container when a new image is uploaded on the Docker Hub repository.
The scripts described below can be found in ./deployment.  

In /home/ec2-user create a deploy.sh file:

.. code-block::

    #!/bin/bash
    # script run when webhooks from Docker Hub detected
    # get the new application image and update the docker accordingly

    echo "Received webhook event."

    # Pull the application new version
    docker pull "yourDockerHubRepositoryReference":latest

    # Restart the Docker containers using the specific image
    docker-compose -f docker-compose.yml up -d --no-deps oc_lettings_site

This script is used to update the application container.
"yourDockerHubRepositoryReference" is your repository which you used in .circleci/config.yml to replace chpancrate/ocrp13-pgsql.

Make the script executable ``sudo chmod +x deploy.sh``.

In your Docker Hub repository add a webhook to your EC2 instance. It will be launched each time a new image is created.

- payload url : http://your-ec2-instance-ip:8001
- payload : application/json

Back on you EC2 instance, install nc to listen to the Webhook.

.. code-block::

    sudo yum install nc

Create a webhook_receiver.sh file with the following content :

.. code-block::

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

This script uses nc to listen to the webhook and when receiving it, executes the file deploy.sh which update the application Docker container.
All actions are logged in webhook_receiver.log

Make the script executable

.. code-block::

    sudo chmod +x webhook_receiver.sh


Launch the script

.. code-block::

    ./webhook_receiver.sh &

When a new image is created in the Docker Hub repository the application container will now be updated.