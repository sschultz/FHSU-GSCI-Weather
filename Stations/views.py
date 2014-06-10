from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.generic import View

class SensorView(View):
    def get(self, request):
        return render_to_response("sensor.html")

def homepage(request):
    return render_to_response("index.html")
