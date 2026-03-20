from django.shortcuts import render


from django.shortcuts import redirect


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        return redirect("login")
