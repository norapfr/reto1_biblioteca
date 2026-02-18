from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required
def dashboard(request):
    return render(request, "dashboard.html")
