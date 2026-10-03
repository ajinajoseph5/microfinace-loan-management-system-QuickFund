from unittest.mock import DEFAULT

from django.db import models
class Register(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    ROLE_CHOICES = [
        ('user', 'User'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    STAFF_STATUS = (
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('resigned', 'Resigned'),
        ('terminated', 'Terminated'),
    )

    BRANCH_TYPE_CHOICES = [
        ('Trivandrum', 'Trivandrum'),
        ('Kollam', 'Kollam'),
        ('Kottayam', 'Kottayam'),
        ('Ernakulam', 'Ernakulam'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    dob = models.DateField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    password = models.CharField(max_length=255)

    branch_type = models.CharField(max_length=50, choices=BRANCH_TYPE_CHOICES)

    is_approved = models.BooleanField(default=False)

    # MUST BE INSIDE THE CLASS
    staff_status = models.CharField(
        max_length=20,
        choices=STAFF_STATUS,
        default='active'
    )
#
# class Register(models.Model):
#
#     GENDER_CHOICES = [
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#         ('Other', 'Other'),
#     ]
#
#     ROLE_CHOICES = [
#         ('user', 'User'),
#         ('staff', 'Staff'),
#         ('admin', 'Admin'),
#     ]
#
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone = models.IntegerField()
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
#     dob = models.DateField()
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
#     password = models.CharField(max_length=255)
#     BRANCH_TYPE_CHOICES = [('Trivandrum', 'Trivandrum'),
#                            ('Kollam', 'kollam'),
#                            ('Kottayam', 'kottayam'),
#                            ('Ernakulam', 'Ernakulam')
#
#                            ]
#     branch_type = models.CharField(max_length=50, choices=BRANCH_TYPE_CHOICES)
#     is_approved = models.BooleanField(default=False)
# STATUS_CHOICES = (
#     ('active', 'Active'),
#     ('temporary', 'Temporary'),
#     ('resigned', 'Resigned'),
#     ('blocked', 'Blocked'),
# )
#
# staff_status = models.CharField(
#     max_length=20,
#     choices=STATUS_CHOICES,
#     default='active'
# )

class loan_application(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    admin_message = models.TextField(blank=True, null=True)
    return_reason = models.TextField(blank=True, null=True)
    reject_reason = models.TextField(blank=True, null=True)

    user = models.ForeignKey('Register', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    loan_amount = models.IntegerField()
    address = models.TextField()
    purpose = models.TextField()
    job = models.CharField(max_length=100)
    income = models.IntegerField()
    relationship = models.CharField(max_length=100)

    photo = models.ImageField()
    id_proof = models.FileField()
    age_proof = models.FileField()
    income_proof = models.FileField()

    LOAN_TYPE_CHOICES = [
        ('personal', 'Personal Loan'),
        ('home', 'Home Loan'),
        ('business', 'Business Loan'),
        ('education', 'Education Loan'),
        ('vehicle', 'Vehicle Loan'),
        ('medical', 'Medical Loan'),
    ]
    loan_type = models.CharField(max_length=50, choices=LOAN_TYPE_CHOICES)

    BRANCH_TYPE_CHOICES = [
        ('Trivandrum', 'Trivandrum'),
        ('Kollam', 'Kollam'),
        ('Kottayam', 'Kottayam'),
        ('Ernakulam', 'Ernakulam')
    ]
    branch_type = models.CharField(max_length=50, choices=BRANCH_TYPE_CHOICES)

    is_disbursed = models.BooleanField(default=False)
    is_transferred = models.BooleanField(default=False)
    notification_seen = models.BooleanField(default=False)

    approved_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    admin_message = models.TextField(blank=True, null=True)

class loan_co_app(models.Model):
    loan = models.ForeignKey(loan_application, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    job = models.CharField(max_length=100)
    co_address = models.TextField()
    income = models.IntegerField()
    relationship = models.CharField(max_length=100)
    photo = models.FileField(upload_to='photo')
    id_proof = models.FileField(upload_to='document')
    age_proof = models.FileField(upload_to='document')
    relational_proof = models.FileField(upload_to='document')
from django.db import models

class EMI(models.Model):
    loan = models.ForeignKey('loan_application', on_delete=models.CASCADE)
    user = models.ForeignKey('Register', on_delete=models.CASCADE)
    emi_number = models.IntegerField()  # 1st EMI, 2nd EMI...
    amount = models.IntegerField()
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Paid', 'Paid')
    ], default='Pending')

    payment_method = models.CharField(max_length=50, null=True, blank=True)

class Transaction(models.Model):
    id=models.AutoField(primary_key=True)
    loan = models.ForeignKey('loan_application', on_delete=models.CASCADE)
    amount=models.IntegerField()
    payment_type = models.CharField(max_length=50,default='disbursement')
    date=models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=[
        ('Pending', 'Pending'),('Paid', 'Paid')
    ])
    reject_reason = models.TextField(blank=True, null=True)
class emi_Payment(models.Model):
    user = models.ForeignKey('Register', on_delete=models.CASCADE)
    emi = models.ForeignKey('EMI', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    payment_method = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Paid', 'Paid')
        ],
        default='Pending'
    )
    emi_date = models.DateField(null=True, blank=True)

from django.db import models


class Bank_Account(models.Model):
    user = models.ForeignKey(
        'Register',
        on_delete=models.CASCADE
    )

    loan = models.ForeignKey(
        'loan_application',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    account_holder = models.CharField(max_length=200)

    bank_name = models.CharField(max_length=200)

    account_number = models.CharField(max_length=50)

    ifsc_code = models.CharField(max_length=20)

    branch_name = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)










