from inspiral.local_settings import GOOGLE_API_KEY
from control_panel.forms import MemberForm


def google_api_key(request):
    return {'google_api_key': GOOGLE_API_KEY}


def forms(request):
    return {'member_form': MemberForm()}
