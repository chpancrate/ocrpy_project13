Architecture
============

The site is composed of the main application oc_lettings_site which uses two services:

- lettings, which handles the lettings
- profiles, which handles the users profiles 

.. image:: ./images/modules.png

Database
--------

Schema
""""""
The database structure is the following :

.. image:: ./images/database.png

Models
""""""
The Django models implementing the structure above are :

.. automodule:: lettings.models
   :members:
   :exclude-members: DoesNotExist, MultipleObjectsReturned
.. automodule:: profiles.models
   :members:
   :exclude-members: DoesNotExist, MultipleObjectsReturned

Modules
-------
The various parts of the site are implemented with the following views functions:

Lettings
""""""""
.. automodule:: lettings.views
   :members:

Profiles
""""""""
.. automodule:: profiles.views
   :members:

OC Lettings Site
""""""""""""""""
.. automodule:: oc_lettings_site.views
   :members:
