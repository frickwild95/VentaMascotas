"""VentaMascotas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import *
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from Ventas.views import VoucherPDFView
from Ventas.views import VentasPDFView
from Mascotas.views import InventoryPDFView
from Empleados.views import EmpleadosPDFView
from Clientes.views import ClientesPDFView
from Mascotas.views import IngresoMercaderiaPDFView
from django.config import settings
from django.config.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("comprobantes/", VoucherPDFView.as_view(),  name="comprobante"),
    url(r"^comprobante/", VoucherPDFView.as_view()),
    url(r"^ventas/", VentasPDFView.as_view()),
    path("imprimir/inventario/", InventoryPDFView.as_view() ,  name="inventario"),
    # url(r"^empleados/", EmpleadosPDFView.as_view()),
    path('reporte/empleados' , EmpleadosPDFView.as_view() , name="empleados"),
    path("reporte/clientes/", ClientesPDFView.as_view() , name="clientes"),
    path('reporte/ingresos/mascotas', IngresoMercaderiaPDFView.as_view(), name="ingresos"),
    path('reporte/ventas', VentasPDFView.as_view(), name="ventas"),
] 
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
