from django.conf import settings


def store_info(_request):
    """Expose store contact and location details to templates."""
    return {
        "store_info": {
            "name": getattr(settings, "STORE_NAME", "Family Hardware & Supplies"),
            "map_url": getattr(settings, "STORE_MAP_URL", ""),
            "address": getattr(settings, "STORE_ADDRESS", ""),
            "phone": getattr(settings, "STORE_PHONE", ""),
            "email": getattr(settings, "STORE_EMAIL", ""),
            "hours": getattr(settings, "STORE_HOURS", ""),
        }
    }
