from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


app_name = 'accounts'


urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html',
            redirect_authenticated_user=True,
        ),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='shopapp:index',
        ),
        name='logout',
    ),
    path(
        'register/',
        views.register,
        name='register',
    ),
    path(
        'about-me/',
        views.about_me,
        name='about_me',
    ),
    path(
        'users/',
        views.users_list,
        name='users_list',
    ),
    path(
        'users/<int:user_id>/',
        views.profile_detail,
        name='profile_detail',
    ),
    path(
        'users/<int:user_id>/update/',
        views.profile_update,
        name='profile_update',
    ),
]
