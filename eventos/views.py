from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import (
    Clientes,
    Eventos,
    Cotizaciones,
    Pagos,
)


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "login.html",
            {
                "error": "Usuario o contraseña incorrectos."
            }
        )

    return render(request, "login.html")


@login_required(login_url="login")
def dashboard(request):

    context = {
        "total_clientes": Clientes.objects.count(),
        "total_eventos": Eventos.objects.count(),
        "total_cotizaciones": Cotizaciones.objects.count(),
        "total_pagos": Pagos.objects.count(),
    }

    return render(request, "dashboard.html", context)


def logout_view(request):

    logout(request)

    return redirect("login")


def nueva_cotizacion(request):
    return render(request, "cotizacioNueva.html")


