from django.http import HttpResponse

def accueil(request):
    return HttpResponse("Bienvenue sur la page d'accueil!")