from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Employee, Department, Designation, Shift, BankAccount,
    AttendanceLog, Attendance, LateEntry, LeaveType, LeaveRequest,
    Notice, Document, SalaryStructure, Payslip, PettyCashLedger,
    Asset, Project, Task, OnboardingRecord, SecureFile,
    EmailTemplate, Holiday, NotificationRule,
)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'get_full_name', 'role', 'is_active')
    list_filter  = ('role', 'is_active')
    fieldsets    = BaseUserAdmin.fieldsets + (
        ('HRM Role', {'fields': ('role',)}),
    )

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'user', 'department', 'designation', 'status', 'salary')
    list_filter  = ('status', 'department')
    search_fields = ('emp_id', 'user__first_name', 'user__last_name', 'user__email')

admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Shift)
admin.site.register(BankAccount)
admin.site.register(AttendanceLog)
admin.site.register(Attendance)
admin.site.register(LateEntry)
admin.site.register(LeaveType)
admin.site.register(LeaveRequest)
admin.site.register(Notice)
admin.site.register(Document)
admin.site.register(SalaryStructure)
admin.site.register(Payslip)
admin.site.register(PettyCashLedger)
admin.site.register(Asset)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(OnboardingRecord)
admin.site.register(SecureFile)
admin.site.register(EmailTemplate)
admin.site.register(Holiday)
admin.site.register(NotificationRule)