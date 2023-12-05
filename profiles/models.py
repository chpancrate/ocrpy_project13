from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    A class used to represent a user profile

    attributes
    ----------
    user : User
        django user
    favorite_city : str
        user's favorite city name
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        """ prints username to identify the profile """

        return self.user.username
