import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrm_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from hrm_app.models import Employee, Department, Designation

User = get_user_model()

# Create demo users
demo_users = [
    {'username': 'admin', 'email': 'admin@gmail.com', 'first_name': 'Admin', 'last_name': 'User', 'role': 'super_admin'},
    {'username': 'manager', 'email': 'manager@gmail.com', 'first_name': 'Manager', 'last_name': 'User', 'role': 'manager'},
    {'username': 'employee', 'email': 'employee@gmail.com', 'first_name': 'Employee', 'last_name': 'User', 'role': 'employee'},
]

# Get or create default department and designation
dept, _ = Department.objects.get_or_create(name='General')
desig, _ = Designation.objects.get_or_create(title='Staff', defaults={'department': dept, 'level': 'L1'})

for user_data in demo_users:
    username = user_data['username']
    email = user_data['email']
    
    # Delete existing user if exists
    if User.objects.filter(username=username).exists():
        User.objects.filter(username=username).delete()
        print(f"Deleted existing user '{username}'...")
    
    # Create user
    user = User.objects.create_user(
        username=username,
        email=email,
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        password='12345',
    )
    user.role = user_data['role']
    user.save()
    
    # Create employee profile
    Employee.objects.create(
        user=user,
        emp_id=f'EMP{username.upper()}001',
        department=dept,
        designation=desig,
        status='Active',
        join_date='2024-01-01'
    )
    
    print(f"Created user: {username} (password: 12345)")

print("\nDemo accounts created successfully!")
print("Username: admin, Password: 12345")
print("Username: manager, Password: 12345")
print("Username: employee, Password: 12345")
