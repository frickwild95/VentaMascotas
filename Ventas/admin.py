from django.contrib import admin
from .models import *
# Register your models here.

class DetailSale (admin.TabularInline):
    model = Saledetail
    extra = 0
    min_num = 1
    max_num = 10
    autocomplete_fields = ['product']

class SaleAdmin (admin.ModelAdmin):
    inlines = [DetailSale]
    readonly_fields = ['total']
    search_fields = ['client__names', 'client__surnames', 'client__nit']
    list_filter = ['date', 'employee']
    list_display = ['date', 'client', 'employee', 'Total', 'voucher']
    ordering = ['date']
    autocomplete_fields = ['client', 'employee']

class SaleDetailAdmin (admin.ModelAdmin):
    search_fields = ['product','sale']
    list_filter = ['product__name__model','sale__date', 'sale__employee']
    list_display = ['sale_date', 'sale', 'product', 'quantity']
    ordering = ['sale__date']
    autocomplete_fields = ['product','sale']

admin.site.register(Sale, SaleAdmin)
admin.site.register(Saledetail, SaleDetailAdmin)