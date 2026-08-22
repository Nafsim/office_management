import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrm_project.settings')
django.setup()

from hrm_app.models import User, UserPermission, RoleMenuPermission

# Get all users except super_admin
users = User.objects.exclude(role='super_admin')
print(f'Found {users.count()} users to initialize')

for user in users:
    # Delete existing permissions for this user
    UserPermission.objects.filter(user=user).delete()
    
    # Copy role default permissions to user-specific permissions
    role_perms = RoleMenuPermission.objects.filter(role=user.role)
    
    for rp in role_perms:
        UserPermission.objects.create(
            user=user,
            module=rp.menu,
            can_view=rp.can_view,
            can_create=rp.can_create,
            can_edit=rp.can_edit,
            can_delete=rp.can_delete,
        )
    
    print(f'Initialized permissions for {user.username} ({user.role})')

print('Done!')
