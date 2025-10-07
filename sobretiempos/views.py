from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Sobretiempo
from .forms import SobretiempoForm

@login_required
def lista_sobretiempos(request):
    query = request.GET.get("q")
    tipo = request.GET.get("tipo")
    fecha_inicio = request.GET.get("inicio")
    fecha_fin = request.GET.get("fin")

    sobretiempos = Sobretiempo.objects.all().order_by("-fecha_registro")

    if query:
        sobretiempos = sobretiempos.filter(empleado__nombre__icontains=query)
    if tipo:
        sobretiempos = sobretiempos.filter(tipo_sobretiempo_id=tipo)
    if fecha_inicio and fecha_fin:
        sobretiempos = sobretiempos.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    return render(request, "sobretiempo/lista.html", {"sobretiempos": sobretiempos})


@login_required
def crear_sobretiempo(request):
    if request.method == "POST":
        form = SobretiempoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sobretiempo_list")
    else:
        form = SobretiempoForm()
    return render(request, "sobretiempo/form.html", {"form": form, "titulo": "Registrar Sobretiempo"})


@login_required
def editar_sobretiempo(request, pk):
    sobretiempo = get_object_or_404(Sobretiempo, pk=pk)
    if request.method == "POST":
        form = SobretiempoForm(request.POST, instance=sobretiempo)
        if form.is_valid():
            form.save()
            return redirect("sobretiempo_list")
    else:
        form = SobretiempoForm(instance=sobretiempo)
    return render(request, "sobretiempo/form.html", {"form": form, "titulo": "Editar Sobretiempo"})


@login_required
def eliminar_sobretiempo(request, pk):
    sobretiempo = get_object_or_404(Sobretiempo, pk=pk)
    if request.method == "POST":
        sobretiempo.delete()
        return redirect("sobretiempo_list")
    return render(request, "sobretiempo/confirmar_eliminar.html", {"sobretiempo": sobretiempo})
