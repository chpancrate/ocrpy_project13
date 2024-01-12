Tests
=====

Unit Tests
----------
Unit tests can be run using pytest.

.. code-block::

    source venv/bin/activate
    pytest

Here is the list of unit tests by application.

Lettings
""""""""
.. automodule:: lettings.tests.tests_models
   :members:
   :noindex:

.. automodule:: lettings.tests.tests_urls
   :members:
   :noindex:

.. automodule:: lettings.tests.tests_views
   :members:
   :noindex:

Profiles
""""""""
.. automodule:: profiles.tests.tests_models
   :members:
   :noindex:

.. automodule:: profiles.tests.tests_urls
   :members:
   :noindex:

.. automodule:: profiles.tests.tests_views
   :members:
   :noindex:

OC Lettings Site
""""""""""""""""
.. automodule:: oc_lettings_site.tests.tests_urls
   :members:
   :noindex:

.. automodule:: oc_lettings_site.tests.tests_views
   :members:
   :noindex:

Functional Tests
-----------------
Functional tests can be launched using pytest and selenium:

.. code-block::

    source venv/bin/activate
    pytest ./oc_lettings_site/tests/functional_test.py

Below are the functional tests :

.. automodule:: oc_lettings_site.tests.functional_test
   :members:
   :noindex:
   :exclude-members: setUp, tearDown

