from django.shortcuts import render

# Here we write the functions to render our basic sites, that just render the html template without
# any further functionality
def home_view(request):
    return render(request, 'home.html', {})


def help_view(request):
    return render(request, 'help.html', {})


def contact_view(request):
    return render(request, 'contact.html', {})

def download_view(request):
    return render(request, 'download.html', {})


def navbars_view(request):
    return render(request, 'navbars.html', {})


def REST_API_view(request):
    return render(request, 'REST_API_home.html', {})


def REST_API_error_view(request):
    return render(request, 'REST_API_error.html', {})
