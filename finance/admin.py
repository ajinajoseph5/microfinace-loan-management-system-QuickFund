from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Register)
admin.site.register(loan_application)
admin.site.register(loan_co_app)
admin.site.register(EMI)
admin.site.register(Transaction)
admin.site.register(emi_Payment)
admin.site.register(Bank_Account)
