from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import SiteSettings
from .models import (
    User, Employee, Department, Designation, Shift,
    Notice, LeaveRequest, LeaveType, Asset, Task, Project,
    ExpenseCategory, FixedCost, PettyCashLedger , Document, SalaryStructure, OnboardingRecord,
    EmailTemplate, Holiday, NotificationRule,
)


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Work Email',
        widget=forms.TextInput(attrs={'placeholder': 'you@luminouslabs.com', 'class': 'input-field'}),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'input-field'}),
    )


class EmployeeForm(forms.ModelForm):
    first_name  = forms.CharField(max_length=100)
    last_name   = forms.CharField(max_length=100)
    email       = forms.EmailField()
    role        = forms.ChoiceField(choices=User.role.field.choices)

    class Meta:
        model  = Employee
        fields = ['emp_id', 'phone', 'department', 'designation', 'shift',
                  'join_date', 'status', 'salary', 'address',
                  'nid', 'blood_group', 'emergency_contact']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['first_name'].initial = instance.user.first_name
            self.fields['last_name'].initial  = instance.user.last_name
            self.fields['email'].initial      = instance.user.email
            self.fields['role'].initial       = instance.user.role


class NoticeForm(forms.ModelForm):
    class Meta:
        model  = Notice
        fields = ['title', 'body', 'category', 'audience', 'dept', 'pinned']


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model  = LeaveRequest
        fields = ['leave_type', 'from_date', 'to_date', 'reason']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date':   forms.DateInput(attrs={'type': 'date'}),
        }


class AssetForm(forms.ModelForm):
    class Meta:
        model  = Asset
        fields = ['asset_id', 'name', 'asset_type', 'serial_no',
                  'assigned_to', 'assigned_on', 'status',
                  'purchase_date', 'purchase_cost', 'note']
        widgets = {
            'assigned_on':   forms.DateInput(attrs={'type': 'date'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = [
            'title',
            'project',
            'assignee',
            'due_date',
            'priority',
            'description',
            'color',
        ]

        widgets = {
            'due_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'rows': 4
                }
            ),

            'color': forms.TextInput(
                attrs={
                    'type': 'color'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['description'].required = False
        self.fields['color'].required = False


class PettyCashForm(forms.ModelForm):
    class Meta:
        model = PettyCashLedger
        fields = ['date', 'description', 'category', 'entry_type', 'amount', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }


class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name', 'description', 'color', 'monthly_budget']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Supplies'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Short description...'}),
            'color': forms.TextInput(attrs={'type': 'color'}),
            'monthly_budget': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

class FixedCostForm(forms.ModelForm):
    class Meta:
        model = FixedCost
        fields = ['item', 'amount', 'frequency', 'due_day', 'status', 'description']
        widgets = {
            'item': forms.TextInput(attrs={'placeholder': 'e.g. Office Rent'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'due_day': forms.TextInput(attrs={'placeholder': 'e.g. 1st or 5th'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model  = Document
        fields = ['name', 'file', 'category', 'document_type', 'employee', 'is_public', 'expiry_date']
        widgets = {'expiry_date': forms.DateInput(attrs={'type': 'date'})}


class SalaryStructureForm(forms.ModelForm):
    class Meta:
        model  = SalaryStructure
        fields = ['employee', 'basic', 'house_rent', 'medical', 'transport',
                  'other_allowance', 'tax_deduction', 'pf_deduction', 'effective_from', 'is_active']
        widgets = {'effective_from': forms.DateInput(attrs={'type': 'date'})}


class DepartmentForm(forms.ModelForm):
    class Meta:
        model  = Department
        fields = ['name', 'head']


class DesignationForm(forms.ModelForm):
    class Meta:
        model  = Designation
        fields = ['title', 'department', 'level']


class ShiftForm(forms.ModelForm):
    class Meta:
        model  = Shift
        fields = ['name', 'start_time', 'end_time', 'team', 'location']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time':   forms.TimeInput(attrs={'type': 'time'}),
        }


class HolidayForm(forms.ModelForm):
    class Meta:
        model  = Holiday
        fields = ['date', 'name', 'htype']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}


class NotificationRuleForm(forms.ModelForm):

    class Meta:
        model = NotificationRule
        fields = [
            'event',
            'channels',
            'recipients',
            'is_active',
        ]

        widgets = {
            'event': forms.TextInput(attrs={
                'placeholder': 'e.g. New leave request',
            }),
            'channels': forms.TextInput(attrs={
                'placeholder': 'e.g. In-app + Email',
            }),
            'recipients': forms.TextInput(attrs={
                'placeholder': 'e.g. Managers, HR',
            }),
            'is_active': forms.CheckboxInput(),
        }


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'company_name',
            'company_email',
            'phone',
            'address',
            'timezone',
            'currency',
            'date_format',
            'logo',
            'maintenance_mode',
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Company Name'
            }),
            'company_email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+880 1XXX-XXXXXX'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Full address'
            }),
            'timezone': forms.Select(attrs={'class': 'form-input'}),
            'currency': forms.Select(attrs={'class': 'form-input'}),
            'date_format': forms.Select(attrs={'class': 'form-input'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'maintenance_mode': forms.CheckboxInput(),
        }
class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate

        fields = [
            'name',
            'category',
            'subject',
            'body',
            'trigger',
            'status',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g. Welcome Email'
            }),

            'category': forms.TextInput(attrs={
                'placeholder': 'e.g. Onboarding'
            }),

            'subject': forms.TextInput(attrs={
                'placeholder': 'Email subject'
            }),

            'body': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': 'Write email content...'
            }),

            'trigger': forms.TextInput(attrs={
                'placeholder': 'e.g. New employee joins'
            }),

            'status': forms.Select(),
        }

