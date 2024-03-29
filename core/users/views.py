from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from avatar_generator import Avatar
from .forms import RegisterForm

User = get_user_model()


def sign_up(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('rooms:home')
    return render(request, 'registration/sign-up.html', {'form': form})


@login_required
@cache_control(max_age=3600)
def get_avatar(request, username):
    avatar = Avatar.generate(64, username, 'PNG')
    response = HttpResponse(avatar, content_type='image/png')
    return response 
