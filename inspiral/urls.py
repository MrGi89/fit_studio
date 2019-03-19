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
from control_panel.views import HomeView, LoginView, LogoutView, UserView, MembersView, MemberView, \
    CreateMemberView, DeleteMemberView, TrainersView, CreateTrainerView, \
    UpdateTrainerView, DeleteTrainerView, ProductsView, CreateProductView, UpdateProductView, DeleteProductView, \
    CreatePassView, DeletePassView, UpdatePassView, UpdatePassStatusView, AddPassEntryView, DeletePassEntryView, \
    ShowScheduleView, ShowGroupsView, DeleteGroupMemberView, AddGroupMemberView, AddGroupMembersView, CreateGroupView, \
    DeleteGroupView, UpdateGroupView, ShowPaymentsView, LoginAsAnonymous, MapView, TrainerView

from control_panel.apiviews import RestMemberView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^edit_user/(?P<user_id>\d+)/$', UserView.as_view(), name='edit_user'),
    url(r'^tester_login/$', LoginAsAnonymous.as_view(), name='tester_login'),

    url(r'^members/$', MembersView.as_view(), name='members'),
    url(r'^member/(?P<pk>\d+)/$', MemberView.as_view(), name='member'),
    url(r'^rest/member/(?P<pk>\d+)/$', RestMemberView.as_view(), name='rest-member'),

    url(r'^map/$', MapView.as_view(), name='map'),

    url(r'^trainers/$', TrainersView.as_view(), name='trainers'),
    url(r'^trainer/(?P<pk>\d+)/$', TrainerView.as_view(), name='trainer'),




    url(r'^member/create/$', CreateMemberView.as_view(), name='create_member'),
    url(r'^member/update/(?P<pk>\d+)/$', RestMemberView.as_view(), name='update_member'),
    url(r'^member/delete/(?P<pk>\d+)/$', DeleteMemberView.as_view(), name='delete_member'),

    url(r'^trainer/create/$', CreateTrainerView.as_view(), name='create_trainer'),
    url(r'^trainer/update/(?P<pk>\d+)/$', UpdateTrainerView.as_view(), name='update_trainer'),
    url(r'^trainer/delete/(?P<pk>\d+)/$', DeleteTrainerView.as_view(), name='delete_trainer'),

    url(r'^products/$', ProductsView.as_view(), name='products'),
    url(r'^product/create/$', CreateProductView.as_view(), name='create_product'),
    url(r'^product/update/(?P<pk>\d+)/$', UpdateProductView.as_view(), name='update_product'),
    url(r'^product/delete/(?P<pk>\d+)/$', DeleteProductView.as_view(), name='delete_product'),

    url(r'^groups/$', ShowGroupsView.as_view(), name='groups'),
    url(r'^group/create/$', CreateGroupView.as_view(), name='create_group'),
    url(r'^group/update/(?P<pk>\d+)/$', UpdateGroupView.as_view(), name='update_group'),
    url(r'^group/delete/(?P<pk>\d+)/$', DeleteGroupView.as_view(), name='delete_group'),

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


    url(r'^show_schedule/$', ShowScheduleView.as_view(), name='show_schedule'),
    url(r'^show_payments/$', ShowPaymentsView.as_view(), name='show_payments'),


]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
