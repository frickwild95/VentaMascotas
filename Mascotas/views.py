from django.shortcuts import render
from easy_pdf.views import PDFTemplateView
from Mascotas.models import *

# Create your views here.

class InventoryPDFView(PDFTemplateView):
    #archivo donde se va a desplegar la info , hay una carpeta llamada templates
    template_name = "inventario.html"

    def get_context_data(self, **kwargs):
        #se hace una instancia del objeto a iterar
        products = Product.objects.all()

        #parametros de salida del reporte,
        return super(InventoryPDFView, self).get_context_data(
            pagesize="Letter landscape",
            title="Inventario",
            products=products,
            **kwargs
        )
class IngresoMercaderiaPDFView(PDFTemplateView):
    #archivo donde se va a desplegar la info , hay una carpeta llamada templates
    template_name = "ingreso_mascotas.html"

    def get_context_data(self, **kwargs):
        #se hace una instancia del objeto a iterar
        addstock = AddStock.objects.all()

        #parametros de salida del reporte,
        return super(IngresoMercaderiaPDFView, self).get_context_data(
            pagesize="Letter",
            title="Mascotas ingresadas",
            addstock=addstock,
            **kwargs
        )
