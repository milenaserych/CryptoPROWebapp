from django.urls import path
from .views import (
    QuizListView,
    quiz_view,
    quiz_data_view,
    save_quiz_view,
    get_incorrect_questions,
    update_current_quiz,
    create_quiz,
    add_question
)

app_name = 'quizes'

urlpatterns=[
    path('update_current_quiz/', update_current_quiz, name='update_current_quiz'),
    path('create-quiz/', create_quiz, name="create-quiz"),
    path('add-question/', add_question, name="add-question"),
    path('<pk>/', quiz_view, name='quiz-view'),
    path('<pk>/data/', quiz_data_view, name='quiz-data-view'),
    path('<pk>/save/', save_quiz_view, name='save-view'),
    path('<pk>/get_incorrect_questions/', get_incorrect_questions, name='incorrect-questions-view'),
]