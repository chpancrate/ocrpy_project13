Development Environment setup
=============================

Place yourself in the directory where you want to work.

Code cloning
------------
The code can be found here : https://github.com/chpancrate/ocrpy_project13

You need to fork it, then you can clone it using the command.

.. code-block::

    git clone https://github.com/yourrepository/yourproject.git

Virtual environment creation and activation
-------------------------------------------
In unix

.. code-block::

    python -m venv venv
    source venv/bin/activate 

In windows

.. code-block::

    python -m venv venv
    .\venv\Scripts\activate

To deactivate the environment

.. code-block::

    deactivate

Environment variables set-up
----------------------------
The environment variables are defined by the package python-dotenv using a file .env. Create the .env file in the root of your project with the following content :

.. code-block::

    # sentry configuration
    SENTRY_DSN= "your Sentry project DSN"

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY= "secret key to define and keep secret"

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG=False

    ALLOWED_HOSTS=localhost,127.0.0.1,nginx

    # database configuration
    DB_ENGINE=django.db.backends.sqlite3
    DB_NAME=oc-lettings-site.sqlite3

This setup will allow to use the sqlite development database. 

To launch the web site
----------------------

.. code-block::

    source venv/bin/activate
    pip install --requirement requirements.txt
    python manage.py runserver

The site can be accessed with http://localhost:8000 in a web browser.

The website administration is reached with : http://localhost:8000/admin

User : admin

Password : Abc1234!

Linting
-------
The linting uses the modules Flake8. To run it :

.. code-block::

    source venv/bin/activate
    flake8
