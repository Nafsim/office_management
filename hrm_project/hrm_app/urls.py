from django.urls import path



from . import views







urlpatterns = [



    # Auth



    path('',            views.login_view,  name='login'),



    path('login/',      views.login_view,  name='login'),



    path('logout/',     views.logout_view, name='logout'),







    # Dashboard



    path('dashboard/',  views.dashboard,   name='dashboard'),



    path('dashboard/export/', views.dashboard_export, name='dashboard_export'),







    # Notices



    path('notices/',               views.notice_list,   name='notice_list'),



    path('notices/<int:pk>/',      views.notice_detail, name='notice_detail'),



    path('notices/create/',        views.notice_create, name='notice_create'),



    path('notices/<int:pk>/delete/', views.notice_delete, name='notice_delete'),

    path(

    "notices/export/",

    views.notice_export,

    name="notice_export"

),





path(

    "notices/<int:pk>/notify/",

    views.notice_notify,

    name="notice_notify"

),



# ─── USERS / EMPLOYEES ─────────────────────────────────────────────

path(
    'employees/',
    views.user_list,
    name='user_list'
),

path(
    'employees/export/',
    views.employee_export,
    name='employee_export'
),

path(
    'employees/create/',
    views.user_create,
    name='user_create'
),

# Role / Default permissions
path(
    'employees/permissions/',
    views.user_permissions,
    name='user_permissions'
),

# Individual user's permissions
path(
    'employees/<int:pk>/permissions/',
    views.user_permissions,
    name='user_permissions_user'
),

path(
    'employees/<int:pk>/edit/',
    views.user_edit,
    name='user_edit'
),

path(
    'employees/<int:pk>/delete/',
    views.user_delete,
    name='user_delete'
),

path(
    'employees/<int:pk>/',
    views.user_detail,
    name='user_detail'
),

path(
    'profile/',
    views.my_profile,
    name='my_profile'
),

  # Attendance

    path(

        'attendance/',

        views.attendance_list,

        name='attendance_list'

    ),

    path(

    'attendance/export/',

    views.attendance_export,

    name='attendance_export'

),

    path(

    'attendance/checkin/',

    views.attendance_checkin,

    name='attendance_checkin'

),

    path(

    'attendance/checkout/',

    views.attendance_checkout,

    name='attendance_checkout'

),

    path(

    'attendance/manual/',

    views.attendance_manual,

    name='attendance_manual'

),

   

    path(

    'attendance/late/',

    views.late_list,

    name='late_list'

),



#late

path(

    'late/',

    views.late_list,

    name='late_list'

),



path(

    'late/export/',

    views.late_export,

    name='late_export'

),



path(

    'late/apply/',

    views.apply_late,

    name='apply_late'

),



path(

    'late/<int:pk>/review/',

    views.late_review,

    name='late_review'

),



path(

    'late/<int:pk>/<str:action>/',

    views.late_action,

    name='late_action'

),



    # Leave



    path('leave/',          views.leave_list,  name='leave_list'),



    path('leave/export/',   views.leave_export, name='leave_export'),



    path('leave/apply/',    views.leave_apply, name='leave_apply'),



    path('leave/<int:pk>/<str:action>/', views.leave_action, name='leave_action'),



    # ─── TASKS ──────────────────────────────────────────────────────────────
    path('tasks/',                         views.task_list,                name='task_list'),
    path('tasks/export/',                  views.task_export,              name='task_export'),
    path('tasks/create/',                  views.task_create,              name='task_create'),

    # Status / Kanban column management
    path('tasks/status/create/',           views.task_status_create,       name='task_status_create'),
    path('tasks/status/<int:pk>/delete/',  views.task_status_delete,       name='task_status_delete'),

    path('tasks/<int:pk>/',                views.task_detail,              name='task_detail'),
    path('tasks/<int:pk>/status/',         views.task_update_status,        name='task_update_status'),
    path('tasks/<int:pk>/edit/',           views.task_edit,                 name='task_edit'),
    path('tasks/<int:pk>/delete/',         views.task_delete,               name='task_delete'),
    path('tasks/<int:pk>/color/',          views.task_update_color,          name='task_update_color'),
    path('tasks/<int:pk>/progress/',       views.task_update_progress,      name='task_update_progress'),
    path('tasks/column-color/',            views.task_update_column_color,   name='task_update_column_color'),


  # ─── TASK STEPS (Dynamic) ──────────────────────────────────────────────
path(
    'task-steps/<int:task_id>/list/',
    views.task_step_list,
    name='task_step_list'
),

path(
    'task-steps/<int:task_id>/add/',
    views.task_step_add,
    name='task_step_add'
),

path(
    'task-steps/<int:step_id>/toggle/',
    views.task_step_toggle,
    name='task_step_toggle'
),

path(
    'task-steps/<int:step_id>/delete/',
    views.task_step_delete,
    name='task_step_delete'
),

path(
    'task-steps/<int:task_id>/reorder/',
    views.task_step_reorder,
    name='task_step_reorder'
),


path('tasks/<int:pk>/upload-image/', views.task_upload_image, name='task_upload_image'),
path('tasks/<int:pk>/upload-document/', views.task_upload_document, name='task_upload_document'),
path('tasks/<int:pk>/attachments/', views.task_get_attachments, name='task_get_attachments'),


    # Documents



        # Documents
    path('documents/',               views.document_list,   name='document_list'),
    path('documents/export/',        views.document_export, name='document_export'),
    path('documents/upload/',        views.document_upload, name='document_upload'),
    path('documents/<int:pk>/download/',  views.document_download, name='document_download'),
    path('documents/<int:pk>/delete/', views.document_delete, name='document_delete'),

    # Document Requests
    path('documents/requests/',                views.document_request_list,   name='document_request_list'),
    path('documents/requests/create/',         views.document_request_create, name='document_request_create'),
    path('documents/requests/<int:pk>/approve/', views.document_request_approve, name='document_request_approve'),
    path('documents/requests/<int:pk>/generate/', views.document_generate, name='document_generate'),





   # change "your_app" to your actual app name (example: hrm)



    # ─────────────────────────────────────────────
    # SALARY / PAYROLL
    # ─────────────────────────────────────────────
    path('salary/', views.salary_list, name='salary_list'),
    path('salary/export/', views.salary_export, name='salary_export'),

    # Dynamic endpoints
    path('salary/breakdown-data/', views.employee_breakdown_data, name='employee_breakdown_data'),
    path('salary/save-adjustment/', views.save_adjustment, name='save_adjustment'),
    path('salary/payslip/download/<int:employee_id>/', views.download_payslip, name='download_payslip'),

    


    # Petty Cash



    path('petty-cash/',      views.petty_cash,     name='petty_cash'),



    path('petty-cash/export/', views.petty_cash_export, name='petty_cash_export'),



    path('petty-cash/add/',  views.petty_cash_add, name='petty_cash_add'),







    # Assets



    path('assets/',                views.asset_list,   name='asset_list'),



    path('assets/export/',         views.asset_export, name='asset_export'),



    path('assets/create/',         views.asset_create, name='asset_create'),



    path('assets/<int:pk>/edit/',  views.asset_edit,   name='asset_edit'),
    path('assets/<int:pk>/assign/', views.asset_assign, name='asset_assign'),
    path('assets/<int:pk>/return/', views.asset_return, name='asset_return'),



    path('assets/<int:pk>/delete/', views.asset_delete, name='asset_delete'),







    # Files



    path('files/',        views.files_list,  name='files_list'),



    path('files/export/', views.files_export, name='files_export'),



    path('files/upload/', views.file_upload, name='file_upload'),



    path('support/faq/', views.user_guide_faq, name='user_guide_faq'),



    path('support/contact/', views.contact_support, name='contact_support'),







    # Onboarding



    path('onboarding/',                          views.onboarding_list,     name='onboarding_list'),



    path('onboarding/export/',                   views.onboarding_export,   name='onboarding_export'),



    path('onboarding/<int:pk>/sign-nda/',        views.onboarding_sign_nda, name='onboarding_sign_nda'),



    path(

    'onboarding/complete/',

    views.onboarding_complete,

    name='onboarding_complete'

),

    path(

    'onboarding/complete/',

    views.onboarding_complete,

    name='onboarding_complete'

),



    # Config



    path('config/',                    views.config,            name='config'),



    path('config/dept/create/',        views.dept_create,       name='dept_create'),



    path('config/desig/create/',       views.desig_create,      name='desig_create'),



    path('config/shift/create/',       views.shift_create,      name='shift_create'),



    path('config/holiday/create/',     views.holiday_create,    name='holiday_create'),



    path('config/notif/<int:pk>/toggle/', views.notif_rule_toggle, name='notif_rule_toggle'),



    path('permissions/',               views.permissions_view,  name='permissions_view'),



     

path('calendar/', views.calendar_view, name='calendar_view'),

path("settings/", views.site_settings, name="site_settings"),

]