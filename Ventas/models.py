from django.db import models
from Clientes.models import *
from Empleados.models import *
from Mascotas.models import *
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

# Create your models here.

class Sale (models.Model) :
    date = models.DateField('Fecha', auto_now_add = True)
    client = models.ForeignKey(Client, on_delete = models.CASCADE, verbose_name = 'Cliente')
    employee = models.ForeignKey(Employee, on_delete = models.CASCADE, verbose_name = 'Empleado')
    total = models.DecimalField('total', max_digits=7, decimal_places=2, default=0.00 )

    def __str__(self):
        cadena = "{0} {1} {2}"
        return cadena.format(self.date, self.client, self.employee)

    def Total (self):
        return 'Q. %s' % self.total

    def agregarTotal (self, total):
        self.total += total

    def descontarTotal (self, total):
        self.total -= total

    def save(self, **kwargs):
        super(Sale, self).save()

    def Nit (self):
        return self.client.nit

    class Meta :
        db_table = 'sale'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def voucher(self):
        #retorna el link que abrira cuando se de un click y el nombre que tendra en la columna
        return mark_safe(u'<a href="/comprobante/?id=%s" target="_blank">comprobante</a>' % self.id)
    voucher.short_description = 'voucher'

    def Ventas (self):
        return mark_safe(u'<a href="/ventas" target="_blank">Ventas</a>')
    Ventas.short_description = 'Ventas'

class Saledetail (models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name = 'Venta')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = 'Mascota')
    quantity = models.PositiveIntegerField('cantidad')

    def save(self, **kwargs):
        total = self.sale.total
        id_product = self.product.pk
        print('id de la mascota:' + str(id_product))
        id_sale = self.sale.pk
        print('id de la venta: '+ str(id_sale))
        if total == 0 :
            print('Procesar stock')
            print('Se va a descontar: '+str(self.quantity))
            self.product.descontarStock(self.quantity)
            print('Quedaron: '+str(self.product.stock))
            print("Procesar total")
            self.sale.total = self.sale.total + (self.product.price * self.quantity)
            cadena = "{0} {1} {2}"
            print (cadena.format(self.sale.total, self.product.name.model, self.product.price))
        else:
            try:
                item = Saledetail.objects.get(sale=id_sale, product=id_product)
                if item.quantity > self.quantity:
                    print('El item si existe se va a procesar como update')
                    print('La cantidad a procesar es menor a la que existia')
                    diferencia = item.quantity - self.quantity
                    print('Stock actual ' + str(item.product.stock))
                    print('Se va a acreditar' + str(diferencia))
                    self.product.agregarStock(diferencia)
                    total=self.product.price * self.quantity
                    print('Total que vienen: ' + str(self.sale.total))
                    print('Total por mascota: ' + str(total))
                    self.sale.descontarTotal(total)
                    print('Total que va: ' + str(self.sale.total))
                else:
                    print('La cantidad a procesar es mayor a la que existia')
                    diferencia = self.quantity - item.quantity
                    print('Stock actual ' + str(item.product.stock))
                    print('Se va a descontar' + str(diferencia))
                    self.product.descontarStock(diferencia)
                    total=self.product.price * diferencia
                    print('Total que vienen: ' + str(self.sale.total))
                    print('Total por mascota: ' + str(total))
                    self.sale.agregarTotal(total)
                    print('Total que va: ' + str(self.sale.total))
            except:
                print('El item no existe se va a procesar como un producto nuevo')
                print('Procesar stock')
                print('Se va a descontar: '+str(self.quantity))
                self.product.descontarStock(self.quantity)
                print('Quedaron: '+str(self.product.stock))
                print("Procesar total")
                self.sale.total = self.sale.total + (self.product.price * self.quantity)
                cadena = "{0} {1} {2}"
                print (cadena.format(self.sale.total, self.product.name.model, self.product.price))

        self.product.save() #Guardamos el producto dado que se modifico su stock
        self.sale.save() #Guardamos la venta junto a su detalle
        super(Saledetail, self).save() #Guardamos el detalle

    def clean(self): # BEFORE INSERT OR UPDATE
        super(Saledetail, self).clean()
        if self.quantity > self.product.stock:
            raise ValidationError('Existencias insuficientes para realizar la venta')

    def __str__(self):
        cadena = "{0} {1} {2}"
        return cadena.format(self.sale, self.product.name, self.quantity)

    def sale_date (self):
        return str(self.sale.date)

    class Meta :
        db_table = 'saledetail'
        verbose_name = 'Detalle de la venta'
        verbose_name_plural = 'Detalle de las ventas'

