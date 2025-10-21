from django.http import HttpResponse

def home(request):
    return HttpResponse("<h2>Benvinguts al meu site</h2>")
