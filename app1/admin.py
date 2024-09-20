from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'amount', 'description')
    list_filter = ('category', 'date')
    search_fields = ('description', 'category')
    ordering = ('-date',)

admin.site.register(Transaction, TransactionAdmin)
