from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileUpdateForm
from .models import Profile


def can_edit_profile(request_user, profile_user):
    return (
        request_user.is_staff
        or request_user.pk == profile_user.pk
    )


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shopapp:index')
    else:
        form = UserCreationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form},
    )


@login_required
def about_me(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
    )

    return render(
        request,
        'accounts/about_me.html',
        {
            'profile_user': request.user,
            'profile': profile,
        },
    )


@login_required
def users_list(request):
    users = User.objects.select_related('profile').order_by(
        'username',
    )

    return render(
        request,
        'accounts/users_list.html',
        {'users': users},
    )


@login_required
def profile_detail(request, user_id):
    profile_user = get_object_or_404(
        User.objects.select_related('profile'),
        pk=user_id,
    )

    profile, _ = Profile.objects.get_or_create(
        user=profile_user,
    )

    return render(
        request,
        'accounts/profile_detail.html',
        {
            'profile_user': profile_user,
            'profile': profile,
            'can_edit_profile': can_edit_profile(
                request.user,
                profile_user,
            ),
        },
    )


@login_required
def profile_update(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)

    profile, _ = Profile.objects.get_or_create(
        user=profile_user,
    )

    if not can_edit_profile(request.user, profile_user):
        return HttpResponseForbidden(
            'You do not have permission to edit this profile.'
        )

    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():
            form.save()

            return redirect(
                'accounts:profile_detail',
                user_id=profile_user.pk,
            )
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(
        request,
        'accounts/profile_update.html',
        {
            'profile_user': profile_user,
            'profile': profile,
            'form': form,
        },
    )
