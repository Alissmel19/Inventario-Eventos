from .models import ReservaHabitacionWeb


def contador_reservas_web(request):
    if request.user.is_authenticated:
        pendientes = ReservaHabitacionWeb.objects.filter(
            estado="Pendiente"
        ).count()
    else:
        pendientes = 0

    return {
        "reservas_web_pendientes": pendientes
    }