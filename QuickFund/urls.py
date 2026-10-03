"""
URL configuration for QuickFund project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from finance import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/',views.reg,name='reg'),
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('user_home/',views.user_home,name='user_home'),
    path('service/',views.service,name='service'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('loan_app/',views.loan_app,name='loan_app'),
    path('staff/',views.manager_dashboard,name='staff'),
    path('loan_s/',views.loan_s,name='loan_s'),
    path('user_app_update/<int:id>/', views.user_appli_update, name='user_app_update'),
    path('staff_view_app/<int:id>',views.staff_view_app,name='staff_view_app'),
    path('user_profile/',views.user_profile,name='user_profile'),
    path('user_edit/<int:id>',views.user_edit,name='user_edit'),
    path('admin_users/', views.admin_users, name='admin_users'),
    path('admin_staff',views.admin_staff,name='admin_staff'),
    path('admin_applications/', views.admin_applications, name='admin_applications'),
    path('admin_change_password /<int:id>',views.admin_change_password,name='admin_change_password'),
    path('admin_view_application/<int:id>',views.admin_view_application,name='admin_view_application'),
    path('admin_approve/',views.admin_approve,name='admin_approve'),
    path('loan_approve/<int:id>',views.loan_approved,name='loan_approve'),
    path('admin_delete_staff/<int:id>/', views.admin_delete_staff, name='admin_delete_staff'),
    path('admin_change_password/<int:id>/', views.admin_change_password, name='admin_change_password'),
    path('admin_rejected/', views.admin_rejected_applications, name='admin_rejected'),
    path('receipt/<int:id>/', views.transaction_receipt, name='receipt'),
    path('user_emi/', views.user_emi, name='user_emi'),
    path('pay/<int:emi_id>/', views.pay_emi, name='pay'),
    path('payment_success/', views.emi_success, name='payment_success'),
    path('user_payment/', views.user_payment, name='user_payment'),
    path('staff/applications/', views.staff_applications, name='staff_applications'),
    path('staff_emi_list', views.emi_list, name='staff_emi_list'),
    path('staff_users/', views.staff_users, name='staff_users'),
    path('user-loan_history/<int:user_id>/', views.user_loan_history, name='user_loan_history'),
    path('delete-application/<int:id>/', views.admin_delete_application, name='admin_delete_application'),
    path('admin_delete_application/<int:id>/', views.admin_delete_application, name='admin_delete_application'),
path('add_bank/', views.add_bank, name='add_bank'),
    path(
    'add_bank_account/<int:id>/',
    views.add_bank_account,
    name='add_bank_account'
    ),
    path(
    'send_emi_message/<int:emi_id>/',
    views.send_emi_message,
    name='send_emi_message'
     ),


path(
    'daily_collection/',
    views.daily_collection,
    name='daily_collection'
),
path("emi-detail/<int:loan_id>/", views.emi_detail, name="emi_detail"),
path('user_logout/', views.user_logout, name='user_logout'),

path('staff_logout/', views.staff_logout, name='staff_logout'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
path('change_password/', views.change_password, name='change_password'),
path(
    'returned_applications/',
    views.returned_applications,
    name='returned_applications'
),path('notification/', views.notification, name='notification'),
path(
    'approve-staff/<int:id>/',
    views.approve_staff,
    name='approve_staff'
),
path(
    'add_staff/',
    views.add_staff,
    name='add_staff'
),    path(
        'employee_register/',
        views.employee_register,
        name='employee_register'
    ),
path(
    'admin_emi_list/',
    views.admin_emi_list,
    name='admin_emi_list'
),
path(
    'staff_profile/',
    views.staff_profile,
    name='staff_profile'
),

path(
    'update_staff_profile/',
    views.update_staff_profile,
    name='update_staff_profile'
),
# urls.py
path('admin_collection/', views.admin_collection, name='admin_collection'),
    path('user_logout/',views.user_logout, name='user_logout'),
    path('block_user/<int:id>/', views.block_user, name='block_user'),

    path('unblock_user/<int:id>/', views.unblock_user, name='unblock_user'),
path(
    'update_staff_status/<int:id>/',
    views.update_staff_status,
    name='update_staff_status'
),
path('forgot_password/', views.forgot_password, name='forgot_password'),
path(
    'reject_application/<int:id>/',
    views.reject_application,
    name='reject_application'
),
    path("verify_otp/", views.verify_otp, name="verify_otp"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
