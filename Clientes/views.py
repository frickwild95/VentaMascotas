from django.shortcuts import render
from easy_pdf.views import PDFTemplateView
from Clientes.models import *
# Create your views here.

class ClientesPDFView(PDFTemplateView):
    #archivo donde se va a desplegar la info , hay una carpeta llamada templates
    template_name = "clientes.html"

    def get_context_data(self, **kwargs):
        #se hace una instancia del objeto a iterar
        clients = Client.objects.all()

        #parametros de salida del reporte,
        return super(ClientesPDFView, self).get_context_data(
            pagesize="Letter landscape",
            title="Clientes",
            clients=clients,
            **kwargs
        )
