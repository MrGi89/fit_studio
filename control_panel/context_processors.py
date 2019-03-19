from inspiral.local_settings import GOOGLE_API_KEY


def google_api_key(request):
    return {'google_api_key': GOOGLE_API_KEY}
