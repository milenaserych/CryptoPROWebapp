from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms import inlineformset_factory

import random

from questions.models import Question, Answer, IncorrectQuestion
from results.models import Result
from users.models import Profile
from results.views import update_leaderboard

from .forms import QuizForm, QuestionForm, AnswerForm



class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/quizes.html'

# Function to retrieve a specific quiz based on its 'pk'
def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizes/quiz.html', {'obj': quiz})

#Function to return JSON data containing info about the quiz:
# Questions with their possible answers
def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append({'text': a.text, 'correct': a.correct})
        questions.append({str(q): answers})
    print("Original Questions Data: ", questions)
    return JsonResponse({
        'data': questions,
        'quiz_name': quiz.name,
        'r_score': quiz.required_score_to_pass,
    })

@csrf_exempt
def save_quiz_view(request, pk):
    # Check if the request is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        
        # Retrieving the questions of the quiz
        for k in data_.keys():
            print('key: ', k)
            try:
                question = Question.objects.get(text=k)
                questions.append(question)
            except Question.DoesNotExist:
                print('Question not found: ', k)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        incorrect_questions = [] # List to store incorrectly answered questions

        # Loop through each question
        for q in questions:
            a_selected = request.POST.get(q.text)
            
            # Check if an answer was selected
            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                correct_answer = None # Initialize correct_answer variable
                
                # Loop through all the answers
                for a in question_answers:
                    # Match the selected answer to the answers available
                    if a_selected == a.text:
                        # Check if the selected answer was correct
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                        else:
                            # Check if the question is not already in the list of incorrect questions
                            if not any(item['question'] == q for item in incorrect_questions):
                                incorrect_question_instance = IncorrectQuestion.objects.filter(user=user, quiz=quiz, question=q).first()
                                # Check if the question is not already in the database
                                if not incorrect_question_instance:
                                    # Save the incorrect answers
                                    incorrect_questions.append({
                                        'question': q,
                                        'frequency': 1,
                                    })
                                    print("Just added a new incorrect question to the database!")
                                else:
                                    incorrect_question_instance.frequency += 1
                                    incorrect_question_instance.save()
                                    print("Just incremented the frequency of one of the previously incorrect questions!")

                    else:
                        if a.correct:
                            correct_answer = a.text
                print("Incorrect answers: ", incorrect_questions)
                # Results will hold The Question itself, the correct answer, and the answer I selected
                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        score_ = score * multiplier
        # Create a Result object for the user's quiz attempt
        result_instance = Result.objects.create(quiz=quiz, user=user, score=score_) 

        # Save incorrect answers in the IncorrectAnswer model
        for incorrect_question in incorrect_questions:
            IncorrectQuestion.objects.create(
                user=user,
                quiz=quiz,
                question=incorrect_question['question'],
                frequency=incorrect_question['frequency']
            )

        update_leaderboard(request.user) 

        # Return JSON response indicating whether the quiz was passed. the score, and detailed results
        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})
        


@csrf_exempt
def get_incorrect_questions(request, pk):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Retrieve all incorrect questions
        incorrect_questions = IncorrectQuestion.objects.filter(user=request.user)

        # Randomly select 2 questions
        random_questions = random.sample(list(incorrect_questions), min(2, len(incorrect_questions)))

        # Prepare data for JSON response
        questions_data = []
        for question in random_questions:
            question_data = {str(question.question): []}
            for answer in question.question.get_answers():
                question_data[str(question.question)].append({
                    'text': answer.text,
                    'correct': answer.correct
                })
            questions_data.append(question_data)
        print("Incorrect Questions Data: ", questions_data)
        return JsonResponse({'data': questions_data})
    else:
        pass


@csrf_exempt
def update_current_quiz(request):
    if request.method == 'POST':
        quiz_title = request.POST.get('quiz_title', '')
        try:
            profile_obj = Profile.objects.get(user=request.user)
            profile_obj.current_quiz = quiz_title
            print("Current quiz was just changed in the back end! Changed to: ", profile_obj.current_quiz)
            profile_obj.save()
            return JsonResponse({'success': True})
        except Profile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Profile not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required(login_url="login")
def create_quiz(request):
    quiz_form = QuizForm()
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST, request.FILES)
        if quiz_form.is_valid():
            quiz_form.save()
            return redirect('projects:projects')
    context = {
        'quiz_form':quiz_form,
    }
    return render(request, 'quizes/create_quiz.html', context)

@login_required(login_url="login")
def add_question(request):
    AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=3)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        answer_formset = AnswerFormSet(request.POST)

        if question_form.is_valid() and answer_formset.is_valid():
            question = question_form.save()
            answer_formset.instance = question
            answer_formset.save()
            return redirect('projects:projects')
    else:
        question_form = QuestionForm()
        answer_formset = AnswerFormSet()

    context = {
        'question_form': question_form,
        'answer_formset': answer_formset,
    }
    return render(request, 'quizes/add_question.html', context)
