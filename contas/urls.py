from django.urls import path
from . import views 

urlpatterns = [
    path('definir_contas/', views.definir_contas, name="definir_contas"),
    path('ver_contas/', views.ver_contas, name="ver_contas"),
    path('paga_conta/<int:id>', views.paga_conta, name='paga_conta')

]
