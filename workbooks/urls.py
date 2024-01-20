from django.urls import path
from . import views

urlpatterns = [
    path('adicionar-apostilas/', views.add_workbooks, name="add_workbooks"),
    path('apostila/<int:id>', views.workbook, name="workbook")
]
