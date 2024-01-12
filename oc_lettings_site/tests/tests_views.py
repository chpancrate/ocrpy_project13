import pytest

from django.urls import reverse
from django.test import Client
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_oc_lettings_site_index_view():
    '''
    GIVEN

    WHEN accessing the url /

    THEN the template index.html is displayed
         and the site home page is displayed
    '''

    client = Client()

    path = reverse('index')

    response = client.get(path)
    content = response.content.decode()

    expected_title = 'Welcome to Holiday Homes'

    assert expected_title in content

    assert response.status_code == 200
    assertTemplateUsed(response, "index.html")
