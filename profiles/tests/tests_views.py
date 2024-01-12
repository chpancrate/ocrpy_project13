import pytest

from django.urls import reverse
from django.test import Client
from profiles.models import Profile
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_profiles_index_view():
    '''
    GIVEN a profile

    WHEN accessing the url /profiles/

    THEN the template profiles/index.html is displayed
         and the profiles list is displayed
    '''

    client = Client()

    test_user = User.objects.create(username='TestUser',
                                    first_name='Test Firstname',
                                    last_name='Test Lastname',
                                    password='password',
                                    email='test@email.com')

    Profile.objects.create(user=test_user,
                           favorite_city='test city')

    path = reverse('profiles:index')

    response = client.get(path)
    content = response.content.decode()

    expected_username = 'TestUser'

    assert expected_username in content

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/index.html")


@pytest.mark.django_db
def test_lettings_details_view():
    '''
    GIVEN a username

    WHEN accessing the url /profiles/username/

    THEN the template profiles/profile.html is displayed
         and the profile data are displayed
    '''

    client = Client()

    test_user = User.objects.create(username='TestUser',
                                    first_name='Test Firstname',
                                    last_name='Test Lastname',
                                    password='password',
                                    email='test@email.com')

    Profile.objects.create(user=test_user,
                           favorite_city='test city')

    path = reverse('profiles:profile', kwargs={'username': 'TestUser'})

    response = client.get(path)
    content = response.content.decode()

    expected_username = 'TestUser'
    expected_first_name = 'Test Firstname'
    expected_last_name = 'Test Lastname'
    expected_email = 'test@email.com'
    expected_favorite_city = 'test city'

    assert expected_username in content
    assert expected_first_name in content
    assert expected_last_name in content
    assert expected_email in content
    assert expected_favorite_city in content

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/profile.html")
