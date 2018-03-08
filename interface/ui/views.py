from django.shortcuts import render, HttpResponse

def home_view(req):
    return render(req, 'ui/home.html', {})
