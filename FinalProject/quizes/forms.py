from django.forms import ModelForm
from .models import Quiz
from questions.models import Question, Answer

class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['project', 'name', 'topic', 'number_of_questions', 'time', 'required_score_to_pass', 'difficulty']

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'quiz', 'lesson']


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'correct', 'question']
