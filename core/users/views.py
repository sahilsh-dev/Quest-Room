from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from .forms import RegisterForm

User = get_user_model()

def sign_up(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('rooms:home')
    return render(request, 'registration/sign-up.html', {'form': form})
