import pytest

from django.urls import reverse
from django.test import Client
from lettings.models import Letting, Address
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_lettings_index_view():
    '''
    GIVEN a letting

    WHEN accessing lettings/

    THEN the template letting/index.html is displayed
         and the lettings list is displayed
    '''

    client = Client()

    test_address = Address.objects.create(number=3,
                                          street='test street',
                                          city='test city',
                                          state='test state',
                                          zip_code=75000,
                                          country_iso_code='FRF')

    Letting.objects.create(title='test letting',
                           address=test_address)

    path = reverse('lettings:index')

    response = client.get(path)
    content = response.content.decode()

    expected_title = 'test letting'

    assert expected_title in content

    assert response.status_code == 200
    assertTemplateUsed(response, "lettings/index.html")


@pytest.mark.django_db
def test_lettings_details_view():
    '''
    GIVEN a letting

    WHEN accessing lettings/letting_id

    THEN the template letting/letting.html is displayed
         and the letting data are displayed
    '''

    client = Client()

    test_address = Address.objects.create(number=3,
                                          street='test street',
                                          city='test city',
                                          state='test state',
                                          zip_code=75000,
                                          country_iso_code='FRF')

    Letting.objects.create(title='test letting',
                           address=test_address)
    path = reverse('lettings:letting', kwargs={'letting_id': 1})

    response = client.get(path)
    content = response.content.decode()

    expected_street = 'test street'
    expected_city = 'test city'
    expected_state = 'test state'
    expected_zip_code = '75000'
    expected_country_iso_code = 'FRF'
    expected_title = 'test letting'

    assert expected_street in content
    assert expected_city in content
    assert expected_state in content
    assert expected_zip_code in content
    assert expected_country_iso_code in content
    assert expected_title in content

    assert response.status_code == 200
    assertTemplateUsed(response, "lettings/letting.html")
