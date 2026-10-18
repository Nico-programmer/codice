from django.contrib import admin
from .models import Branch, Companies

@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_document', 'end_date_subscription', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'number_document')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('headquarters', 'company', 'city', 'active')
    list_filter = ('active', 'company')