from django.shortcuts import render
from easy_pdf.views import PDFTemplateView
from Ventas.models import *
# Create your views here.

class VoucherPDFView(PDFTemplateView):
    template_name = "comprobante.html"

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get("id")
        sale = Sale.objects.get(id=ids)
        saledetail = Saledetail.objects.filter(sale=ids)

        return super(VoucherPDFView, self).get_context_data(
            pagesize="Letter",
            title="comprobante",
            sale=sale,
            saledetails=saledetail,
            **kwargs
        )

class VentasPDFView(PDFTemplateView):
    #archivo donde se va a desplegar la info , hay una carpeta llamada templates
    template_name = "ventas.html"

    def get_context_data(self, **kwargs):
        #se hace una instancia del objeto a iterar
        sales = Sale.objects.all()

        #parametros de salida del reporte,
        return super(VentasPDFView, self).get_context_data(
            pagesize="Letter landscape",
            title="Ventas",
            sales=sales,
            **kwargs
        )
