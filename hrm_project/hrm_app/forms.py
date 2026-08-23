from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import SiteSettings
from .models import (
    User, Employee, Department, Designation, Shift,
    Notice, LeaveRequest, LeaveType, Asset, Task, Project,
    PettyCashLedger, Document, SalaryStructure, OnboardingRecord,
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
        # Make description and color not required
        self.fields['description'].required = False
        self.fields['color'].required = False

class PettyCashForm(forms.ModelForm):
    class Meta:
        model  = PettyCashLedger
        fields = ['date', 'description', 'category', 'entry_type', 'amount', 'note']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}


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
        model  = NotificationRule
        fields = ['event', 'channels', 'recipients', 'is_active']



class SiteSettingsForm(forms.ModelForm):

    class Meta:
        model = SiteSettings
        fields = "__all__"
