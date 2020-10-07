from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from Clientes.models import *
from django.utils.safestring import mark_safe
# Create your models here.

class ProductType (models.Model):
    type = models.CharField('Tipo de Mascota', max_length=50, help_text='Ejemplo: Mamifero, Reptil, Ave,etc.')

    def __str__(self):
        return self.type

    def Type (self):
        cadena = "{0}"
        return cadena.format(self.type)

    class Meta:
        db_table = 'producttype'
        verbose_name = 'Tipo de mascota'
        verbose_name_plural = 'Tipos de mascotas'
        unique_together = ['type']

class ProductBrand (models.Model):
    type = models.ForeignKey(ProductType, on_delete = models.CASCADE, verbose_name = 'Tipo de Mascota')
    brand = models.CharField('Especie de Mascotas', max_length=50, help_text='Ejemplo: Caninos, Felinos, Reptiles, etc.')

    def __str__(self):
        cadena = "{0} {1}"
        return cadena.format(self.type, self.brand)

    class Meta:
        db_table = 'productbrand'
        verbose_name = 'Especie de mascota'
        verbose_name_plural = 'Especies de mascotas'
        unique_together = ['brand']

class ProductModel (models.Model):
    brand = models.ForeignKey(ProductBrand, on_delete = models.CASCADE, verbose_name = 'Especie de mascota')
    model = models.CharField('Raza de la mascota', max_length=50, help_text='Ejemplo: Labrador, Pastor Aleman, Buldog, etc.')

    def __str__(self):
        cadena = "{0} {1}"
        return cadena.format(self.brand, self.model)

    def Models (self):
        return self.model

    class Meta:
        db_table = 'productmodel'
        verbose_name = 'Raza de la mascota'
        verbose_name_plural = 'Razas de las mascotas'
        unique_together = ['model']

class Product (models.Model):
    name = models.ForeignKey(ProductModel, on_delete = models.CASCADE, verbose_name = 'Nombre de la mascota')
    description = models.TextField('Descripción de la mascota', max_length = 250)
    serie = models.CharField('Número de Serie', max_length = 25)
    stock = models.PositiveIntegerField ('Cantidad de existencias', help_text='Solo ingresar números enteros positivos')
    cost = models.PositiveIntegerField ('Costo de la mascota', help_text='Solo ingresar números enteros positivos')
    price = models.PositiveIntegerField ('Precio de Venta de la mascota', help_text='Solo ingresar números enteros positivos')
    state = models.BooleanField('Estado', default='True')

    def __str__ (self) :
        return str(self.name)

    def Costo (self):
        return 'Q. %s' % self.cost

    def Precio (self):
        return 'Q. %s' % self.price

    def descontarStock (self, quantity):
        self.stock = self.stock - quantity

    def agregarStock (self, quantity):
        self.stock += quantity

    def ModifyCost (self, cost):
        self.cost = cost

    def ModifyPrice (self, price):
        self.price = price

    class Meta:
        db_table = 'product'
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        unique_together = ['name']

    def Inventory(self):
        return mark_safe(u'<a href="/inventario" target="_blank">Inventario</a>')
    Inventory.short_description = 'Inventory'

class AddStock (models.Model):
    date = models.DateField(auto_now_add=True, verbose_name='Fecha de ingreso') #se agrega automaticamente la fecha actual
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = 'Mascota')
    quantity = models.PositiveIntegerField('cantidad')
    cost = models.PositiveIntegerField ('Costo de la Mascota', help_text='Solo ingresar números enteros positivos')
    price = models.PositiveIntegerField ('Precio de Venta de la Mascota', help_text='Solo ingresar números enteros positivos')

    def __str__(self):
        return str(self.date)

    def save(self, **kwargs):
        self.product.agregarStock(self.quantity)
        self.product.ModifyCost(self.cost)
        self.product.ModifyPrice(self.price)
        self.product.save()
        super(AddStock, self).save()

    class Meta:
        db_table = 'addstock'
        verbose_name = 'Agregar existencia'
        verbose_name_plural = 'Agregar existencias'

    def IngresoMercaderia(self):
        return mark_safe(u'<a href="/ingreso_mercaderia" target="_blank">Existencias ingresadas</a>')
    IngresoMercaderia.short_description = 'Ingreso Mercaderia'

class Warranty (models.Model):
    date = models.DateField(auto_now_add=True, verbose_name='Fecha de recibido') #se agrega automaticamente la fecha actual
    client = models.ForeignKey(Client, on_delete = models.CASCADE, verbose_name = 'Cliente')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = 'Mascota')
    detail = models.TextField('Detalle o Motivo', max_length = 250)
    state = models.BooleanField('Cubre garantia', default=False)

    def __str__(self):
        cadena = "{0} {1} {2}"
        return cadena.format(self.date, self.client, self.product)

    def modifyState(self, state):
        self.state = state

    class Meta:
        db_table = 'warranty'
        verbose_name = 'Garantía'
        verbose_name_plural = 'Garantías'

class ApproveWarranty (models.Model):
    warranty = models.ForeignKey(Warranty, on_delete = models.CASCADE, verbose_name = 'Garantía')
    state = models.BooleanField('Estado')

    def __str__(self):
        if self.state:
            cadena = "Aplica"
        else:
            cadena = "No aplica"
        return cadena

    def save(self, **kwargs):
        self.warranty.modifyState(self.state)
        self.warranty.save()
        super(ApproveWarranty, self).save()

    class Meta:
        db_table = 'approvewarranty'
        verbose_name = 'Aprobar garantía'
        verbose_name_plural = 'Aprobar garantías'
