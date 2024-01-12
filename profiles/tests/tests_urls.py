import pytest

from django.urls import reverse, resolve
from profiles.models import Profile
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_profiles_index_url():
    '''
    GIVEN

    WHEN accessing the url /profiles/

    THEN the view profiles:index is called
    '''

    path = reverse('profiles:index')

    assert path == "/profiles/"
    assert resolve(path).view_name == "profiles:index"


@pytest.mark.django_db
def test_profile_details_url():
    '''
    GIVEN a username

    WHEN accessing the url /profiles/username/

    THEN the view letting is called
    '''

    test_user = User.objects.create(username='TestUser',
                                    password='password',
                                    email='test@email.com')

    Profile.objects.create(user=test_user,
                           favorite_city='test city')
    path = reverse('profiles:profile', kwargs={'username': 'TestUser'})

    assert path == "/profiles/TestUser/"
    assert resolve(path).view_name == "profiles:profile"
