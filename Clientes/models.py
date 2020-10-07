from django.db import models
from datetime import datetime
from django.utils.safestring import mark_safe
# Create your models here.

class Person (models.Model):
    gender_choices = (('M', 'Masculino'), ('F', 'Femenino'), )
    names = models.CharField('Nombres', max_length=50)
    surnames = models.CharField('Apellidos', max_length=50)
    gender = models.CharField('Género', max_length=1, choices=gender_choices, default='M')
    dateofbirth = models.DateField('Fecha de nacimiento')
    cui = models.CharField('CUI', max_length=17)

    #funcion que nos permite calcular la edad del miembro tomando como parametro su fecha de nacimiento
    def edad (self) :
        cadena = int((datetime.now().date() - self.dateofbirth).days / 365.25)
        return '%s años' % cadena

    #funcion que nos retorna en nombre completo del miembro
    def nombrecompleto(self) :
        cadena = "{0} {1}"
        return cadena.format(self.names, self.surnames)

    def nombre (self) :
        return self.names

    def __str__(self):
        return self.nombrecompleto()

    class Meta:
        abstract = True

class PhoneType (models.Model):
    type = models.CharField('Tipo', max_length=50, help_text='Ingrese el tipo de número telefonico ya sea Celular, Residencial, Laboral, etc.')

    def __str__(self):
        return self.type

    class Meta:
        db_table = 'phonetype'
        verbose_name = 'Tipo de número de teléfono'
        verbose_name_plural = 'Tipos de números de teléfonos'
        unique_together = ['type'] #no puede existir otra tipos de números iguales

class Department (models.Model):
    name = models.CharField('Nombre del Departamento', max_length=50, help_text='Ejemplo: Chiquimula, Jutiapa, Zacapa, etc.')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'department'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        unique_together = ['name'] #no puede existir otro departamento con el mismo nombr

class Municipality (models.Model):
    name = models.CharField('Nombre del Municipio', max_length=50, help_text='Ejemplo: Chiquimula, Esquipulas, Quezaltepeque, etc.')
    department = models.ForeignKey(Department, on_delete = models.CASCADE, verbose_name = 'Departamento')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'municipality'
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'
        unique_together = ['name'] #no puede existir otro municipio con el mismo nombre

class Client (Person) :
    nit = models.CharField('NIT', max_length=100, help_text='Ejemplo: 1234567-8')
    municipality = models.ForeignKey(Municipality, on_delete = models.CASCADE, verbose_name = 'Municipio')
    address = models.CharField('Dirección de Residencia', max_length=100)
    email = models.EmailField('Correo Electrónico', max_length=254)
    state = models.BooleanField('Estado', default=True)

    '''def __str__(self):
        return self.names'''

    def Name (self) :
        return self.names

    def Departamento (self):
        cadena = "{0}"
        return cadena.format(self.municipality.department)

    def Nit (self):
        return str(self.nit)

    class Meta:
        db_table = 'client'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def Clientes (self):
        return mark_safe(u'<a href="/clientes" target="_blank">Clientes</a>')
    Clientes.short_description = 'Clientes'

class PhoneNumber (models.Model):
    client = models.ForeignKey(Client, on_delete = models.CASCADE, verbose_name = 'Cliente')
    phonetype = models.ForeignKey(PhoneType, on_delete = models.CASCADE, verbose_name = 'Tipo de número telefónico')
    number = models.PositiveIntegerField ('Número de Teléfono', help_text='Solo ingresar números')

    def __str__(self):
        cadena = "{0} {1} {2}"
        return cadena.format(self.client, self.phonetype, self.number)

    def ClientName (self) :
        return self.client.nombrecompleto()

    class Meta:
        db_table = 'phonenumber'
        verbose_name = 'Número de teléfono'
        verbose_name_plural = 'Números de teléfono'
        unique_together = ['number']
