from django.shortcuts import render


def index(request):
    """
    Display the home age from the site.

    parameters
    ----------
    request : HttpRequest
        http request to be processed

    return
    ------
    the rendered web page
    """
    return render(request, 'index.html')
