from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path("empleados/", views.lista_empleados, name="empleado_list"),
    path("empleados/crear/", views.crear_empleado, name="empleado_create"),
    path("empleados/<int:pk>/editar/", views.editar_empleado, name="empleado_update"),
    path("empleados/<int:pk>/eliminar/", views.eliminar_empleado, name="empleado_delete"),
    path("empleados/<int:pk>/sueldo/", views.obtener_sueldo_empleado, name="obtener_sueldo_empleado"),
    path("nominas/", views.lista_nominas, name="nomina_list"),
    path("nominas/crear/", views.crear_nomina, name="nomina_create"),
    path("nominas/<int:pk>/", views.detalle_nomina, name="nomina_detail"),
    path("nominas/<int:pk>/editar/", views.editar_nomina, name="nomina_edit"),
    path("nominas/<int:pk>/eliminar/", views.eliminar_nomina, name="nomina_delete"),
    path("nominas/detalle/<int:pk>/eliminar/", views.eliminar_detalle_nomina, name="nomina_detail_delete"),
]