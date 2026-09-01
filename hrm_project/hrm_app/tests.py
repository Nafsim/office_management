from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import (
    Attendance,
    Department,
    Designation,
    Employee,
    Notice,
    Project,
    Shift,
    Task,
    TaskStatus,
    TaskStep,
    User,
    UserPermission,
)


class AttendanceViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='secret123', role='super_admin')
        self.department = Department.objects.create(name='Engineering')
        self.designation = Designation.objects.create(title='Engineer', department=self.department)
        self.shift = Shift.objects.create(name='Default', start_time='09:00:00', end_time='18:00:00')

        self.employee = Employee.objects.create(
            user=self.user,
            emp_id='EMP-001',
            department=self.department,
            designation=self.designation,
            shift=self.shift,
            status='Active',
        )

        self.employee_two = Employee.objects.create(
            user=User.objects.create_user(username='jane', password='secret123', role='employee'),
            emp_id='EMP-002',
            department=self.department,
            designation=self.designation,
            shift=self.shift,
            status='Active',
        )

        self.employee_three = Employee.objects.create(
            user=User.objects.create_user(username='alex', password='secret123', role='employee'),
            emp_id='EMP-003',
            department=self.department,
            designation=self.designation,
            shift=self.shift,
            status='On Leave',
        )

        Attendance.objects.create(
            employee=self.employee,
            date=date.today(),
            check_in='09:00:00',
            check_out='18:00:00',
            status='Present',
            late_minutes=0,
        )

        Attendance.objects.create(
            employee=self.employee_two,
            date=date.today(),
            check_in='09:15:00',
            check_out='18:30:00',
            status='Late',
            late_minutes=15,
        )

    def test_attendance_page_shows_summary_counts(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('attendance_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['present_count'], 1)
        self.assertEqual(response.context['late_count'], 1)
        self.assertEqual(response.context['on_leave_count'], 1)
        self.assertEqual(response.context['absent_count'], 0)
        self.assertContains(response, 'Attendance')
        self.assertContains(response, 'On Leave')

    def test_own_profile_marks_my_profile_as_active(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_detail', args=[self.employee.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_my_profile'])


class UserPermissionViewTests(TestCase):
    def setUp(self):
        self.super_admin = User.objects.create_user(
            username='superadmin',
            password='secret123',
            role='super_admin',
        )

    def test_super_admin_can_manage_permissions_by_role_without_employee(self):
        self.client.force_login(self.super_admin)

        response = self.client.get(f"{reverse('user_permissions_select')}?role=SUPER_ADMIN")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['selected_role'], 'super_admin')
        self.assertContains(response, 'Manage Permissions')
        self.assertNotContains(response, 'No employee found for the selected role.')

        post_response = self.client.post(
            reverse('user_permissions_select'),
            {
                'role': 'SUPER_ADMIN',
                'dashboard_view': 'on',
            },
        )

        self.assertEqual(post_response.status_code, 302)
        permission = UserPermission.objects.get(user=self.super_admin, module='dashboard')
        self.assertTrue(permission.can_view)
        self.assertFalse(permission.can_create)
        self.assertFalse(permission.can_edit)
        self.assertFalse(permission.can_delete)


class ExportFormatTests(TestCase):
    def setUp(self):
        self.super_admin = User.objects.create_user(
            username='superadmin-export',
            password='secret123',
            role='super_admin',
        )
        self.department = Department.objects.create(name='Operations')
        self.designation = Designation.objects.create(title='Analyst', department=self.department)
        self.shift = Shift.objects.create(name='Day', start_time='09:00:00', end_time='18:00:00')
        self.employee = Employee.objects.create(
            user=self.super_admin,
            emp_id='EMP-100',
            department=self.department,
            designation=self.designation,
            shift=self.shift,
            status='Active',
        )
        Notice.objects.create(
            title='Policy Update',
            body='Updated policy text',
            category='Policy',
            audience='all',
            posted_by=self.super_admin,
        )

    def test_employee_export_can_download_pdf(self):
        self.client.force_login(self.super_admin)

        response = self.client.get(f"{reverse('employee_export')}?format=pdf")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('.pdf', response['Content-Disposition'])

    def test_attendance_export_can_download_pptx(self):
        self.client.force_login(self.super_admin)

        response = self.client.get(f"{reverse('attendance_export')}?format=pptx&month=8&year=2026")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
        self.assertIn('.pptx', response['Content-Disposition'])


class TaskStepProgressTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='task-admin',
            password='secret123',
            role='super_admin',
        )
        self.department = Department.objects.create(name='Projects')
        self.designation = Designation.objects.create(title='Manager', department=self.department)
        self.shift = Shift.objects.create(name='Office', start_time='09:00:00', end_time='18:00:00')
        self.employee = Employee.objects.create(
            user=self.user,
            emp_id='EMP-200',
            department=self.department,
            designation=self.designation,
            shift=self.shift,
            status='Active',
        )
        self.project = Project.objects.create(name='Website', manager=self.employee)
        self.status = TaskStatus.objects.create(project=self.project, name='To Do', color='#6B7280', order=0, active=True)
        self.task = Task.objects.create(
            title='Landing page',
            project=self.project,
            assignee=self.employee,
            due_date='2026-09-15',
            priority='High',
            status=self.status,
            progress=0,
        )

    def test_single_task_step_counts_as_20_percent(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('task_step_add', args=[self.task.pk]),
            {'title': 'Create design draft'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['progress'], 20)

        list_response = self.client.get(reverse('task_step_list', args=[self.task.pk]))
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.json()['steps'][0]['title'], 'Create design draft')


class TaskBoardStatusTests(TestCase):
    def test_statuses_for_project_with_no_tasks_still_render_in_card_view(self):
        user = User.objects.create_user(
            username='board-admin',
            password='secret123',
            role='super_admin',
        )
        department = Department.objects.create(name='Board Ops')
        designation = Designation.objects.create(title='Lead', department=department)
        shift = Shift.objects.create(name='Shift A', start_time='09:00:00', end_time='18:00:00')
        employee = Employee.objects.create(
            user=user,
            emp_id='EMP-300',
            department=department,
            designation=designation,
            shift=shift,
            status='Active',
        )
        project = Project.objects.create(name='New Board Project', manager=employee)
        TaskStatus.objects.create(project=project, name='Custom Stage', color='#123456', order=0, active=True)

        self.client.force_login(user)
        response = self.client.get(reverse('task_list'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Custom Stage', [status.name for status in response.context['board_statuses']])
        self.assertEqual(response.context['current_project'], project)
