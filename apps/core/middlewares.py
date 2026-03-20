from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


class BlockInactiveUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path = request.path

        # ✅ 1. If logged-in but inactive → logout
        if request.user.is_authenticated and not request.user.is_active:
            logout(request)
            messages.error(request, "Your account is inactive.")
            return redirect("login")

        # ✅ 2. Block forgot password for inactive users
        if path == reverse("password_reset") and request.method == "POST":

            email = request.POST.get("email")

            if email:
                try:
                    user = User.objects.get(email=email)

                    if not user.is_active:
                        messages.error(request, "This account is inactive.")
                        return redirect("login")

                except User.DoesNotExist:
                    messages.error(request, "No account found with this email.")
                    return redirect("password_reset")

        return self.get_response(request)
