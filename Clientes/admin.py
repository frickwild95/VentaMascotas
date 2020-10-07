from django.contrib import admin
from .models import *
# Register your models here.

class PhoneClient (admin.TabularInline):
	model = PhoneNumber
	extra = 1
	max_num =3

class DepartamentAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_filter = ['name']
	list_display = ['name']
	ordering = ['name']

class PhoneTypeAdmin(admin.ModelAdmin):
    search_fields = ['type']
    list_filter = ['type']
    list_display = ['type']
    ordering = ['type']

class PhoneAdmin (admin.ModelAdmin):
    search_fields = ['client__names','number','phonetype__type']
    list_filter = ['phonetype']
    list_display = ['ClientName', 'phonetype', 'number']
    ordering = ['client']
    autocomplete_fields = ['client', 'phonetype']
    #para usar el autocomplete_fields debemos de crear una clase administradora que de forma a nuestra clase por la que queremos listar y filtrar

class MunicipalityAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['department']
    list_display = ['department', 'name']
    ordering = ['name']

class ClientAdmin(admin.ModelAdmin):
    inlines = [PhoneClient]
    readonly_fields = ['state']
    search_fields = ['names', 'surnames']
    #search_fields = ['names', 'surnames', 'municipality','email', 'cui', 'nit']
    list_filter = ['gender', 'municipality__department', 'municipality','state']
    fields = (('names', 'surnames'), ('gender','dateofbirth'), ('cui','nit'),('municipality','address'),'email','state')
    list_display = ['names', 'surnames', 'edad', 'dateofbirth', 'Departamento', 'municipality','state']
    ordering = ['names'] #visualizaremos los datos ordenados por nombres
    autocomplete_fields = ['municipality',]

admin.site.register(PhoneType, PhoneTypeAdmin)
admin.site.register(PhoneNumber, PhoneAdmin)
admin.site.register(Department, DepartamentAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Client, ClientAdmin)