from django.contrib import admin
from .models import Empleado, Nomina, NominaDetalle


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("cedula", "nombre", "departamento", "cargo", "sueldo")
    search_fields = ("cedula", "nombre", "departamento", "cargo")


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
