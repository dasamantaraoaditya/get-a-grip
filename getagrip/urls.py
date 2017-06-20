"""getagrip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf.urls import include, url
from django.contrib import admin
from getagrip_app import views, getagrip_crud

urlpatterns = [
    url(r'', include('django.contrib.auth.urls')),

    url(r'^getagrip/', include('getagrip_app.getagrip_urls')),
    url(r'^Logout/', views.logout_view, name='logout'),
    url(r'^$', views.index, name='index'),
    url(r'^successful-register/', views.successfulRegister, name='successful-register'),

    url(r'^register/$', getagrip_crud.UserFormView.as_view(), name='register'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^all_user/$', getagrip_crud.UserListView.as_view(), name='display_all_user'),
    url(r'^users/(?P<pk>[0-9]+)/$', getagrip_crud.UserDetailView.as_view(), name='user_detail_view'),
    url(r'^users/(?P<pk>[0-9]+)/update$', getagrip_crud.UserUpdateView.as_view(), name='user_update_view'),
    url(r'^users/(?P<pk>[0-9]+)/delete$', getagrip_crud.UserDeleteView.as_view(), name='user_delete_view'),

]
