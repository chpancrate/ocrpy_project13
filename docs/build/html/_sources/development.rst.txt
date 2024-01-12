Development Environment setup
=============================

Place yourself in the directory where you want to work.

Code cloning
------------
The code can be cloned from https://github.com/chpancrate/ocrpy_project13 using the command

.. code-block::

    git clone https://github.com/chpancrate/ocrpy_project13.git

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
