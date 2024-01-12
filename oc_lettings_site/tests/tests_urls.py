import pytest

from django.urls import reverse, resolve


@pytest.mark.django_db
def test_oc_lettings_site_index_url():
    '''
    GIVEN

    WHEN accessing the url /

    THEN the view index is called
    '''

    path = reverse('index')

    assert path == "/"
    assert resolve(path).view_name == "index"
