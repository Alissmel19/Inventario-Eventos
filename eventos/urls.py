from django.urls import path
from . import views


urlpatterns = [
    path("", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("cotizaciones/nueva/", views.nueva_cotizacion, name="nueva_cotizacion"),
]