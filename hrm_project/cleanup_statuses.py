import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrm_project.settings')
django.setup()

from hrm_app.models import TaskStatus, Project, Task

# Get all projects
projects = Project.objects.all()

# For each project, keep only the 3 default statuses
for project in projects:
    # Delete all statuses that are not in the default list
    default_status_names = ['To Do', 'In Progress', 'Completed']
    
    # Get all statuses for this project
    all_statuses = TaskStatus.objects.filter(project=project)
    
    # First, reassign tasks from non-default statuses to "To Do"
    todo_status = TaskStatus.objects.filter(project=project, name='To Do').first()
    
    deleted_count = 0
    for status in all_statuses:
        if status.name not in default_status_names:
            # Reassign tasks to "To Do" status
            tasks_to_reassign = Task.objects.filter(status=status)
            if tasks_to_reassign.exists() and todo_status:
                tasks_to_reassign.update(status=todo_status)
                print(f'Reassigned {tasks_to_reassign.count()} tasks from "{status.name}" to "To Do"')
            
            print(f'Deleting status: {status.name} from project {project.name}')
            status.delete()
            deleted_count += 1
    
    # Ensure the 3 default statuses exist
    default_statuses = [
        ('To Do', '#6B7280', 0),
        ('In Progress', '#3B82F6', 1),
        ('Completed', '#10B981', 2),
    ]
    
    for name, color, order in default_statuses:
        TaskStatus.objects.get_or_create(
            project=project,
            name=name,
            defaults={'color': color, 'order': order}
        )
    
    print(f'Project {project.name}: Deleted {deleted_count} extra statuses, ensured 3 default statuses exist')

print('Done! All projects now have exactly 3 statuses: To Do, In Progress, Completed')
