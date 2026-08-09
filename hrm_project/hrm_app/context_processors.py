from .models import RoleMenuPermission

def role_menu_permissions(request):
    allowed_menus = []

    if request.user.is_authenticated:
        if request.user.role == "super_admin":
          allowed_menus = []         
        else:
            allowed_menus = list(
                RoleMenuPermission.objects.filter(
                    role=request.user.role,
                    is_allowed=True
                ).values_list("menu", flat=True)
            )

    return {
        "allowed_menus": allowed_menus
    }