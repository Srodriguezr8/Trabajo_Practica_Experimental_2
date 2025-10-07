from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_sobretiempos, name='sobretiempo_list'),
    path('nuevo/', views.crear_sobretiempo, name='sobretiempo_create'),
    path('editar/<int:pk>/', views.editar_sobretiempo, name='sobretiempo_edit'),
    path('eliminar/<int:pk>/', views.eliminar_sobretiempo, name='sobretiempo_delete'),
]