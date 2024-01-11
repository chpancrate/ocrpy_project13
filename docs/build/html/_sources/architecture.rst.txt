Architecture
============

Database
--------

Schema
""""""
The database structure is the following :

.. image:: ./images/database.png

Models
""""""
The Django models describing the tables are:

.. automodule:: lettings.models
   :members:
   :exclude-members: DoesNotExist, MultipleObjectsReturned
.. automodule:: profiles.models
   :members:
   :exclude-members: DoesNotExist, MultipleObjectsReturned

Modules
-------
The site is rendered by the following Django views :

.. automodule:: lettings.views
   :members:

.. automodule:: profiles.views
   :members:

.. automodule:: oc_lettings_site.views
   :members:
