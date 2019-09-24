from django.conf import settings
from control_panel.forms import MemberForm, TrainerForm, ProductForm, ActivityForm, GroupForm


def google_api_key(request):
    return {'google_api_key': settings.GOOGLE_API_KEY}


def forms(request):
    return {'member_form': MemberForm(),
            'trainer_form': TrainerForm(),
            'product_form': ProductForm(),
            'activity_form': ActivityForm(),
            'group_form': GroupForm()}
