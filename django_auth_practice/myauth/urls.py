from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'myauth'

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='myauth/login.html',
            redirect_authenticated_user=True,
        ),
        name='login',
    ),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    path('', views.index, name='index'),

    path('cookie/get/', views.get_cookie, name='get_cookie'),
    path('cookie/set/', views.set_cookie, name='set_cookie'),

    path('session/get/', views.get_session, name='get_session'),
    path('session/set/', views.set_session, name='set_session'),
]