"""inspiral URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import settings
from control_panel.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^login_as_anonymous/$', LoginAsAnonymous.as_view(), name='login_as_anonymous'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^edit_user/(?P<user_id>\d+)/$', UserView.as_view(), name='edit_user'),

    url(r'^members/$', MembersView.as_view(), name='members'),
    url(r'^member/(?P<pk>\d+)/$', MemberView.as_view(), name='member'),
    url(r'^member/delete/(?P<pk>\d+)/$', DeleteMemberView.as_view(), name='delete_member'),

    url(r'^map/$', MapView.as_view(), name='map'),

    url(r'^trainers/$', TrainersView.as_view(), name='trainers'),
    url(r'^trainer/(?P<pk>\d+)/$', TrainerView.as_view(), name='trainer'),
    url(r'^trainer/create/$', CreateTrainerView.as_view(), name='add_trainer'),
    url(r'^trainer/delete/(?P<pk>\d+)/$', DeleteTrainerView.as_view(), name='delete_trainer'),

    url(r'^groups/$', GroupsView.as_view(), name='groups'),
    url(r'^group/(?P<pk>\d+)/$', GroupView.as_view(), name='group'),
    url(r'^group/create/$', CreateGroupView.as_view(), name='add_group'),
    url(r'^group/delete/(?P<pk>\d+)/$', DeleteGroupView.as_view(), name='delete_group'),

    url(r'^products/$', ProductsView.as_view(), name='products'),
    url(r'^product/(?P<pk>\d+)/$', ProductView.as_view(), name='product'),
    url(r'^product/create/$', CreateProductView.as_view(), name='add_product'),
    url(r'^product/delete/(?P<pk>\d+)/$', DeleteProductView.as_view(), name='delete_product'),

    url(r'^activities/$', ActivitiesView.as_view(), name='activities'),
    url(r'^activity/(?P<pk>\d+)/$', ActivityView.as_view(), name='activity'),
    url(r'^activity/create/$', CreateActivityView.as_view(), name='add_activity'),
    url(r'^activity/delete/(?P<pk>\d+)/$', DeleteActivityView.as_view(), name='delete_activity'),

    url(r'^create/(?P<obj_name>member|trainer|group|product|activity)/$', CreateObjectView.as_view(), name='create'),






    url(r'^group/delete_member/(?P<group_id>\d+)/(?P<member_id>\d+)/(?P<next>\d)/$', DeleteGroupMemberView.as_view(),
        name='delete_group_member'),
    url(r'^group/add_member/(?P<group_id>\d+)/(?P<member_id>\d+)/$', AddGroupMemberView.as_view(),
        name='add_group_member'),
    url(r'^group/add_members/(?P<group_id>\d+)', AddGroupMembersView.as_view(),
        name='add_group_members'),

    url(r'^pass/create/(?P<member_id>\d+)/$', CreatePassView.as_view(), name='create_pass'),
    url(r'^pass/update/(?P<pk>\d+)/$', UpdatePassView.as_view(), name='update_pass'),
    url(r'^pass/delete/(?P<pk>\d+)/$', DeletePassView.as_view(), name='delete_pass'),
    url(r'^pass/update_status/(?P<pk>\d+)/$', UpdatePassStatusView.as_view(), name='update_pass_status'),

    url(r'^pass/add_entry/(?P<pk>\d+)/$', AddPassEntryView.as_view(), name='add_pass_entry'),
    url(r'^pass/delete_entry/(?P<pk>\d+)/$', DeletePassEntryView.as_view(), name='delete_pass_entry'),

    url(r'^show_payments/$', ShowPaymentsView.as_view(), name='show_payments'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
