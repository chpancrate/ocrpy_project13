import pytest

from django.urls import reverse, resolve
from lettings.models import Letting, Address


@pytest.mark.django_db
def test_lettings_index_url():
    '''
    GIVEN
    WHEN accessing the url /lettings/
    THEN the view lettings:index is called
    '''

    path = reverse('lettings:index')

    assert path == "/lettings/"
    assert resolve(path).view_name == "lettings:index"


@pytest.mark.django_db
def test_lettings_details_url():
    '''
    GIVEN a letting_id
    WHEN accessing the url /lettings/letting_id/
    THEN the view lettings:letting is called
    '''

    test_address = Address.objects.create(number=3,
                                          street='test street',
                                          city='test city',
                                          state='test state',
                                          zip_code=75000,
                                          country_iso_code='FRF')

    Letting.objects.create(title='test letting',
                           address=test_address)
    path = reverse('lettings:letting', kwargs={'letting_id': 1})

    assert path == "/lettings/1/"
    assert resolve(path).view_name == "lettings:letting"
