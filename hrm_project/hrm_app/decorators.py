from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


# ── Role checks ──────────────────────────────────────────────────────────────
def role_required(*roles):
    """Decorator: restrict view to users with one of the given roles."""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            if request.user.role not in roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def admin_required(view_func):
    return role_required('super_admin')(view_func)


def manager_or_admin(view_func):
    return role_required('super_admin', 'manager')(view_func)


# ── CBV Mixins ───────────────────────────────────────────────────────────────
class RoleRequiredMixin(LoginRequiredMixin):
    allowed_roles = []  # override in subclass

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated:
            return result
        if self.allowed_roles and request.user.role not in self.allowed_roles:
            raise PermissionDenied
        return result


class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['super_admin']


class ManagerOrAdminMixin(RoleRequiredMixin):
    allowed_roles = ['super_admin', 'manager']