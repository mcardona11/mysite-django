from django.http import HttpResponse
# pàgina que surt al clicar website
def home(request):
    return HttpResponse("<h2>benvinguts al meu site</h2>")
