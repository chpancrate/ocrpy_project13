import pytest

from lettings.models import Letting, Address


@pytest.mark.django_db
def test_letting_str():
    '''
    GIVEN a Letting object
    WHEN using the str function on the letting
    THEN the __str__ format is returned
    '''

    test_address = Address.objects.create(number=3,
                                          street='test street',
                                          city='test city',
                                          state='test state',
                                          zip_code=75000,
                                          country_iso_code='FRF')

    test_letting = Letting.objects.create(title='test letting',
                                          address=test_address)

    assert str(test_letting) == 'test letting'


@pytest.mark.django_db
def test_address_str():
    '''
    GIVEN an Address object
    WHEN using the str function on the address
    THEN the __str__ format is returned
    '''

    test_address = Address.objects.create(number=3,
                                          street='test street',
                                          city='test city',
                                          state='test state',
                                          zip_code=75000,
                                          country_iso_code='FRF')

    assert str(test_address) == '3 test street'
