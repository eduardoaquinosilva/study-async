from django.urls import path
from . import views

urlpatterns = [
    path('novo-flashcard/', views.new_flashcard, name="new_flashcard"),
    path('deletar-flashcard/<int:id>', views.delete_flashcard, name="delete_flashcard"),
    path('iniciar-desafio/', views.start_challenge, name="start_challenge"),
    path('listar-desafio/', views.list_challenge, name="list_challenge"),
    path('desafio/<int:id>', views.challenge, name="challenge"),
    path('responder-flashcard/<int:id>', views.answer_flashcard, name="answer_flashcard"),
    path('relatorio/<int:id>', views.report, name="report")
]
