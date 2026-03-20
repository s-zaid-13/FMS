from django.http import HttpResponseForbidden


def admin_required(view_func):

    def wrapper(request, *args, **kwargs):

        if (
            request.user.is_authenticated
            and request.user.role == "admin"
            and request.user.is_active
        ):
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden("Unauthorized")

    return wrapper


def member_required(view_func):

    def wrapper(request, *args, **kwargs):

        if (
            request.user.is_authenticated
            and request.user.role == "member"
            and request.user.is_active
        ):
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden("Unauthorized")

    return wrapper
