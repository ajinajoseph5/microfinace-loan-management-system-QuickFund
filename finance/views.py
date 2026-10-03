from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import re

def reg(request):

    if request.method == 'POST':

        name = request.POST['name'].strip()

        email = request.POST['email'].strip()

        phone = request.POST['phone'].strip()

        dob = request.POST['dob']

        gender = request.POST['gender']

        branch_type = request.POST['branch_type']

        password = request.POST['pwd'].strip()

        # NAME VALIDATION

        if len(name) < 3:

            return HttpResponse(
                "Name must contain minimum 3 characters"
            )

        # EMAIL VALIDATION

        email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'

        if not re.match(email_pattern, email):

            return HttpResponse(
                "Enter valid Gmail address"
            )

        # PHONE VALIDATION

        phone = request.POST.get("phone")

        if not phone.isdigit():
            return HttpResponse("Phone number must contain only numbers.")

        if len(phone) != 10:
            return HttpResponse("Phone number must be exactly 10 digits.")

        if phone[0] not in [ '7', '8', '9']:
            return HttpResponse("Indian mobile number must start with  7, 8, or 9.")
        # PASSWORD VALIDATION

        import re

        if not (6 <= len(password) <= 8):
            return HttpResponse(
                "Password must be between 6 and 8 characters long."
            )

        if not re.search(r'[A-Z]', password):
            return HttpResponse("Password must contain at least one uppercase letter.")

        if not re.search(r'[a-z]', password):
            return HttpResponse("Password must contain at least one lowercase letter.")

        if not re.search(r'\d', password):
            return HttpResponse("Password must contain at least one number.")

        if not re.search(r'[@#$%^&+=!_]', password):
            return HttpResponse("Password must contain at least one special character (@, #, $, %, ^, &, +, =, !, _).")

        # EMAIL EXISTS

        if Register.objects.filter(email=email).exists():

            return HttpResponse(
                "Email already exists"
            )

        # SAVE USER

        Register.objects.create(

            name=name,

            email=email,

            phone=phone,

            dob=dob,

            gender=gender,

            branch_type=branch_type,

            role='user',

            password=password,

            is_approved=True

        )

        return redirect('home')

    return render(request, 'regform.html')

#
# def home(request):
#
#     if request.method == "POST":
#
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#
#         # EMPTY FIELD CHECK
#         if not email or not password:
#
#             messages.error(
#                 request,
#                 "Please enter email and password"
#             )
#
#             return redirect('home')
#
#
#         # ADMIN LOGIN
#         # if email == "admin@gmail.com" and password == "admin123":
#         #
#         #     request.session['adminid'] = email
#         #
#         #     return redirect("admin_home")
#         if email == "admin@gmail.com" and password == "admin123":
#             request.session['adminid'] = email
#             return redirect("admin_home")
#
#
#         try:
#
#             # FIND USER
#             user = Register.objects.get(email=email)
#
#
#             # PASSWORD CHECK
#             if user.password == password:
#
#
#                 # STAFF APPROVAL CHECK
#                 if (
#                     user.role.strip().lower() == 'staff'
#                     and
#                     not user.is_approved
#                 ):
#
#                     messages.error(
#                         request,
#                         "Admin approval pending"
#                     )
#
#                     return redirect('home')
#
#
#                 # SESSION
#                 request.session['userid'] = user.id
#
#
#                 # USER LOGIN
#                 if user.role.strip().lower() == 'user':
#
#                     return redirect("user_home")
#
#
#                 # STAFF LOGIN
#                 elif user.role.strip().lower() == 'staff':
#
#                     return redirect("staff")
#
#
#                 # ADMIN ROLE IN DATABASE
#                 elif user.role.strip().lower() == 'admin':
#
#                     return redirect("admin_home")
#
#
#                 else:
#
#                     messages.error(
#                         request,
#                         "Invalid role"
#                     )
#
#                     return redirect('home')
#
#
#             else:
#
#                 messages.error(
#                     request,
#                     "Incorrect password"
#                 )
#
#                 return redirect('home')
#
#
#         except Register.DoesNotExist:
#
#             messages.error(
#                 request,
#                 "User not found"
#             )
#
#             return redirect('home')
#
#
#     return render(
#         request,
#         'home.html'
#     )
#
#
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register


def home(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        # Empty field validation
        if not email or not password:
            messages.error(request, "Please enter email and password")
            return redirect('home')

        # Admin Login
        if email == "admin@gmail.com" and password == "admin123":
            request.session['adminid'] = email
            return redirect('admin_home')

        try:
            user = Register.objects.get(email=email)

            # Password Check
            if user.password != password:
                messages.error(request, "Incorrect password")
                return redirect('home')

            # BLOCK CHECK FOR ALL USERS
            if user.staff_status == 'blocked':
                messages.error(
                    request,
                    "Your account has been blocked by Admin."
                )
                return redirect('home')

            # STAFF APPROVAL CHECK
            if user.role == 'staff':

                if not user.is_approved:
                    messages.error(
                        request,
                        "Your account is waiting for Admin approval."
                    )
                    return redirect('home')

                if user.staff_status == 'resigned':
                    messages.error(
                        request,
                        "Your account is marked as resigned."
                    )
                    return redirect('home')

            # Create Session
            request.session['userid'] = user.id

            # Role Based Login
            if user.role == 'user':
                return redirect('user_home')

            elif user.role == 'staff':
                return redirect('staff')

            elif user.role == 'admin':
                return redirect('admin_home')

            else:
                messages.error(request, "Invalid role")
                return redirect('home')

        except Register.DoesNotExist:
            messages.error(request, "User not found")
            return redirect('home')

    return render(request, 'home.html')
# USER REGISTRATION

def add_staff(request):

    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')

        # FIXED ERROR HERE
        role = request.POST.get('user_type', 'staff')

        branch = request.POST.get('branch_type')
        password = request.POST.get('pwd')

        # EMAIL CHECK
        if Register.objects.filter(email=email).exists():

            return HttpResponse(
                "Email already exists"
            )

        # CREATE USER
        Register.objects.create(

            name=name,
            email=email,
            phone=phone,
            gender=gender,
            dob=dob,
            role=role,
            branch_type=branch,
            password=password,

            # STAFF NEED APPROVAL
            is_approved=False

        )

        return redirect('home')

    return render(
        request,
        'add_staff_admin.html'
    )


def about(request):
    return render(request,'about.html')

def service(request):
    return render(request,'services.html')

def loan_app(request):
    user = Register.objects.get(id=request.session['userid'])

    if request.method == "POST":
        loan = loan_application.objects.create(
            user=user,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            loan_amount=request.POST.get('loan_amount'),
            address=request.POST.get('address'),
            purpose=request.POST.get('purpose'),
            job=request.POST.get('job'),
            income=request.POST.get('income'),
            relationship=request.POST.get('relationship'),
            loan_type=request.POST.get('loan_type'),
            branch_type=request.POST.get('branch_type'),
            photo=request.FILES.get('photo'),
            id_proof=request.FILES.get('id_proof'),
            age_proof=request.FILES.get('age_proof'),
            income_proof=request.FILES.get('income_proof'),
        )

        # Create co-applicant only if data exists
        if request.POST.get('co_name'):
            loan_co_app.objects.create(
                loan=loan,
                name=request.POST.get('co_name'),
                email=request.POST.get('co_email'),
                phone=request.POST.get('co_phone'),
                co_address=request.POST.get('co_address'),
                job=request.POST.get('co_job'),
                relationship=request.POST.get('co_relationship'),
                income=request.POST.get('co_income'),
                photo=request.FILES.get('co_image'),
                id_proof=request.FILES.get('co_id_proof'),
                age_proof=request.FILES.get('co_age_proof'),
                relational_proof=request.FILES.get('co_relational_proof')
            )

        messages.success(request, "Application submitted successfully!")
        return redirect('user_home')

    return render(request, 'loan_f.html', {'data': user})


def loan_s(request):

    # CHECK LOGIN
    if 'userid' not in request.session:
        return redirect('userhome')

    # CURRENT USER
    user = Register.objects.get(
        id=request.session['userid']
    )

    # LATEST LOAN
    loan = loan_application.objects.filter(
        user=user
    ).order_by('-id').first()

    # BANK ACCOUNT
    bank = None

    if loan:
        bank = Bank_Account.objects.filter(
            user=user,
            loan=loan
        ).first()

    # CONTEXT
    context = {

        'loan': loan,
        'bank': bank
    }

    return render(
        request,
        'loan_status.html',
        context
    )

def user_appli_update(request, id):
    data = loan_application.objects.get(pk=id)
    co_data = loan_co_app.objects.filter(loan=data).first()
    if request.method == "POST":
        data.name = request.POST.get('name')
        data.email = request.POST.get('email')
        data.phone = request.POST.get('phone')
        data.address = request.POST.get('address')
        data.loan_amount = request.POST.get('loan_amount')
        data.purpose = request.POST.get('purpose')
        data.job = request.POST.get('job')
        data.income = request.POST.get('income')
        data.loan_type = request.POST.get('loan_type')
        data.branch_type = request.POST.get('branch_type')
        data.relationship = request.POST.get('relationship')

        if request.FILES.get('id_proof'):
            data.id_proof = request.FILES.get('id_proof')

        if request.FILES.get('age_proof'):
            data.age_proof = request.FILES.get('age_proof')

        if request.FILES.get('income_proof'):
            data.income_proof = request.FILES.get('income_proof')

        if request.FILES.get('photo'):
            data.photo = request.FILES.get('photo')

        data.save()

        print("FILES:", request.FILES)



        if co_data:
            co_data.name = request.POST.get('co_name')
            co_data.email = request.POST.get('co_email')
            co_data.phone = request.POST.get('co_phone')
            co_data.job = request.POST.get('co_job')
            co_data.co_address = request.POST.get('co_address')
            co_data.income = request.POST.get('co_income')
            co_data.relationship = request.POST.get('co_relationship')

            if request.FILES.get('co_image'):
                co_data.photo = request.FILES.get('co_image')

            if request.FILES.get('co_id_proof'):
                co_data.id_proof = request.FILES.get('co_id_proof')

            if request.FILES.get('co_age_proof'):
                co_data.age_proof = request.FILES.get('co_age_proof')

            if request.FILES.get('co_relational_proof'):
                co_data.relational_proof = request.FILES.get('co_relational_proof')

            print(co_data)

            co_data.save()

        return redirect('loan_s')
    return render(request, 'user_update.html', {
        'data': data,
        'co_data': co_data
    })


from datetime import date
#
# def staff_view_app(request, id):
#
#     application = loan_application.objects.get(pk=id)
#
#     if request.method == "POST":
#
#         action = request.POST.get("action")
#
#         message = request.POST.get("message")
#
#         if action == "approve":
#
#             application.status = "approved"
#
#             application.approved_date = date.today()
#
#             application.admin_message = f"""
# Congratulations {application.name},
#
# Your loan application has been approved.
#
# Please fill your bank account details for loan disbursement.
#
# Required Details:
# - Account Holder Name
# - Bank Name
# - Account Number
# - IFSC Code
# - Branch Name
#
# Message:
# {message}
# """
#
#         elif action == "reject":
#
#             application.status = "rejected"
#
#             application.reject_reason = message
#
#         elif action == "return":
#
#             application.status = "returned"
#
#             application.return_reason = message
#
#         application.save()
#
#         return redirect('staff')
#
#     return render(
#         request,
#         'staff_app_view.html',
#         {
#             'application': application
#         }
#     )
def staff_view_app(request, id):

    application = loan_application.objects.get(pk=id)

    if request.method == "POST":

        action = request.POST.get("action")
        message = request.POST.get("message")

        if action == "approve":

            application.status = "approved"
            application.approved_date = date.today()

        elif action == "return":

            application.status = "returned"
            application.return_reason = message

        elif action == "reject":

            application.status = "rejected"
            application.reject_reason = message

        application.save()

        return redirect('staff')

    return render(
        request,
        'staff_app_view.html',
        {'application': application}
    )
def change_password(request):

    user = Register.objects.get(id=request.session['userid'])

    if request.method == "POST":

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # CHECK OLD PASSWORD

        if user.password != old_password:

            messages.error(request, "Old password is incorrect")

        # CHECK PASSWORD MATCH

        elif new_password != confirm_password:

            messages.error(request, "New password and confirm password do not match")

        else:

            user.password = new_password
            user.save()

            messages.success(request, "Password changed successfully")

            return redirect('user_profile')

    return render(request, 'user_change_pwd.html')

def user_profile(request):

    user = Register.objects.get(id=request.session['userid'])

    bank = Bank_Account.objects.filter(user=user).first()

    return render(request, 'profile.html', {
        'data': user,
        'bank': bank
    })


def user_edit(request, id):

    data = Register.objects.get(pk=id)

    if request.method == 'POST':

        data.name = request.POST.get('name')
        data.email = request.POST.get('email')
        data.phone = request.POST.get('phone')
        data.dob = request.POST.get('dob')
        data.gender = request.POST.get('gender')
        data.branch_type = request.POST.get('branch_type')

        data.save()

        messages.success(request, "Profile updated successfully!")

        return redirect('user_edit', id=id)

    return render(request, 'user_edit.html', {'data': data})


def add_bank(request):

    user = Register.objects.get(id=request.session['userid'])

    bank = Bank_Account.objects.filter(user=user).first()

    if request.method == "POST":

        if bank:

            bank.account_holder = request.POST.get('account_holder')
            bank.bank_name = request.POST.get('bank_name')
            bank.account_number = request.POST.get('account_number')
            bank.ifsc_code = request.POST.get('ifsc_code')
            bank.branch_name = request.POST.get('branch_name')

            bank.save()

            messages.success(request, "Bank details updated successfully")

        else:

            Bank_Account.objects.create(
                user=user,
                account_holder=request.POST.get('account_holder'),
                bank_name=request.POST.get('bank_name'),
                account_number=request.POST.get('account_number'),
                ifsc_code=request.POST.get('ifsc_code'),
                branch_name=request.POST.get('branch_name'),
            )

            messages.success(request, "Bank details added successfully")

        return redirect('user_profile')

    return render(request, 'bank_form.html', {
        'bank': bank
    })
#
# def admin_home(request):
#
#     loans = loan_application.objects.all()
#
#     emis = EMI.objects.select_related('loan', 'user').all()
#
#     total_users = Register.objects.count()
#     total_applications = loans.count()
#
#     pending = loans.filter(status="Pending").count()
#     approved = loans.filter(status="Approved").count()
#
#     emi_details = []
#
#     for loan in loans:
#         principal = loan.loan_amount
#         interest = (principal * 5) / 100
#         total = principal + interest
#         months = 10
#         emi = total / months
#
#         emi_details.append({
#             "loan_id": loan.id,
#             "customer": loan.name,
#             "loan_amount": principal,
#             "interest": interest,
#             "months": months,
#             "monthly_emi": emi
#         })
#
#     context = {
#         "total_users": total_users,
#         "total_applications": total_applications,
#         "pending": pending,
#         "approved": approved,
#         "emi_details": emi_details,
#         "emis": emis,
#     }
#
#     return render(request, "admin.html", context)
def admin_home(request):

    loans = loan_application.objects.all()
    emis = EMI.objects.select_related('loan', 'user')

    total_users = Register.objects.count()
    total_applications = loans.count()

    pending = loans.filter(status='pending').count()
    approved = loans.filter(status='approved').count()
    rejected = loans.filter(status='rejected').count()
    returned = loans.filter(status='returned').count()

    transferred = loans.filter(
        status='approved',
        is_transferred=True
    ).count()

    emi_details = []

    for loan in loans:
        principal = loan.loan_amount
        interest = principal * 5 / 100
        total = principal + interest
        months = 10
        emi = total / months

        emi_details.append({
            "loan_id": loan.id,
            "customer": loan.name,
            "loan_amount": principal,
            "interest": interest,
            "months": months,
            "monthly_emi": emi,
        })

    context = {
        "total_users": total_users,
        "total_applications": total_applications,
        "pending": pending,
        "approved": approved,
        "rejected": rejected,
        "returned": returned,
        "transferred": transferred,
        "emi_details": emi_details,
        "emis": emis,
    }

    return render(request, "admin.html", context)
def admin_users(request):
    users = Register.objects.filter(role='user')

    search = request.GET.get('search')
    branch = request.GET.get('branch')

    if search:
        users = users.filter(name__icontains=search)

    if branch:
        users = users.filter(branch_type=branch)

    return render(request, 'admin_users.html', {'data': users})
def admin_staff(request):
    data = Register.objects.filter(role='staff')

    search = request.GET.get('search')
    branch = request.GET.get('branch')

    if search:
        data = data.filter(name__icontains=search)

    if branch:
        data = data.filter(branch_type=branch)

    return render(request, 'admin_staff.html', {'data': data})

def approve_staff(request, id):

    staff = Register.objects.get(id=id)

    staff.is_approved = True
    staff.save()

    messages.success(
        request,
        f"{staff.name} approved successfully."
    )

    return redirect('admin_staff')
def admin_applications(request):
    applications = loan_application.objects.all()
    return render(request, 'admin_application.html', {
        'applications': applications
    })

def admin_change_password(request, id):
    user = Register.objects.get(id=id)

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("admin_change_password", id=id)

        if not (6 <= len(password) <= 8):
            messages.error(request, "Password must be between 6 and 8 characters.")
            return redirect("admin_change_password", id=id)

        # Update password
        user.password = password
        user.save()

        # Send email to staff
        send_mail(
            subject="Password Changed Successfully",
            message=f"""
Dear {user.name},

Your account password has been changed by the administrator.

Your new password is:
{password}

Please log in using this password and change it after logging in.

Regards,
QuickFund Team
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(request, "Password updated successfully and email sent.")
        return redirect("admin_staff")

    return render(request, "change_pwd.html", {"user": user})
from django.utils import timezone
def admin_delete_application(request, id):
    application =loan_application.objects.get(id=id)

    if request.method == "POST":
        application.delete()
        return redirect('admin_dashboard')  # change to your page

    return render(request, 'confirm_delete.html', {
        'application': application
    })
def admin_view_application(request, id):
    application = loan_application.objects.get(id=id)

    if request.method == "POST":
        action = request.POST.get('action')
        message = request.POST.get('message')

        if action == "approve":
            application.status = "approved"
            application.admin_message = message
            application.approved_date = timezone.now()

        elif action == "reject":
            application.status = "rejected"
            application.reject_reason = message

        elif action == "return":
            application.status = "returned"
            application.return_reason = message

        elif action == "disburse":
            application.is_disbursed = True

        application.save()

    return render(request, 'admin_application_view.html', {
        'application': applicationp
    })


def admin_approve(request):

    applications = loan_application.objects.filter(
        status="approved"
    )

    application_data = []

    for app in applications:

        bank = Bank_Account.objects.filter(
            loan=app
        ).first()

        application_data.append({
            'app': app,
            'bank': bank
        })

    context = {
        'application_data': application_data
    }

    return render(
        request,
        'admin_approved.html',
        context
    )


from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

def loan_approved(request, id):

    loan = loan_application.objects.get(pk=id)

    if request.method == "POST":

        # CHECK ALREADY APPROVED
        if not loan.is_transferred:

            principal = loan.loan_amount

            interest_rate = 5

            months = 12

            # CALCULATIONS
            interest_amount = (principal * interest_rate) / 100

            total_amount = principal + interest_amount

            monthly_emi = total_amount / months

            # EMAIL SUBJECT
            subject = "QuickFund Loan Approved Successfully"

            # EMAIL MESSAGE
            message = f"""
Hello {loan.name},

Congratulations!

Your loan application has been approved successfully.

--------------------------------------

Loan Details

Loan Amount : ₹{principal}

Interest Rate : {interest_rate}%

Interest Amount : ₹{interest_amount}

Total Repayment : ₹{total_amount}

Monthly EMI : ₹{round(monthly_emi, 2)}

Tenure : {months} Months

--------------------------------------

Thank you for choosing QuickFund.

QuickFund Team
"""

            try:

                # SEND EMAIL
                email = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [loan.email]
                )

                email.send()

                print("EMAIL SENT SUCCESSFULLY")

            except Exception as e:

                print("EMAIL ERROR:", e)

            # CREATE TRANSACTION
            txn = Transaction.objects.create(
                loan=loan,
                amount=principal,
                payment_type='disbursement',
                status='Paid'
            )

            # CREATE EMI
            for i in range(1, months + 1):

                EMI.objects.create(
                    loan=loan,
                    user=loan.user,
                    emi_number=i,
                    amount=round(monthly_emi, 2),
                    due_date=timezone.now().date() + timedelta(days=30 * i),
                    status='Pending'
                )

            # UPDATE LOAN STATUS
            loan.is_transferred = True

            # IMPORTANT
            loan.is_disbursed = True

            loan.status = 'approved'

            loan.approved_date = timezone.now()

            loan.save()

            return redirect('receipt', id=txn.id)

        return redirect('loan_approve', id=loan.id)

    return render(
        request,
        'loan_approved.html',
        {
            'application': loan
        }
    )

from django.contrib import messages
from django.core.mail import EmailMessage

def reject_application(request, id):

    loan = loan_application.objects.get(id=id)

    if request.method == "POST":

        reason = request.POST.get("reason")

        loan.status = "rejected"
        loan.reject_reason = reason
        loan.admin_message = reason
        loan.save()

        subject = "Loan Application Rejected"

        message = f"""
Hello {loan.name},

Your loan application has been rejected.

Reason:
{reason}

Thank you,
QuickFund
"""

        EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [loan.email]
        ).send()

        messages.success(request, "Application rejected successfully.")

        return redirect("loan_approve", id=loan.id)
def admin_delete_staff(request, id):
    staff = Register.objects.get(id=id)
    staff.delete()
    return redirect('admin_staff')

def admin_change_password(request, id):
    staff =Register.objects.get (id=id)

    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            staff.password = new_password
            staff.save()

            messages.success(request, "Password updated successfully!")
            return redirect(request.GET.get('next', 'admin_staff'))
        else:
            messages.error(request, "Passwords do not match!")

    return render(request, 'password.html', {'staff': staff})
def admin_delete_user(request, id):
    staff = Register.objects.get(id=id)
    staff.delete()
    return redirect('admin_user')
def admin_rejected_applications(request):
    data = loan_application.objects.filter(status='rejected')
    return render(request, 'admin_reject.html', {'data': data})

def logout_view(request):
    request.session.flush()   # clears all session data
    return redirect('home')  # redirect to login page

#
def user_home(request):

    if 'userid' not in request.session:
        return redirect('home')

    user_id = request.session.get('userid')

    user = Register.objects.filter(id=user_id).first()

    if not user:
        return redirect('home')

    loans = loan_application.objects.filter(email=user.email)

    total_loan = 0
    total_emi = 0
    months = 10

    emi_data = []

    for loan in loans:

        principal = loan.loan_amount

        interest = (principal * 5) / 100

        total = principal + interest

        emi = total / months

        total_loan += principal

        total_emi += emi

        paid_count = Transaction.objects.filter(
            loan=loan,
            payment_type='emi',
            status='Paid'
        ).count()

        remaining = months - paid_count

        emi_data.append({
            'loan': loan,
            'emi': emi,
            'paid': paid_count,
            'remaining': remaining
        })

    paid_emi = sum([item['paid'] for item in emi_data])

    remaining_emi = sum([item['remaining'] for item in emi_data])

    txn = Transaction.objects.filter(
        loan__in=loans,
        status='Paid'
    ).last()

    # NOTIFICATION COUNT

    notification_count = loan_application.objects.filter(
        user=user,
        notification_seen=False
    ).count()

    return render(request, 'userhome.html', {

        'total_loan': total_loan,

        'emi_amount': total_emi,

        'paid_emi': paid_emi,

        'remaining_emi': remaining_emi,

        'emi_data': emi_data,

        'txn': txn,

        'notification_count': notification_count

    })



from django.shortcuts import render
from django.db.models import Sum
from django.utils.timezone import now

def manager_dashboard(request):

    # Logged in staff id
    userid = request.session.get('userid')

    # Get current staff
    staff = Register.objects.get(id=userid)

    # Staff branch
    branch = staff.branch_type

    # Branch based loans
    loans = loan_application.objects.filter(
        branch_type=branch
    )

    total_applicants = loans.count()

    completed_loans = loans.filter(
        status="approved"
    ).count()

    today = now().date()

    # EMI branch based
    emis = EMI.objects.select_related(
        'loan',
        'user'
    ).filter(
        loan__branch_type=branch,
        due_date=today,
        status="Pending"
    )

    pending_emi = emis.count()

    # Daily collection branch based
    daily_collection = EMI.objects.filter(
        loan__branch_type=branch,
        status="Paid"
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    context = {

        "loans": loans,

        "total_applicants": total_applicants,

        "completed_loans": completed_loans,

        "pending_emi": pending_emi,

        "daily_collection": daily_collection,

        "emis": emis,

        "today_date": today,

        "branch": branch,
    }

    return render(
        request,
        "staff.html",
        context
    )
def staff_applications(request):

    # Logged in staff id
    userid = request.session.get('userid')

    # Current staff details
    staff = Register.objects.get(id=userid)

    # Staff branch
    branch = staff.branch_type

    # Only same branch applications
    applications = loan_application.objects.filter(
        branch_type=branch
    ).order_by('-id')

    return render(
        request,
        'staff_application_list.html',
        {
            'applications': applications,
            'branch': branch
        }
    )
def emi_list(request):

    userid = request.session.get('userid')

    staff = Register.objects.get(id=userid)

    branch = staff.branch_type

    loans = loan_application.objects.filter(
        branch_type=branch
    )

    loan_data = []

    for loan in loans:

        principal = loan.loan_amount

        interest = (principal * 5) / 100

        total = principal + interest

        emis = EMI.objects.filter(loan=loan)

        months = emis.count()

        monthly_emi = emis.first().amount if emis.exists() else 0

        loan_data.append({

            "loan": loan,
            "loan_id": loan.id,
            "name": loan.name,
            "loan_amount": principal,
            "interest": interest,
            "total": total,
            "months": months,
            "monthly_emi": monthly_emi,
        })

    return render(request, "staff_emi_list.html", {

        "loan_data": loan_data,
        "branch": branch
    })

# def emi_detail(request, loan_id):
#
#     # CHECK LOGIN
#
#
#
#     # GET ADMIN / STAFF
#
#     userid = request.session.get('userid')
#
#     user = Register.objects.get(id=userid)
#
#     # GET LOAN
#
#     loan = loan_application.objects.get(
#         id=loan_id
#     )
#
#     # GET EMI LIST
#
#     emis = EMI.objects.filter(
#         loan=loan
#     ).order_by("emi_number")
#
#     # TOTAL COUNTS
#
#     total_emis = emis.count()
#
#     paid_count = emis.filter(
#         status="Paid"
#     ).count()
#
#     pending_count = emis.filter(
#         status="Pending"
#     ).count()
#
#     # TOTAL AMOUNT
#
#     total_paid_amount = 0
#
#     for emi in emis:
#
#         if emi.status == "Paid":
#
#             total_paid_amount += emi.amount
#
#     # CONTEXT
#
#     context = {
#
#         "loan": loan,
#
#         "emis": emis,
#
#         "total_emis": total_emis,
#
#         "paid_count": paid_count,
#
#         "pending_count": pending_count,
#
#         "total_paid_amount": total_paid_amount,
#
#     }
#
#     return render(
#         request,
#         "emi_detail.html",
#         context
#     )


def emi_detail(request, loan_id):

    userid = request.session.get("userid")

    user = get_object_or_404(Register, id=userid)

    loan = get_object_or_404(loan_application, id=loan_id)

    emis = EMI.objects.filter(loan=loan).order_by("emi_number")

    total_emis = emis.count()
    paid_count = emis.filter(status="Paid").count()
    pending_count = emis.filter(status="Pending").count()

    total_paid_amount = sum(emi.amount for emi in emis if emi.status == "Paid")

    context = {
        "loan": loan,
        "emis": emis,
        "total_emis": total_emis,
        "paid_count": paid_count,
        "pending_count": pending_count,
        "total_paid_amount": total_paid_amount,
    }

    return render(request, "emi_detail.html", context)
def staff_users(request):

    userid = request.session.get('userid')

    staff = Register.objects.get(id=userid)

    branch = staff.branch_type

    users = Register.objects.filter(
        role='user',
        branch_type=branch
    )

    return render(request, 'staff_userlist.html', {

        'users': users,
        'branch': branch
    })
def user_loan_history(request, user_id):
    user = Register.objects.filter(id=user_id)
    loans = loan_application.objects.filter(user_id=user_id).order_by('-id')
    return render(request, 'loans_list.html', {
        'user': user,
        'loans': loans
    })
# ADMIN EMI LIST VIEW

def admin_emi_list(request):


    # GET ALL APPROVED LOANS

    loans = loan_application.objects.filter(
        status='approved'
    )

    # SEARCH

    search = request.GET.get('search')

    if search:

        loans = loans.filter(
            name__icontains=search
        )

    # BRANCH FILTER

    branch = request.GET.get('branch')

    if branch:

        loans = loans.filter(
            branch_type=branch
        )

    loan_data = []

    for loan in loans:

        principal = loan.loan_amount

        interest = (principal * 5) / 100

        total = principal + interest

        emis = EMI.objects.filter(
            loan=loan
        )

        months = emis.count()

        monthly_emi = (
            emis.first().amount
            if emis.exists()
            else 0
        )

        paid_emis = emis.filter(
            status='Paid'
        ).count()

        pending_emis = emis.filter(
            status='Pending'
        ).count()

        loan_data.append({

            "loan": loan,

            "loan_id": loan.id,

            "name": loan.name,

            "branch": loan.branch_type,

            "loan_amount": principal,

            "interest": interest,

            "total": total,

            "months": months,

            "monthly_emi": monthly_emi,

            "paid_emis": paid_emis,

            "pending_emis": pending_emis,

        })

    return render(

        request,

        "admin_emi.html",

        {

            "loan_data": loan_data

        }

    )

def admin_delete_application(request, id):
    application = loan_application.objects.get( id=id)
    application.delete()
    return redirect('admin_applications')



# EMI CALC FUNCTION
def calculate_emi(principal, annual_rate, months):

    monthly_rate = annual_rate / (12 * 100)

    emi = (
        principal * monthly_rate * (1 + monthly_rate) ** months
    ) / ((1 + monthly_rate) ** months - 1)

    return round(emi, 2)
from django.shortcuts import render, redirect
from datetime import timedelta

def user_emi(request):

    # CHECK LOGIN
    if 'userid' not in request.session:
        return redirect('home')

    user = Register.objects.get(id=request.session['userid'])

    loans = loan_application.objects.filter(user=user)

    emi_data = []
    total_loan = 0
    total_paid = 0

    for loan in loans:

        # GET NEXT EMI
        emi_obj = EMI.objects.filter(
            loan=loan,
            user=user
        ).first()

        if not emi_obj:
            continue

        emi_amount = emi_obj.amount

        # PAID EMI COUNT
        paid_count = emi_Payment.objects.filter(
            emi__loan=loan,
            user=user,
            status='Paid'
        ).count()

        months = 24

        remaining_months = months - paid_count

        paid_amount = paid_count * emi_amount

        remaining_amount = (months * emi_amount) - paid_amount

        total_loan += loan.loan_amount

        total_paid += paid_amount

        # NEXT EMI DATE
        start_date = loan.approved_date or loan.created_at

        next_emi_date = None

        if start_date:
            next_emi_date = start_date + timedelta(days=30 * (paid_count + 1))

        # LAST RECEIPT
        txn = emi_Payment.objects.filter(
            emi__loan=loan,
            user=user,
            status='Paid'
        ).last()

        # ALREADY PAID CHECK
        already_paid = emi_obj.status == "Paid"

        emi_data.append({

            "loan": loan,

            "emi": emi_obj,

            "emi_amount": emi_amount,

            "emi_date": next_emi_date,

            "txn": txn,

            "paid_months": paid_count,

            "remaining_months": remaining_months,

            "remaining_amount": remaining_amount,

            "already_paid": already_paid

        })

    return render(request, "emi_list.html", {

        "emi_data": emi_data,

        "total_loan": total_loan,

        "total_paid": total_paid

    })

#   #PAGE2

def user_payment(request):
    user = Register.objects.get(id=request.session['userid'])
    payments = emi_Payment.objects.filter(user=user)\
        .select_related('emi', 'emi__loan')\
        .order_by('-payment_date')

    return render(request, 'payment_history.html', {'payments': payments})



def add_bank_account(request, id):

    # Current user
    user = Register.objects.get(
        id=request.session['userid']
    )

    # Loan
    loan = loan_application.objects.get(
        id=id
    )

    # Save Bank Details
    if request.method == "POST":

        account_holder = request.POST.get('account_holder')
        bank_name = request.POST.get('bank_name')
        account_number = request.POST.get('account_number')
        ifsc_code = request.POST.get('ifsc_code')
        branch_name = request.POST.get('branch_name')

        Bank_Account.objects.create(

            user=user,
            loan=loan,

            account_holder=account_holder,
            bank_name=bank_name,
            account_number=account_number,
            ifsc_code=ifsc_code,
            branch_name=branch_name
        )

        return redirect('loan_s')

    return render(
        request,
        'Bank_Acc.html',
        {'loan': loan}
    )

from django.contrib import messages
from django.shortcuts import redirect
def send_emi_message(request, emi_id):

    emi = EMI.objects.get(id=emi_id)

    # DEMO MESSAGE
    print(
        f"""
        Dear {emi.user},

        Your EMI payment of ₹{emi.amount}
        is pending today.

        Please pay immediately.

        QuickFund Team
        """
    )

    messages.success(
        request,
        "Reminder Message Sent Successfully"
    )

    return redirect('manager_dashboard')
# views.py
#
# from django.shortcuts import render
# from django.db.models import Sum
# from datetime import date
# from .models import EMI
#
#
# def daily_collection(request):
#
#     today = date.today()
#
#     paid_emis = EMI.objects.filter(
#         status="Paid",
#         payment_date=today
#     ).select_related('loan', 'user')
#
#     total_collection = paid_emis.aggregate(
#         total=Sum('amount')
#     )['total'] or 0
#
#     total_paid = paid_emis.count()
#
#     context = {
#
#         "paid_emis": paid_emis,
#         "total_collection": total_collection,
#         "total_paid": total_paid,
#         "today": today,
#     }
#
#     return render(
#         request,
#         "collection.html",
#         context
#     )
# from django.shortcuts import redirect
from django.shortcuts import render
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from datetime import date

from .models import emi_Payment


def daily_collection(request):

    # TODAY DATE
    today = date.today()

    # DAILY PAID EMI
    paid_emis = emi_Payment.objects.filter(
        status='Paid',
        payment_date__date=today
    ).select_related(
        'user',
        'emi'
    )

    # TOTAL DAILY COLLECTION
    total_collection = paid_emis.aggregate(
        total=Sum('amount')
    )['total'] or 0

    # TOTAL DAILY PAID
    total_paid = paid_emis.count()

    # MONTHLY COLLECTION
    monthly_data = emi_Payment.objects.filter(
        status='Paid'
    ).annotate(
        month_name=TruncMonth('payment_date')
    ).values(
        'month_name'
    ).annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-month_name')

    # FORMAT MONTH
    formatted_monthly_data = []

    for item in monthly_data:

        formatted_monthly_data.append({

            'month': item['month_name'].strftime('%B %Y'),
            'total': item['total'],
            'count': item['count']

        })

    context = {

        'paid_emis': paid_emis,
        'total_collection': total_collection,
        'total_paid': total_paid,
        'today': today,
        'monthly_data': formatted_monthly_data

    }

    return render(
        request,
        'collection.html',
        context
    )

# USER LOGOUT
def user_logout(request):

    if 'userid' in request.session:
        del request.session['userid']

    return redirect('home')


# STAFF LOGOUT
def staff_logout(request):

    if 'userid' in request.session:
        del request.session['userid']

    return redirect('home')


# ADMIN LOGOUT
def admin_logout(request):

    if 'adminid' in request.session:
        del request.session['adminid']

    return redirect('home')

from django.views.decorators.csrf import csrf_exempt




# EMI PAYMENT PAGE
import razorpay
def pay_emi(request, emi_id):

    if 'userid' not in request.session:
        return redirect('userhome')

    emi = EMI.objects.get(id=emi_id)

    client = razorpay.Client(
        auth=(
            "rzp_test_SROSnyInFv81S4",
            "WIWYANkTTLg7iGbFgEbwj4BM"
        )
    )

    amount = emi.amount * 100

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        "emi": emi,
        "user": emi.user,
        "payment": payment,
        "amount": amount,
    }

    return render(request, 'payment_now.html', context)

# # PAYMENT SUCCESS
# #
# @csrf_exempt
# #
# def emi_success(request):
#
#
#     if 'payment_data' not in request.session:
#         return redirect('payment_success')
#
#     data = request.session['payment_data']
#
#     user = Register.objects.get(
#         id=request.session['userid']
#     )
#
#     emi = EMI.objects.get(
#         id=data['emi_id'],
#         user=user
#     )
#
#     if emi.status != "Paid":
#
#         emi.status = "Paid"
#         emi.payment_date = timezone.now().date()
#         emi.save()
#
#         emi_Payment.objects.create(
#             user=user,
#             emi=emi,
#             amount=emi.amount,
#             payment_method='Online',
#             status='Paid',
#             emi_date=emi.due_date
#         )
#
#     context = {
#         'emi': emi
#     }
#
#     return render(request, 'emi_pay_success.html', context)
# views.py


@csrf_exempt
def emi_success(request):

    emi_id = request.GET.get("emi_id")

    try:
        emi = EMI.objects.get(id=emi_id)

    except EMI.DoesNotExist:

        messages.error(request, "EMI not found")

        return redirect("user_emi")

    # CHECK ALREADY PAID

    already_paid = emi_Payment.objects.filter(
        emi=emi,
        status="Paid"
    ).exists()

    if not already_paid:

        # UPDATE EMI STATUS

        emi.status = "Paid"
        emi.payment_date = now()
        emi.save()

        # SAVE PAYMENT HISTORY

        emi_Payment.objects.create(

            user=emi.user,

            emi=emi,

            amount=emi.amount,

            payment_method="Razorpay",

            status="Paid",

            emi_date=emi.due_date

        )

    return render(
        request,
        "emi_pay_success.html",
        {
            "emi": emi
        }
    )
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
def transaction_receipt(request, id):

    txn = Transaction.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = f'attachment; filename="receipt_{txn.id}.pdf"'

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("QuickFund Receipt", styles['Title']))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Receipt ID : {txn.id}", styles['Normal']))
    content.append(Paragraph(f"Name : {txn.loan.name}", styles['Normal']))
    content.append(Paragraph(f"Amount : ₹{txn.amount}", styles['Normal']))
    content.append(Paragraph(f"Status : {txn.status}", styles['Normal']))
    content.append(Paragraph(f"Date : {txn.date}", styles['Normal']))

    doc.build(content)

    return response
from django.db.models.functions import TruncWeek
from django.db.models import Count
from .models import loan_application


def returned_applications(request):

    returned_loans = loan_application.objects.filter(
        status='returned'
    ).order_by('-created_at')

    weekly_data = loan_application.objects.filter(
        status='returned'
    ).annotate(
        week=TruncWeek('created_at')
    ).values(
        'week'
    ).annotate(
        total=Count('id')
    ).order_by('-week')

    return render(request, 'returned_applications.html', {
        'returned_loans': returned_loans,
        'weekly_data': weekly_data
    })

def notification(request):

    # CHECK LOGIN

    if 'userid' not in request.session:
        return redirect('home')

    # GET USER

    user_id = request.session.get('userid')

    user = Register.objects.get(id=user_id)

    # GET USER LOANS

    loans = loan_application.objects.filter(
        user=user
    ).order_by('-id')

    # REMOVE NOTIFICATION COUNT AFTER OPEN

    loans.update(notification_seen=True)

    return render(request,
                  'notification.html',
                  {
                      'loans': loans
                  })




def employee_register(request):

    if request.method == "POST":

        # GET FORM DATA

        name = request.POST.get("name").strip()

        email = request.POST.get("email").strip()

        phone = request.POST.get("phone").strip()

        dob = request.POST.get("dob")

        gender = request.POST.get("gender")

        branch_type = request.POST.get("branch_type")

        role = request.POST.get("role")

        password = request.POST.get("password").strip()

        confirm_password = request.POST.get("confirm_password").strip()

        # NAME VALIDATION

        if len(name) < 3:

            messages.error(
                request,
                "Name must contain minimum 3 characters"
            )

            return redirect("employee_register")

        # EMAIL VALIDATION

        email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'

        if not re.match(email_pattern, email):

            messages.error(
                request,
                "Enter valid Gmail address"
            )

            return redirect("employee_register")

        # PHONE VALIDATION

        if not phone.isdigit():

            messages.error(
                request,
                "Phone number must contain only numbers"
            )

            return redirect("employee_register")

        if len(phone) != 10:

            messages.error(
                request,
                "Phone number must be 10 digits"
            )

            return redirect("employee_register")

        # PASSWORD VALIDATION

        if len(password) < 6:

            messages.error(
                request,
                "Password must contain minimum 6 characters"
            )

            return redirect("employee_register")

        if not re.search(r'[A-Z]', password):

            messages.error(
                request,
                "Password must contain one uppercase letter"
            )

            return redirect("employee_register")

        if not re.search(r'[a-z]', password):

            messages.error(
                request,
                "Password must contain one lowercase letter"
            )

            return redirect("employee_register")

        if not re.search(r'[0-9]', password):

            messages.error(
                request,
                "Password must contain one number"
            )

            return redirect("employee_register")

        if not re.search(r'[@#$%^&+=!]', password):

            messages.error(
                request,
                "Password must contain one special character"
            )

            return redirect("employee_register")

        # CONFIRM PASSWORD CHECK

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match"
            )

            return redirect("employee_register")

        # EMAIL EXISTS CHECK

        if Register.objects.filter(email=email).exists():

            messages.error(
                request,
                "Email already exists"
            )

            return redirect("employee_register")

        # SAVE STAFF

        Register.objects.create(

            name=name,

            email=email,

            phone=phone,

            dob=dob,

            gender=gender,

            branch_type=branch_type,

            role=role,

            password=password,

            is_approved=False

        )

        messages.success(
            request,
            "Staff Registered Successfully"
        )

        return redirect("home")

    return render(request, "staff_reg.html")

from django.shortcuts import render, redirect
from .models import Register


# STAFF PROFILE VIEW

def staff_profile(request):

    if 'userid' not in request.session:
        return redirect('home')

    staff = Register.objects.get(
        id=request.session['userid']
    )

    return render(
        request,
        'staff_profile.html',
        {'staff': staff}
    )


# STAFF PROFILE UPDATE

def update_staff_profile(request):

    if 'userid' not in request.session:
        return redirect('home')

    staff = Register.objects.get(
        id=request.session['userid']
    )

    if request.method == 'POST':

        staff.name = request.POST.get('name')
        staff.email = request.POST.get('email')
        staff.phone = request.POST.get('phone')
        staff.gender = request.POST.get('gender')
        staff.dob = request.POST.get('dob')
        staff.branch_type = request.POST.get('branch_type')

        staff.save()

        return redirect('staff_profile')

    return render(
        request,
        'update_staff_profile.html',
        {'staff': staff}
    )

# views.py


# views.py



def admin_collection(request):

    # TODAY DATE
    today = date.today()

    # DAILY PAID EMI
    paid_emis = emi_Payment.objects.filter(
        status='Paid',
        payment_date__date=today
    ).select_related(
        'user',
        'emi'
    )

    # TOTAL DAILY COLLECTION
    total_collection = paid_emis.aggregate(
        total=Sum('amount')
    )['total'] or 0

    # TOTAL DAILY PAID
    total_paid = paid_emis.count()

    # MONTHLY COLLECTION
    monthly_data = emi_Payment.objects.filter(
        status='Paid'
    ).annotate(
        month_name=TruncMonth('payment_date')
    ).values(
        'month_name'
    ).annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-month_name')

    # FORMAT MONTH
    formatted_monthly_data = []

    for item in monthly_data:

        formatted_monthly_data.append({

            'month': item['month_name'].strftime('%B %Y'),
            'total': item['total'],
            'count': item['count']

        })

    context = {

        'paid_emis': paid_emis,
        'total_collection': total_collection,
        'total_paid': total_paid,
        'today': today,
        'monthly_data': formatted_monthly_data

    }

    return render(
        request,
        'daliy_collection.html',
        context
    )
from django.shortcuts import get_object_or_404, redirect

from django.shortcuts import render, redirect, get_object_or_404
from .models import Register

# def admin_users(request):
#     users = Register.objects.all()
#     return render(request, 'admin_users.html', {'users': users})

from django.shortcuts import get_object_or_404, redirect

def block_user(request, id):
    user = get_object_or_404(Register, id=id)

    user.staff_status = 'blocked'
    user.save(update_fields=['staff_status'])

    return redirect('admin_users')


def unblock_user(request, id):
    user = get_object_or_404(Register, id=id)

    user.staff_status = 'active'
    user.save(update_fields=['staff_status'])

    return redirect('admin_users')
from django.contrib import messages

def update_staff_status(request, id):

    staff = get_object_or_404(Register, id=id)

    if request.method == "POST":

        status = request.POST.get("staff_status")

        if status in ["active", "returned", "resigned", "terminated"]:

            staff.staff_status = status
            staff.save()

            messages.success(
                request,
                f"{staff.name} status updated successfully."
            )

        else:
            messages.error(
                request,
                "Invalid status selected."
            )

    return redirect("admin_staff")
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Register

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = Register.objects.get(email=email)

            otp = random.randint(100000, 999999)

            # Store OTP and email in session
            request.session["reset_email"] = email
            request.session["reset_otp"] = str(otp)

            send_mail(
                subject="Password Reset OTP",
                message=f"Your OTP is {otp}. It is valid for 5 minutes.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, "OTP sent to your email.")
            return redirect("verify_otp")

        except Register.DoesNotExist:
            messages.error(request, "Email not found.")

    return render(request, "forgot_password.html")


from django.contrib.auth.hashers import make_password

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        session_otp = request.session.get("reset_otp")
        email = request.session.get("reset_email")

        if entered_otp != session_otp:
            messages.error(request, "Invalid OTP.")
            return redirect("verify_otp")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("verify_otp")

        user = Register.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()

        # Remove session data
        request.session.pop("reset_otp", None)
        request.session.pop("reset_email", None)

        messages.success(request, "Password changed successfully.")
        return redirect("home")

    return render(request, "verify_otp.html")