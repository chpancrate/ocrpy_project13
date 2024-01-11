from django.shortcuts import render

from profiles.models import Profile


def index(request):
    """
    Display the profiles index page using the profiles/index.html template.
    Get the list of all profiles to display them on the page

    parameters
    ----------
    request : HttpRequest
        http request to be processed

    return
    ------
    the rendered web page
    """

    profiles_list = Profile.objects.all()
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles/index.html', context)


def profile(request, username):
    """
    Display the details of one user profile using the profiles/profile.html template.
    Get the details of the profile using the username contained in the url

    parameters
    ----------
    request : HttpRequest
        http request to be processed
    username : str
        name of the user to be displayed retrieved from the url

    return
    ------
    the rendered web page
    """

    profile = Profile.objects.get(user__username=username)
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)
