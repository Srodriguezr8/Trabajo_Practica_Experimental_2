from django.contrib import admin
from django.apps import apps
from .models import Empleado, Nomina, NominaDetalle
Sobretiempo = apps.get_model('sobretiempos', 'Sobretiempo')


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("cedula", "nombre", "departamento", "cargo", "sueldo")
    search_fields = ("cedula", "nombre", "departamento", "cargo")
    inlines = []


class NominaDetalleInline(admin.TabularInline):
    model = NominaDetalle
    extra = 1


@admin.register(Nomina)
class NominaAdmin(admin.ModelAdmin):
    list_display = ("aniomes", "mostrar_tot_ing", "mostrar_tot_des", "neto")
    inlines = [NominaDetalleInline]

    def mostrar_tot_ing(self, obj):
        return obj.tot_ing if hasattr(obj, "tot_ing") else 0
    mostrar_tot_ing.short_description = "Total Ingresos"

    def mostrar_tot_des(self, obj):
        return obj.tot_des if hasattr(obj, "tot_des") else 0
    mostrar_tot_des.short_description = "Total Descuentos"


@admin.register(NominaDetalle)
class NominaDetalleAdmin(admin.ModelAdmin):
    list_display = (
        "nomina", "empleado", "sueldo", "bono",
        "mostrar_tot_ing", "iess", "prestamo", "mostrar_tot_des", "neto"
    )
    list_filter = ("nomina", "empleado")

    def mostrar_tot_ing(self, obj):
        return obj.tot_ing if hasattr(obj, "tot_ing") else 0
    mostrar_tot_ing.short_description = "Total Ingresos"

    def mostrar_tot_des(self, obj):
        return obj.tot_des if hasattr(obj, "tot_des") else 0
    mostrar_tot_des.short_description = "Total Descuentos"


if Sobretiempo is not None:
    class SobretiempoInline(admin.TabularInline):
        model = Sobretiempo
        extra = 0
        readonly_fields = ("valor", "fecha_registro", "tipo_sobretiempo", "numero_horas")
        can_delete = True
        show_change_link = True

    try:
        admin.site.unregister(Empleado)
    except Exception:
        pass

    @admin.register(Empleado)
    class EmpleadoAdminWithInline(admin.ModelAdmin):
        list_display = ("cedula", "nombre", "departamento", "cargo", "sueldo")
        search_fields = ("cedula", "nombre", "departamento", "cargo")
        inlines = [SobretiempoInline]
