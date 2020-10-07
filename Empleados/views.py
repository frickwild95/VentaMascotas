from django.shortcuts import render
from easy_pdf.views import PDFTemplateView
from Empleados.models import *
# Create your views here.

class EmpleadosPDFView(PDFTemplateView):
    #archivo donde se va a desplegar la info , hay una carpeta llamada templates
    template_name = "empleados.html"

    def get_context_data(self, **kwargs):
        #se hace una instancia del objeto a iterar
        eployees = Employee.objects.all()

        #parametros de salida del reporte,
        return super(EmpleadosPDFView, self).get_context_data(
            pagesize="Letter landscape",
            title="Empleados",
            employees=employees,
            **kwargs
        )