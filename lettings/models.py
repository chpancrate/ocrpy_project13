from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


class Address(models.Model):
    """
    A class used to represent an address of a location

    attributes
    ----------
    number : positive int
        street number of the location
    street : str
        street name of the location
    city : str
        city name of the location
    state : str
        state name of the location
    zip_code : positive int
        zip code of the location
    country_iso_code : str
        iso code of the location's country
    """

    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    class Meta:
        """ define the name displayed in the admin interface """

        verbose_name_plural = 'Adresses'

    def __str__(self):
        """ prints number and street to identify the adress object """

        return f'{self.number} {self.street}'


class Letting(models.Model):
    """
    A class used to represent a place available to rent

    attributes
    ----------
    title : str
        name to document the place
    address : Adress
        address of the place
     """

    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
