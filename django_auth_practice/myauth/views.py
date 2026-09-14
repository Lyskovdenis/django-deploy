from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:index')


def index(request):
    return render(request, 'myauth/index.html')


def get_cookie(request):
    username = request.COOKIES.get('username', 'Guest')
    return HttpResponse(f'Cookie username value: {username}')


def set_cookie(request):
    response = HttpResponse('Cookie set. Go to read cookie page.')
    response.set_cookie(
        key='username',
        value='Dmitry',
        max_age=60 * 60 * 24,
    )
    return response


def get_session(request):
    username = request.session.get('username', 'Guest')
    return HttpResponse(f'Session username value: {username}')


def set_session(request):
    request.session['username'] = 'Dmitry'
    return HttpResponse('Session set. Go to read session page.')
