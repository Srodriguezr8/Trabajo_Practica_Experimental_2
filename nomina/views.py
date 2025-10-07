from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Empleado, Nomina, NominaDetalle
from .forms import EmpleadoForm, NominaForm, NominaDetalleForm


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], 
                    password=request.POST["password1"]
                )
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'signup.html', {
                    "form": UserCreationForm(),
                    "error": "El nombre de usuario ya existe."
                })
        else:
            return render(request, 'signup.html', {
                "form": UserCreationForm(),
                "error": "Las contraseñas no coinciden."
            })


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm()})
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'signin.html', {
                "form": AuthenticationForm(),
                "error": "⚠️ Usuario o contraseña incorrectos."
            })

        login(request, user)
        return redirect('index')

@login_required
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

@login_required
def signout(request):
    logout(request)
    return redirect('signin')


@login_required
def lista_empleados(request):
    empleados = Empleado.objects.all().order_by("nombre")
    paginator = Paginator(empleados, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "empleados/lista.html", {"page_obj": page_obj})


@login_required
def crear_empleado(request):
    if request.method == "POST":
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("empleado_list")
    else:
        form = EmpleadoForm()
    return render(request, "empleados/form.html", {"form": form})


@login_required
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


@login_required
def eliminar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == "POST":
        empleado.delete()
        return redirect("empleado_list")
    return render(request, "empleados/confirmar_eliminar.html", {"empleado": empleado})


@login_required
def lista_nominas(request):
    nominas = Nomina.objects.all().order_by("-aniomes")
    paginator = Paginator(nominas, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "nominas/lista.html", {"page_obj": page_obj})


@login_required
def crear_nomina(request):
    if request.method == "POST":
        form = NominaForm(request.POST)
        if form.is_valid():
            nomina = form.save()
            return redirect("nomina_detail", pk=nomina.pk)
    else:
        form = NominaForm()
    return render(request, "nominas/form.html", {"form": form})


@login_required
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


@login_required
def editar_nomina(request, pk):
    nomina = get_object_or_404(Nomina, pk=pk)
    if request.method == "POST":
        form = NominaForm(request.POST, instance=nomina)
        if form.is_valid():
            form.save()
            return redirect("nomina_list")
    else:
        form = NominaForm(instance=nomina)
    return render(request, "nominas/form.html", {"form": form, "nomina": nomina})


@login_required
def eliminar_nomina(request, pk):
    nomina = get_object_or_404(Nomina, pk=pk)
    if request.method == "POST":
        nomina.delete()
        return redirect("nomina_list")
    return render(request, "nominas/confirmar_eliminar.html", {"nomina": nomina})


@login_required
def eliminar_detalle_nomina(request, pk):
    detalle = get_object_or_404(NominaDetalle, pk=pk)
    nomina = detalle.nomina
    if request.method == "POST":
        detalle.delete()
        nomina.recalcular_totales()
        return redirect("nomina_detail", pk=nomina.pk)
    return render(request, "nominas/confirmar_eliminar.html", {"detalle": detalle})


@login_required
def obtener_sueldo_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    return JsonResponse({'sueldo': str(empleado.sueldo)})
