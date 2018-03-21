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
from control_panel.views import HomeView, LoginView, LogoutView, EditUserView, ShowMembersView, ShowMemberView, \
    CreateMemberView, UpdateMemberView, DeleteMemberView, ShowTrainersView, CreateTrainerView, \
    UpdateTrainerView, DeleteTrainerView


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^edit_user/(?P<user_id>\d+)/$', EditUserView.as_view(), name='edit_user'),

    url(r'^show_members/$', ShowMembersView.as_view(), name='show_members'),
    url(r'^show_member/(?P<pk>\d+)/$', ShowMemberView.as_view(), name='show_member'),
    url(r'^member/create/$', CreateMemberView.as_view(), name='create_member'),
    url(r'^member/update/(?P<pk>\d+)/$', UpdateMemberView.as_view(), name='update_member'),
    url(r'^member/delete/(?P<pk>\d+)/$', DeleteMemberView.as_view(), name='delete_member'),


    url(r'^show_trainers/$', ShowTrainersView.as_view(), name='show_trainers'),
    url(r'^trainer/create/$', CreateTrainerView.as_view(), name='create_trainer'),
    url(r'^trainer/update/(?P<pk>\d+)/$', UpdateTrainerView.as_view(), name='update_trainer'),
    url(r'^trainer/delete/(?P<pk>\d+)/$', DeleteTrainerView.as_view(), name='delete_trainer'),

]

