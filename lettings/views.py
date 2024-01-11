from django.shortcuts import render

from lettings.models import Letting


def index(request):
    """
    Display the lettings index page using the lettings/index.html template.
    Get the list of all lettings to display them on the page

    parameters
    ----------
    request : HttpRequest
        http request to be processed

    return
    ------
    the rendered web page
    """

    lettings_list = Letting.objects.all()
    context = {'lettings_list': lettings_list}
    return render(request, 'lettings/index.html', context)


def letting(request, letting_id):
    """
    Display the details of one letting using the lettings/letting.html template.
    Get the details of the letting using the letting_id contained in the url

    parameters
    ----------
    request : HttpRequest
        http request to be processed
    letting_id : int
        id of the letting to be displayed retrieved from the url

    return
    ------
    the rendered web page
    """

    letting = Letting.objects.get(id=letting_id)
    context = {
        'title': letting.title,
        'address': letting.address,
    }
    return render(request, 'lettings/letting.html', context)
