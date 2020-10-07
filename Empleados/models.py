from django.db import models
from Clientes.models import *
from django.utils.safestring import mark_safe
# Create your models here.

class PhoneType (models.Model):
    type = models.CharField('Tipo', max_length=50, help_text='Ingrese el tipo de número telefonico ya sea Celular, Residencial, Laboral, etc.')

    def __str__(self):
        return self.type

    class Meta:
        db_table = 'phonetypeemployee'
        verbose_name = 'Tipo de número de teléfono'
        verbose_name_plural = 'Tipos de números de teléfonos'
        unique_together = ['type']

class Employee (Person) :
    code = models.CharField('Código de empleado', max_length=5, help_text='Ejemplo: EMP01')
    municipality = models.ForeignKey(Municipality, on_delete = models.CASCADE, verbose_name = 'Municipio')
    address = models.CharField('Dirección de Residencia', max_length=100)
    email = models.EmailField('Correo Electrónico', max_length=254)
    state = models.BooleanField('Estado', default=True)

    def Departamento (self):
        cadena = "{0}"
        return cadena.format(self.municipality.department)

    class Meta:
        db_table = 'employee'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def Empleados (self):
        return mark_safe(u'<a href="/empleados" target="_blank">Empleados</a>')
    Empleados.short_description = 'Empleados'

class PhoneNumber (models.Model):
    employee = models.ForeignKey(Employee, on_delete = models.CASCADE, verbose_name = 'Cliente')
    phonetype = models.ForeignKey(PhoneType, on_delete = models.CASCADE, verbose_name = 'Tipo de número telefónico')
    number = models.PositiveIntegerField ('Número de Teléfono', help_text='Solo ingresar números')

    def __str__(self):
        cadena = "{0} {1} {2}"
        return cadena.format(self.employee, self.phonetype, self.number)

    class Meta:
        db_table = 'phonenumberemployee'
        verbose_name = 'Número de teléfono'
        verbose_name_plural = 'Números de teléfono'
        unique_together = ['number']
