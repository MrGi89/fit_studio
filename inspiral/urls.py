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
from django.urls import include, path
from django.conf.urls import url
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from control_panel.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^login_as_anonymous/$', LoginAsAnonymous.as_view(), name='login_as_anonymous'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^settings/(?P<user_id>\d+)/$', SettingsView.as_view(), name='settings'),
    url(r'^map/$', MapView.as_view(), name='map'),
    url(r'^studio-location/$', GetLocationView.as_view(), name='location'),

    # LISTS
    url(r'^members/$', MembersView.as_view(), name='members'),
    url(r'^trainers/$', TrainersView.as_view(), name='trainers'),
    url(r'^groups/$', GroupsView.as_view(), name='groups'),
    url(r'^products/$', ProductsView.as_view(), name='products'),

    # SINGLE PAGES
    url(r'^member/(?P<pk>\d+)/$', MemberView.as_view(), name='member'),
    url(r'^trainer/(?P<pk>\d+)/$', TrainerView.as_view(), name='trainer'),
    url(r'^group/(?P<pk>\d+)/$', GroupView.as_view(), name='group'),
    url(r'^calendar/$', CalendarView.as_view(), name='calendar'),

    # CUD
    url(r'^create/(?P<obj_name>member|trainer|group|product|pass)/$',
        view=CreateObjectView.as_view(),
        name='create'),
    url(r'^update/(?P<obj_name>member|trainer|group|product|pass|user|studio)/(?P<pk>\d+)/$',
        view=UpdateObjectView.as_view(),
        name='update'),
    url(r'^delete/(?P<redirect_to>members|trainers|groups|products|pass)/(?P<pk>\d+)/$',
        view=DeleteObjectView.as_view(),
        name='delete'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
