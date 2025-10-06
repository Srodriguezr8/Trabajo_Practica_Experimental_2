from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Empleado, Nomina, NominaDetalle
from .forms import EmpleadoForm, NominaForm, NominaDetalleForm

def index(request):
    empleados_count = Empleado.objects.count()
    promedio_sueldos = Empleado.objects.aggregate(Avg("sueldo"))["sueldo__avg"] or 0
    ultima = Nomina.objects.order_by("-aniomes").first()
    total_neto = ultima.neto if ultima else 0
    return render(request, "index.html", {
        "empleados_count": empleados_count,
        "promedio_sueldos": round(promedio_sueldos, 2),
        "ultima": ultima,
        "total_neto": total_neto,
    })

def lista_empleados(request):
    empleados = Empleado.objects.all().order_by("nombre")
    paginator = Paginator(empleados, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "empleados/lista.html", {"page_obj": page_obj})

def crear_empleado(request):
    if request.method == "POST":
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("empleado_list")
    else:
        form = EmpleadoForm()
    return render(request, "empleados/form.html", {"form": form})

def editar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == "POST":
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect("empleado_list")
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, "empleados/form.html", {"form": form})

def eliminar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == "POST":
        empleado.delete()
        return redirect("empleado_list")
    return render(request, "empleados/confirmar_eliminar.html", {"empleado": empleado})

def lista_nominas(request):
    nominas = Nomina.objects.all().order_by("-aniomes")
    paginator = Paginator(nominas, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "nominas/lista.html", {"page_obj": page_obj})


def crear_nomina(request):
    if request.method == "POST":
        form = NominaForm(request.POST)
        if form.is_valid():
            nomina = form.save()
            return redirect("nomina_detail", pk=nomina.pk)
    else:
        form = NominaForm()
    return render(request, "nominas/form.html", {"form": form})


def detalle_nomina(request, pk):
    nomina = get_object_or_404(Nomina, pk=pk)
    detalles = nomina.detalles.all()

    if request.method == "POST":
        form = NominaDetalleForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.nomina = nomina
            detalle.sueldo = detalle.empleado.sueldo
            detalle.save() 
            return redirect("nomina_detail", pk=pk)
    else:
        form = NominaDetalleForm()

    return render(request, "nominas/detalle.html", {
        "nomina": nomina,
        "detalles": detalles,
        "form": form,
    })


def eliminar_detalle_nomina(request, pk):
    detalle = get_object_or_404(NominaDetalle, pk=pk)
    nomina = detalle.nomina
    if request.method == "POST":
        detalle.delete()
        nomina.recalcular_totales()
        return redirect("nomina_detail", pk=nomina.pk)
    return render(request, "nominas/confirmar_eliminar.html", {"detalle": detalle})

def obtener_sueldo_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    return JsonResponse({'sueldo': str(empleado.sueldo)})