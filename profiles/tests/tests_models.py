import pytest

from profiles.models import Profile
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_profile_str():
    '''
    GIVEN a Profile object

    WHEN using the str function on the profile

    THEN the __str__ format is returned
    '''

    test_user = User.objects.create(username='TestUser',
                                    first_name='Test Firstname',
                                    last_name='Test Lastname',
                                    password='password',
                                    email='test@email.com')

    test_profile = Profile.objects.create(user=test_user,
                                          favorite_city='test city')

    assert str(test_profile) == 'TestUser'
