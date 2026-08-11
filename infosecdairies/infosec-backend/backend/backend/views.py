from django.http import JsonResponse


def api_root(request):
    """Simple root endpoint for the backend API"""
    return JsonResponse({
        "status": "ok",
        "message": "Infosec backend is running",
    })
