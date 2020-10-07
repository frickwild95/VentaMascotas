from django.contrib import admin
from .models import *
# Register your models here.

class ProductTypeAdmin(admin.ModelAdmin):
    search_fields = ['type']
    list_filter = ['type']
    list_display = ['type']
    ordering = ['type']

class ProductBrandAdmin(admin.ModelAdmin):
    search_fields = ['type','brand']
    list_filter = ['type','brand']
    list_display = ['type', 'brand']
    ordering = ['type']

class ProductModelAdmin(admin.ModelAdmin):
    #search_fields = ['brand__brand','brand__type','model']
    search_fields = ['model', 'brand__brand', 'brand__type__type']
    list_filter = ['brand__brand', 'brand__type','model']
    list_display = ['brand', 'model']
    ordering = ['brand']

class ProductAdmin(admin.ModelAdmin):
    #search_fields = ['name__model']
    search_fields = ['name__model', 'name__brand__brand', 'name__brand__type__type']
    list_filter = ['name__brand__type','name__brand__brand']
    list_display = ['name', 'description', 'serie', 'Costo', 'Precio', 'stock']
    ordering = ['name']
    autocomplete_fields = ['name']

class AddStockAdmin(admin.ModelAdmin):
    search_fields = ['product__name__model', 'product__name__brand__brand', 'product__name__brand__type__type']
    list_filter = ['product__name__brand__type','product__name__brand__brand']
    fields = ['product', 'quantity', 'cost', 'price']
    list_display = ['date', 'product', 'quantity', 'cost', 'price']
    ordering = ['date']
    autocomplete_fields = ['product']

class WarrantyAdmin(admin.ModelAdmin):
    search_fields = ['client__names', 'client__surnames', 'product__name__model', 'product__name__brand__brand', 'product__name__brand__type__type']
    list_filter = ['product__name__brand__type','product__name__brand__brand', 'date', 'state']
    fields = ['client', 'product', 'detail', 'state']
    list_display = ['date', 'client', 'product', 'detail', 'state']
    ordering = ['date']
    autocomplete_fields = ['product','client']

class ApproveWarrantyAdmin(admin.ModelAdmin):
    search_fields = ['warranty']
    list_filter = ['state']
    fields = ['warranty', 'state']
    list_display = ['warranty', 'state']
    ordering = ['warranty']
    autocomplete_fields = ['warranty']

admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductBrand, ProductBrandAdmin)
admin.site.register(ProductModel, ProductModelAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(AddStock, AddStockAdmin)
admin.site.register(Warranty, WarrantyAdmin)
admin.site.register(ApproveWarranty, ApproveWarrantyAdmin)