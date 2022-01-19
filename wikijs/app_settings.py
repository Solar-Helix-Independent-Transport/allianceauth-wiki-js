from django.conf import settings

WIKIJS_AADISCORDBOT_INTEGRATION = getattr(settings, 'WIKIJS_AADISCORDBOT_INTEGRATION', True)

WIKIJS_API_URL = getattr(settings, 'WIKIJS_API_URL', settings.WIKIJS_URL)