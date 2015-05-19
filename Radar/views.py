from django.shortcuts import render
#from django.http import HttpResponse, HttpResponseNotFound

def radarView(request):
    return render(request, 'radar.html', {})