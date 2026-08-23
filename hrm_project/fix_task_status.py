import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrm_project.settings')
django.setup()

from django.db import connection

# First, manually create the TaskStatus table
with connection.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hrm_app_taskstatus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL,
            color VARCHAR(7) DEFAULT '#6B7280',
            "order" INTEGER DEFAULT 0,
            active BOOLEAN DEFAULT 1,
            project_id INTEGER NOT NULL,
            FOREIGN KEY (project_id) REFERENCES hrm_app_project (id)
        )
    """)
    print('Created hrm_app_taskstatus table')

# Now create the status_id column in hrm_app_task
with connection.cursor() as cursor:
    # Check if status_id column exists
    cursor.execute("PRAGMA table_info(hrm_app_task)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'status_id' not in columns:
        cursor.execute("ALTER TABLE hrm_app_task ADD COLUMN status_id INTEGER")
        print('Added status_id column to hrm_app_task')
    else:
        print('status_id column already exists')

# Now import models and create default statuses
from hrm_app.models import Task, TaskStatus, Project

# Get all projects
projects = Project.objects.all()

# For each project, create default TaskStatus records
for project in projects:
    # Create only the 3 default statuses
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
    
    print(f'Created default statuses for project: {project.name}')

# Now fix existing tasks - get their current status as string
with connection.cursor() as cursor:
    # Get the old status values from the database
    cursor.execute("SELECT id, status FROM hrm_app_task")
    rows = cursor.fetchall()
    
    for task_id, old_status in rows:
        if old_status and not str(old_status).isdigit():  # If it's a string status, not an ID
            # Find the corresponding TaskStatus for the task's project
            task = Task.objects.filter(id=task_id).first()
            if task and task.project:
                status_obj = TaskStatus.objects.filter(project=task.project, name=old_status).first()
                if status_obj:
                    cursor.execute(
                        "UPDATE hrm_app_task SET status_id = %s WHERE id = %s",
                        [status_obj.id, task_id]
                    )
                    print(f'Updated task {task_id}: {old_status} -> {status_obj.name} (ID: {status_obj.id})')

print('Done! Now run: python manage.py migrate --fake')
