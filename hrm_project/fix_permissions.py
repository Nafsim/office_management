import re

# Read the file
with open('hrm_app/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entire user_permissions function
old_pattern = r'@admin_required\s+def user_permissions\(request, pk=None\):.*?return render\(request, "hrm/user_permissions\.html", \{.*?\}\)'

new_function = '''@login_required
def user_permissions(request, pk=None):
    if request.user.role != 'super_admin':
        messages.error(request, "You don't have permission to access this page.")
        return redirect("user_list")

    selected_role = request.GET.get("role", "")
    users_for_role = User.objects.filter(role=selected_role) if selected_role else User.objects.none()
    module_choices = UserPermission.MODULE_CHOICES

    if request.method == "POST":
       selected_role = request.POST.get("role", "")
       users_for_role = User.objects.filter(role=selected_role)

       if not selected_role:
           messages.error(request, "Please select a role first.")
           return render(request, "hrm/user_permissions.html", {
               "saved_permissions": {},
               "modules": module_choices,
               "selected_role": "",
               "selected_role_label": "",
               "role_choices": Role.choices,
               "role_user_count": 0,
               "module_choices": module_choices,
               "allowed_menus": [],
           })

       for user in users_for_role:
           for module in PERMISSION_MODULES:
               UserPermission.objects.update_or_create(
                   user=user,
                   module=module,
                   defaults={
                       "can_view": request.POST.get(f"{module}_view") == "on",
                       "can_create": request.POST.get(f"{module}_create") == "on",
                       "can_edit": request.POST.get(f"{module}_edit") == "on",
                       "can_delete": request.POST.get(f"{module}_delete") == "on",
                   }
               )

       RoleMenuPermission.objects.filter(role=selected_role).delete()

       for menu_key, menu_name in module_choices:
           if request.POST.get(f"menu_{menu_key}"):
               RoleMenuPermission.objects.create(
                   role=selected_role,
                   menu=menu_key,
                   is_allowed=True
               )

       messages.success(request, "Permissions updated successfully.")
       return redirect(f"/employees/permissions/?role={selected_role}")

    selected_user = users_for_role.first()
    saved_permissions = {}
    if selected_user:
        saved_permissions = {
            p.module: p
            for p in UserPermission.objects.filter(user=selected_user)
        }

    allowed_menus = RoleMenuPermission.objects.filter(
        role=selected_role,
        is_allowed=True
    ).values_list('menu', flat=True)

    selected_role_label = dict(Role.choices).get(selected_role, "") if selected_role else ""

    return render(request, "hrm/user_permissions.html", {
        "saved_permissions": saved_permissions,
        "modules": module_choices,
        "selected_role": selected_role,
        "selected_role_label": selected_role_label,
        "role_choices": Role.choices,
        "role_user_count": users_for_role.count(),
        "module_choices": module_choices,
        "allowed_menus": allowed_menus,
    })'''

content = re.sub(old_pattern, new_function, content, flags=re.DOTALL)

# Write back
with open('hrm_app/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed user_permissions function")
