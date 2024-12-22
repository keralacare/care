from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from maintenance_mode.decorators import (
    force_maintenance_mode_off,
)


def app_version(request):
    return JsonResponse({"version": settings.APP_VERSION})


def home_view(request):
    return render(request, "pages/home.html")


@force_maintenance_mode_off
def ping(request):
    return JsonResponse({"status": "OK"})
