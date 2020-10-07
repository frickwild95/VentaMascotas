from django.contrib import admin
from Clientes.models import *
from .models import *
# Register your models here.

class PhoneEmployee (admin.TabularInline):
    model = PhoneNumber
    extra = 1
    max_num = 3

class PhoneTypeAdmin(admin.ModelAdmin):
    search_fields = ['type']
    list_filter = ['type']
    list_display = ['type']
    ordering = ['type']

class PhoneAdmin (admin.ModelAdmin):
    search_fields = ['employee__names', 'phonetype']
    list_filter = ['phonetype']
    list_display = ['employee', 'phonetype', 'number']
    ordering = ['employee']
    autocomplete_fields = ('employee', 'phonetype')

class EmployeeAdmin(admin.ModelAdmin):
    inlines = [PhoneEmployee]
    readonly_fields = ['state']
    search_fields = ['names', 'surnames']
    #search_fields = ['names', 'surnames', 'municipality','email', 'cui']
    list_filter = ['gender', 'municipality__department', 'municipality','state']
    fields = (('names', 'surnames'), ('gender','dateofbirth'), ('cui','code'),('municipality','address'),'email','state')
    list_display = ['names', 'surnames', 'edad', 'dateofbirth', 'Departamento', 'municipality','state', 'Empleados']
    ordering = ['names'] #visualizaremos los datos ordenados por nombres
    autocomplete_fields = ['municipality',]

admin.site.register(PhoneType, PhoneTypeAdmin)
admin.site.register(PhoneNumber, PhoneAdmin)
admin.site.register(Employee, EmployeeAdmin)