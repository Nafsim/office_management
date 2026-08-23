from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone


# ─────────────────────────────────────────────
#  ROLE CONSTANTS
# ─────────────────────────────────────────────
class Role(models.TextChoices):
    SUPER_ADMIN = 'super_admin', 'Super Admin'
    MANAGER     = 'manager',     'Manager'
    EMPLOYEE    = 'employee',    'Employee'


# ─────────────────────────────────────────────
#  CUSTOM USER  (replaces auth.User)
# ─────────────────────────────────────────────
class User(AbstractUser):
    """
    Extends Django's AbstractUser.
    Role is stored on the model AND synced to Django Groups so that
    Django's built-in permission system works out of the box.
    """ 
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLOYEE,
    )
    # Override M2M to avoid clashes with auth.User
    groups = models.ManyToManyField(
        Group,
        related_name='hrm_users',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='hrm_user_permissions',
        blank=True,
    )

    # ── helpers ──────────────────────────────
    @property
    def is_super_admin(self):
        return self.role == Role.SUPER_ADMIN

    @property
    def is_manager(self):
        return self.role == Role.MANAGER

    @property
    def is_employee(self):
        return self.role == Role.EMPLOYEE

    def sync_group(self):
        """Keep Django Group membership aligned with self.role."""
        for r in Role.values:
            grp, _ = Group.objects.get_or_create(name=r)
            if r == self.role:
                self.groups.add(grp)
            else:
                self.groups.remove(grp)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.sync_group()

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"


# ─────────────────────────────────────────────
#  DEPARTMENT
# ─────────────────────────────────────────────
class Department(models.Model):
    name   = models.CharField(max_length=100, unique=True)
    head   = models.ForeignKey(
        'Employee', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='headed_dept'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────
#  DESIGNATION
# ─────────────────────────────────────────────
class Designation(models.Model):
    title      = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='designations')
    level      = models.CharField(max_length=10, blank=True)  # e.g. L1, L2

    def __str__(self):
        return f"{self.title} ({self.department})"


# ─────────────────────────────────────────────
#  SHIFT
# ─────────────────────────────────────────────
class Shift(models.Model):
    name       = models.CharField(max_length=80)
    start_time = models.TimeField()
    end_time   = models.TimeField()
    team       = models.CharField(max_length=80, blank=True)
    location   = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────
#  EMPLOYEE PROFILE
# ─────────────────────────────────────────────
class Employee(models.Model):
    STATUS_CHOICES = [
        ('Active',    'Active'),
        ('On Leave',  'On Leave'),
        ('Probation', 'Probation'),
        ('Inactive',  'Inactive'),
    ]
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    emp_id      = models.CharField(max_length=20, unique=True)
    phone       = models.CharField(max_length=20, blank=True)
    department  = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    designation = models.ForeignKey(Designation, null=True, on_delete=models.SET_NULL)
    shift       = models.ForeignKey(Shift, null=True, blank=True, on_delete=models.SET_NULL)
    join_date   = models.DateField(default=timezone.now)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    salary      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avatar_color = models.CharField(max_length=10, default='#ef6a4f')
    avatar_initials = models.CharField(max_length=4, blank=True)
    address     = models.TextField(blank=True)
    nid         = models.CharField(max_length=30, blank=True, verbose_name='NID / Passport')
    blood_group = models.CharField(max_length=5, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['emp_id']

    def __str__(self):
        return f"{self.emp_id} — {self.user.get_full_name()}"

    def save(self, *args, **kwargs):
        if not self.avatar_initials:
            parts = (self.user.get_full_name() or self.user.username).split()
            self.avatar_initials = ''.join(p[0].upper() for p in parts[:2])
        super().save(*args, **kwargs)

# ─────────────────────────────────────────────
# USER PERMISSIONS
# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
# USER PERMISSIONS
# ─────────────────────────────────────────────

class UserPermission(models.Model):

    MODULE_CHOICES = [
    ('dashboard', 'Dashboard'),
    ('notice', 'Notice & Announcements'),

    ('users', 'Users & Employees'),
    ('onboarding', 'Onboarding & NDA'),
    ('profile', 'My Profile'),

    ('attendance', 'Attendance'),
    ('late', 'Late Management'),
    ('leave', 'Leave Management'),

    ('tasks', 'Task Management'),

    # ── Document Management (expanded) ──
    ('documents', 'Document Management (All)'),
    ('documents_request', 'Document - Request'),
    ('documents_generate', 'Document - Generate'),
    ('documents_employee', 'Document - Employee'),
    ('documents_office', 'Document - Office'),

    ('salary', 'Payroll & Salary'),
    ('payroll', 'Payroll'),
    ('petty_cash', 'Petty Cash'),

    ('assets', 'Asset Management'),
    ('files', 'Files & Credentials'),
    ('configuration', 'Configuration'),
    ('upload_center', 'Upload Center'),
    ('support', 'Support & Help'),
    ('calendar', 'Calendar'),
]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="custom_permissions"
    )

    module = models.CharField(
        max_length=50,
        choices=MODULE_CHOICES
    )

    # None = use role default
    # True = explicitly allowed for this user
    # False = explicitly denied for this user
    can_view = models.BooleanField(
        null=True,
        blank=True,
        default=None
    )

    can_create = models.BooleanField(
        null=True,
        blank=True,
        default=None
    )

    can_edit = models.BooleanField(
        null=True,
        blank=True,
        default=None
    )

    can_delete = models.BooleanField(
        null=True,
        blank=True,
        default=None
    )

    class Meta:
        unique_together = ("user", "module")
        ordering = ["module"]

    def __str__(self):
        return f"{self.user.username} - {self.module}"


    # ─────────────────────────────────────────────
# ROLE DEFAULT PERMISSIONS
# ─────────────────────────────────────────────

class RoleMenuPermission(models.Model):

    role = models.CharField(
        max_length=20,
        choices=Role.choices
    )

    menu = models.CharField(
        max_length=50,
        choices=UserPermission.MODULE_CHOICES
    )

    # Default permissions for this role
    can_view = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        unique_together = ("role", "menu")

    def __str__(self):
        return f"{self.role} - {self.menu}"
# ─────────────────────────────────────────────
#  BANK ACCOUNT
# ─────────────────────────────────────────────
class BankAccount(models.Model):
    employee       = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='bank_accounts')
    bank_name      = models.CharField(max_length=100)
    branch         = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    is_primary     = models.BooleanField(default=False)
    color      = models.CharField(max_length=7, default='#FF6B00', help_text='Task card color in hex format')

    def __str__(self):
        return f"{self.bank_name} — {self.employee}"


# ─────────────────────────────────────────────
#  ATTENDANCE
# ─────────────────────────────────────────────
class AttendanceLog(models.Model):
    """Raw punch-in / punch-out log from device."""
    ACTION_CHOICES = [('IN', 'Check In'), ('OUT', 'Check Out')]
    employee   = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='punch_logs')
    date       = models.DateField(default=timezone.now)
    time       = models.TimeField()
    action     = models.CharField(max_length=3, choices=ACTION_CHOICES)
    device     = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.employee} {self.action} @ {self.date} {self.time}"


class Attendance(models.Model):
    """Daily summarised attendance record."""
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent',  'Absent'),
        ('Late',    'Late'),
        ('Half Day','Half Day'),
        ('Holiday', 'Holiday'),
        ('Leave',   'Leave'),
    ]
    SOURCE_CHOICES = [
        ('web', 'Web'),
        ('manual', 'Manual'),
        ('sync', 'Sync'),
    ]
    employee    = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance')
    date        = models.DateField()
    check_in    = models.TimeField(null=True, blank=True)
    check_out   = models.TimeField(null=True, blank=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Present')
    source      = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='web')
    added_by    = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='attendance_added',
    )
    late_minutes = models.PositiveIntegerField(default=0)
    note        = models.TextField(blank=True)

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.employee} — {self.date} — {self.status}"


# ─────────────────────────────────────────────
#  LATE MANAGEMENT
# ─────────────────────────────────────────────
class LateEntry(models.Model):
    title       = models.CharField(max_length=200, default='')
    WARN_CHOICES = [
        ('none',   'No Warning'),
        ('verbal', 'Verbal Warning'),
        ('written','Written Warning'),
        ('final',  'Final Warning'),
    ]
    attendance   = models.OneToOneField(Attendance, on_delete=models.CASCADE, related_name='late_entry')
    late_minutes = models.PositiveIntegerField()
    reason       = models.TextField(blank=True)
    warning      = models.CharField(max_length=10, choices=WARN_CHOICES, default='none')
    excused      = models.BooleanField(default=False)
    reviewed_by  = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Late {self.late_minutes}m — {self.attendance}"


# ─────────────────────────────────────────────
#  LEAVE
# ─────────────────────────────────────────────
class LeaveType(models.Model):
    name          = models.CharField(max_length=50, unique=True)
    max_days_year = models.PositiveIntegerField(default=10)
    carry_forward = models.BooleanField(default=False)
    paid          = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending',  'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled','Cancelled'),
    ]
    employee    = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    title       = models.CharField(max_length=200, default='')
    leave_type  = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    from_date   = models.DateField()
    to_date     = models.DateField()
    days        = models.PositiveIntegerField()
    reason      = models.TextField()
    attachment  = models.FileField(upload_to='leave_attachments/', null=True, blank=True)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    applied_on  = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_leaves')
    reviewed_on = models.DateTimeField(null=True, blank=True)
    note        = models.TextField(blank=True)
    half_day = models.BooleanField(default=False)
    class Meta:
        ordering = ['-applied_on']

    def __str__(self):
        return f"{self.employee} — {self.leave_type} ({self.status})"


# ─────────────────────────────────────────────
#  NOTICE / ANNOUNCEMENT
# ─────────────────────────────────────────────
class Notice(models.Model):
    CAT_CHOICES = [
        ('Holiday', 'Holiday'), ('Policy', 'Policy'), ('Payroll', 'Payroll'),
        ('General', 'General'), ('Urgent', 'Urgent'),
    ]
    AUDIENCE_CHOICES = [
        ('all',     'All Employees'),
        ('manager', 'Managers Only'),
        ('dept',    'Specific Department'),
    ]
    title    = models.CharField(max_length=200)
    body     = models.TextField()
    category = models.CharField(max_length=20, choices=CAT_CHOICES, default='General')
    audience = models.CharField(max_length=10, choices=AUDIENCE_CHOICES, default='all')
    dept     = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    pinned   = models.BooleanField(default=False)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pinned', '-created_at']

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────
#  DOCUMENT
# ─────────────────────────────────────────────
class Document(models.Model):
    CAT_CHOICES = [
        ('Policy', 'Policy'), ('Legal', 'Legal'), ('Payroll', 'Payroll'),
        ('Benefits', 'Benefits'), ('Personal', 'Personal'), ('Contract', 'Contract'),
    ]
    DOC_TYPE_CHOICES = [
        ('request', 'Request Document'),
        ('generated', 'Generated Document'),
        ('employee', 'Employee Document'),
        ('office', 'Office Document'),
    ]
    name       = models.CharField(max_length=200)
    file       = models.FileField(upload_to='documents/')
    category   = models.CharField(max_length=20, choices=CAT_CHOICES, default='Policy')
    document_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES, default='office', help_text='Type of document for filtering')
    is_approved = models.BooleanField(default=False, help_text='Admin approval for employee documents')
    owner      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    employee   = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL, related_name='personal_docs')
    is_public  = models.BooleanField(default=True, help_text='Visible to all employees')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.name

    @property
    def size_display(self):
        size = self.file.size if self.file else 0
        if size > 1_000_000:
            return f"{size/1_000_000:.1f} MB"
        return f"{size/1_000:.0f} KB"


# ─────────────────────────────────────────────
#  DOCUMENT REQUEST
# ─────────────────────────────────────────────
class DocumentRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]
    
    DOC_TYPE_CHOICES = [
        ('Experience Letter', 'Experience Letter'),
        ('Salary Certificate', 'Salary Certificate'),
        ('NOC', 'NOC (No Objection Certificate)'),
        ('Joining Letter', 'Joining Letter'),
        ('Promotion Letter', 'Promotion Letter'),
        ('Relieving Letter', 'Relieving Letter'),
        ('Other', 'Other'),
    ]
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_requests')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='requested_documents')
    document_type = models.CharField(max_length=50, choices=DOC_TYPE_CHOICES)
    custom_type = models.CharField(max_length=200, blank=True, help_text='Specify if "Other" is selected')
    reason = models.TextField(help_text='Reason for document request')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_requests')
    notes = models.TextField(blank=True, help_text='Admin notes for approval/rejection')
    generated_document = models.ForeignKey(Document, null=True, blank=True, on_delete=models.SET_NULL, related_name='request_source')
    
    class Meta:
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"{self.requester.get_full_name()} - {self.document_type} ({self.status})"



# ─────────────────────────────────────────────
#  PAYROLL / SALARY
# ─────────────────────────────────────────────
class SalaryStructure(models.Model):
    employee        = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salary_structures')
    basic           = models.DecimalField(max_digits=10, decimal_places=2)
    house_rent      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medical         = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_deduction   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pf_deduction    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    effective_from  = models.DateField()
    is_active       = models.BooleanField(default=True)

    @property
    def gross(self):
        return self.basic + self.house_rent + self.medical + self.transport + self.other_allowance

    @property
    def net(self):
        return self.gross - self.tax_deduction - self.pf_deduction

    def __str__(self):
        return f"{self.employee} — ৳{self.gross}"


class Payslip(models.Model):
    STATUS_CHOICES = [('Draft', 'Draft'), ('Processed', 'Processed'), ('Paid', 'Paid')]
    employee    = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payslips')
    month       = models.PositiveIntegerField()   # 1-12
    year        = models.PositiveIntegerField()
    structure   = models.ForeignKey(SalaryStructure, on_delete=models.PROTECT)
    bonus       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deduction   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_pay     = models.DecimalField(max_digits=10, decimal_places=2)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Draft')
    processed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    processed_at = models.DateTimeField(null=True, blank=True)
    paid_at      = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.employee} — {self.month}/{self.year} ({self.status})"



class PayrollAdjustment(models.Model):

    TYPE_CHOICES = (
        ('Bonus', 'Bonus'),
        ('Deduction', 'Deduction'),
        ('Advance', 'Advance'),
        ('Incentive', 'Incentive'),
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='payroll_adjustments'
    )

    adjustment_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    reason = models.CharField(
        max_length=255
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee} - {self.adjustment_type}"
# ─────────────────────────────────────────────
#  PETTY CASH
# ─────────────────────────────────────────────
class PettyCashLedger(models.Model):
    TYPE_CHOICES = [('Credit', 'Credit'), ('Debit', 'Debit')]
    CAT_CHOICES  = [
        ('Supplies', 'Supplies'), ('Food', 'Food'), ('Logistics', 'Logistics'),
        ('Funding', 'Funding'), ('Other', 'Other'),
    ]
    date        = models.DateField(default=timezone.now)
    description = models.CharField(max_length=200)
    category    = models.CharField(max_length=20, choices=CAT_CHOICES, default='Other')
    entry_type  = models.CharField(max_length=6, choices=TYPE_CHOICES)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    balance     = models.DecimalField(max_digits=10, decimal_places=2)
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE)
    note        = models.TextField(blank=True)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return f"{self.date} {self.entry_type} ৳{self.amount}"


# ─────────────────────────────────────────────
#  ASSET MANAGEMENT
# ─────────────────────────────────────────────
class Asset(models.Model):
    TYPE_CHOICES   = [
        ('Laptop', 'Laptop'), ('Monitor', 'Monitor'), ('Mobile', 'Mobile'),
        ('Accessory', 'Accessory'), ('Furniture', 'Furniture'), ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('Available', 'Available'), ('In Use', 'In Use'),
        ('Maintenance', 'Maintenance'), ('Retired', 'Retired'),
    ]
    asset_id     = models.CharField(max_length=30, unique=True)
    name         = models.CharField(max_length=200)
    asset_type   = models.CharField(max_length=20, choices=TYPE_CHOICES)
    serial_no    = models.CharField(max_length=100, blank=True)
    assigned_to  = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL, related_name='assets')
    assigned_on  = models.DateField(null=True, blank=True)
    status       = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Available')
    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    note         = models.TextField(blank=True)

    def __str__(self):
        return f"{self.asset_id} — {self.name}"


# ─────────────────────────────────────────────
#  TASK MANAGEMENT
# ─────────────────────────────────────────────

class Project(models.Model):
    name = models.CharField(max_length=200)

    manager = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='managed_projects'
    )

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class TaskStatus(models.Model):
    """
    Dynamic Kanban status/column.

    Example:
    To Do
    In Progress
    Testing
    Review
    Completed
    """

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='task_statuses'
    )

    name = models.CharField(max_length=50)

    color = models.CharField(
        max_length=7,
        default='#6B7280',
        help_text='Kanban column color in hex format'
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text='Order of the status on the Kanban board'
    )

    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'name'],
                name='unique_task_status_per_project'
            )
        ]

    def __str__(self):
        return self.name


class Task(models.Model):

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    title = models.CharField(max_length=200)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    assignee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    due_date = models.DateField()

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )

    # Dynamic Kanban status
    status = models.ForeignKey(
        TaskStatus,
        on_delete=models.PROTECT,
        related_name='tasks'
    )

    progress = models.PositiveIntegerField(
        default=0
    )

    description = models.TextField(
        blank=True
    )

    # Task card color
    color = models.CharField(
        max_length=7,
        default='#FF6B00',
        help_text='Task card color in hex format'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} [{self.status.name}]"

# ─────────────────────────────────────────────
#  ONBOARDING / NDA
# ─────────────────────────────────────────────
class OnboardingRecord(models.Model):
    STATUS_CHOICES = [
        ('Invited', 'Invited'), ('In Progress', 'In Progress'),
        ('NDA Signed', 'NDA Signed'), ('Completed', 'Completed'),
    ]
    employee      = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='onboarding')
    status        = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Invited')
    nda_signed    = models.BooleanField(default=False)
    nda_signed_at = models.DateTimeField(null=True, blank=True)
    checklist     = models.JSONField(default=dict)   # {step: bool}
    notes         = models.TextField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Onboarding — {self.employee} ({self.status})"


# ─────────────────────────────────────────────
#  FILES & CREDENTIALS (secure vault)
# ─────────────────────────────────────────────
class SecureFile(models.Model):
    name       = models.CharField(max_length=200)
    file       = models.FileField(upload_to='secure/')
    owner      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='secure_files')
    note       = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────
#  EMAIL TEMPLATE
# ─────────────────────────────────────────────
class EmailTemplate(models.Model):
    STATUS_CHOICES = [('Active', 'Active'), ('Draft', 'Draft')]
    name      = models.CharField(max_length=100)
    category  = models.CharField(max_length=50)
    subject   = models.CharField(max_length=200)
    body      = models.TextField()
    trigger   = models.CharField(max_length=100, blank=True)
    status    = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Draft')

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────
#  HOLIDAY CALENDAR
# ─────────────────────────────────────────────
class Holiday(models.Model):
    TYPE_CHOICES = [('Public', 'Public'), ('Religious', 'Religious'), ('Optional', 'Optional')]
    date  = models.DateField(unique=True)
    name  = models.CharField(max_length=200)
    htype = models.CharField(max_length=15, choices=TYPE_CHOICES, default='Public')

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.date} — {self.name}"


# ─────────────────────────────────────────────
#  NOTIFICATION RULE
# ─────────────────────────────────────────────
class NotificationRule(models.Model):
    event      = models.CharField(max_length=100)
    channels   = models.CharField(max_length=50)   # "In-app + Email"
    recipients = models.CharField(max_length=100)
    is_active  = models.BooleanField(default=True)

    def __str__(self):
        return self.event
    




    

# ─────────────────────────────────────────────
# SITE SETTINGS
# ─────────────────────────────────────────────
class SiteSettings(models.Model):
    company_name = models.CharField(max_length=150)
    company_email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.TextField()

    timezone = models.CharField(
        max_length=50,
        default="Asia/Dhaka"
    )

    currency = models.CharField(
        max_length=10,
        default="BDT"
    )

    date_format = models.CharField(
        max_length=20,
        default="DD-MM-YYYY"
    )

    company_logo = models.ImageField(
        upload_to="company_logo/",
        blank=True,
        null=True
    )

    maintenance_mode = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.company_name