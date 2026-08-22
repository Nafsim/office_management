from .models import UserPermission

def role_menu_permissions(request):
    allowed_menus = []

    if request.user.is_authenticated:
        if request.user.role == "super_admin":
          allowed_menus = []         
        else:
            # Use user-specific permissions instead of role-based
            allowed_menus = list(
                UserPermission.objects.filter(
                    user=request.user,
                    can_view=True
                ).values_list("module", flat=True)
            )

    return {
        "allowed_menus": allowed_menus
    }