from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Types, Question, Answer
import random
import json


from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')

from .models import QuizAttempt

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url='/login/')
def leaderboard(request):
    category = request.GET.get('category', 'all')  
    if category == 'all':
        user_attempts = QuizAttempt.objects.filter(user=request.user).order_by('-timestamp')
    else:
        user_attempts = QuizAttempt.objects.filter(
            user=request.user,
            question__gfg__gfg_name__iexact=category
        ).order_by('-timestamp')

    # Initialize performance metrics
    total_score = sum(attempt.score for attempt in user_attempts)
    total_correct = sum(attempt.correct_answers for attempt in user_attempts)
    total_incorrect = sum(attempt.incorrect_answers for attempt in user_attempts)
    total_unattempted = sum(attempt.unattempted for attempt in user_attempts)

    # Prepare leaderboard data for display
    leaderboard_data = [
        {
            'quiz': attempt.question.gfg.gfg_name,
            'timestamp': attempt.timestamp,
            'score': attempt.score,
            'status': attempt.status,
            'correct_answers': attempt.correct_answers,
            'incorrect_answers': attempt.incorrect_answers,
            'unattempted': attempt.unattempted,
        }
        for attempt in user_attempts
    ]

    # Add pagination
    paginator = Paginator(leaderboard_data, 5)  # Show 10 entries per page
    page = request.GET.get('page')
    try:
        paginated_data = paginator.page(page)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)

    # Fetch all categories
    categories = Types.objects.values_list('gfg_name', flat=True)

    context = {
        'leaderboard_data': paginated_data,  # Pass the paginated data
        'categories': categories,
        'total_score': total_score,
        'total_correct': total_correct,
        'total_incorrect': total_incorrect,
        'total_unattempted': total_unattempted,
        'selected_category': category,
    }
    return render(request, 'leaderboard.html', context)

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('login')

    return render(request, 'login.html')

# Registration view
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Check if passwords match
        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'register.html')

# Logout view
@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('index')



def home(request):
    context = {'catgories': Types.objects.all()}
    if request.GET.get('gfg'):
        return redirect(f"/quiz/?gfg={request.GET.get('gfg')}")
    return render(request, 'home.html', context)


def quiz(request):
    category = request.GET.get('gfg', 'all')  # Default to 'all' if no category is selected
    if category == 'all' or not category:
        questions = Question.objects.all()
    else:
        questions = Question.objects.filter(gfg__gfg_name__iexact=category)
    
    context = {
        'gfg': category,
        'questions': questions,
    }
    return render(request, 'quiz.html', context)


def get_quiz(request):
    try:
        category = request.GET.get('gfg', 'all')  # Default to 'all'
        if category == 'all' or not category:
            question_objs = Question.objects.all()
        else:
            question_objs = Question.objects.filter(gfg__gfg_name__icontains=category)
        
        question_objs = list(question_objs)
        random.shuffle(question_objs)
        data = [
            {
                "uid": question.uid,
                "gfg": question.gfg.gfg_name,
                "question": question.question,
                "marks": question.marks,
                "answer": question.get_answers(),  # Ensure get_answers returns correct answers
            }
            for question in question_objs
        ]
        payload = {'status': True, 'data': data}
        return JsonResponse(payload)
    except Exception as e:
        return JsonResponse({"status": False, "message": str(e)})

from django.http import JsonResponse
import json
from django.http import JsonResponse
import json
from .models import Question

from django.http import JsonResponse
import json
from .models import Question


from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
import json

def submit_quiz(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_answers = data.get('answers', {})
            score = 0
            correct = 0
            incorrect = 0
            unattempted = 0

            for question_uid, user_answer in user_answers.items():
                question = Question.objects.get(uid=question_uid)
                correct_answer = question.question_answer.filter(is_correct=True).first()

                if correct_answer and correct_answer.answer == user_answer:
                    score += question.marks
                    correct += 1
                else:
                    incorrect += 1

            unattempted = len(Question.objects.all()) - len(user_answers)

            if request.user.is_authenticated:
                # Log the attempt only if the user is authenticated
                QuizAttempt.objects.create(
                    user=request.user,
                    question=question,
                    timestamp=datetime.now(),
                    score=score,
                    correct_answers=correct,
                    incorrect_answers=incorrect,
                    unattempted=unattempted,
                    status="Passed" if score >= (len(user_answers) / 2) else "Failed"
                )

            return JsonResponse({'status': True, 'score': score})

        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})

    return JsonResponse({'status': False, 'message': 'Invalid request method'})



@login_required(login_url='/login/')
def create_quiz(request):
    # Ensure categories exist
    Types.create_default_categories()

    if request.method == "POST":
        category_name = request.POST.get("category")
        category = Types.objects.get(gfg_name=category_name)
        question_text = request.POST.get("question")
        marks = request.POST.get("marks")
        answers = request.POST.getlist("answers")
        correct_answer = request.POST.get("correct_answer")

        # Create the question
        question = Question.objects.create(gfg=category, question=question_text, marks=marks)

        # Add answers
        for answer_text in answers:
            is_correct = (answer_text == correct_answer)
            Answer.objects.create(question=question, answer=answer_text, is_correct=is_correct)

        return redirect('all_quizzes')

    context = {'categories': Types.objects.all()}
    return render(request, 'create_quiz.html', context)


def all_quizzes(request):
    questions = Question.objects.all()
    return render(request, 'all_quiz.html', {'questions': questions})

@login_required(login_url='/login/')
def edit_quiz(request, uid):
    question = get_object_or_404(Question, uid=uid)
    if request.method == "POST":
        category_name = request.POST.get("category")
        category = Types.objects.get(gfg_name=category_name)
        question_text = request.POST.get("question")
        marks = request.POST.get("marks")
        answers = request.POST.getlist("answers")
        correct_answer = request.POST.get("correct_answer")

        # Update question
        question.gfg = category
        question.question = question_text
        question.marks = marks
        question.save()

        # Update answers
        question.question_answer.all().delete()
        for answer_text in answers:
            is_correct = (answer_text == correct_answer)
            Answer.objects.create(question=question, answer=answer_text, is_correct=is_correct)

        return redirect('all_quizzes')

    # Fetch the correct answer
    correct_answer = question.question_answer.filter(is_correct=True).first()

    context = {
        'question': question,
        'categories': Types.objects.all(),
        'correct_answer': correct_answer.answer if correct_answer else '',
    }
    return render(request, 'edit_quiz.html', context)

@login_required(login_url='/login/')
def delete_quiz(request, uid):
    question = get_object_or_404(Question, uid=uid)
    question.delete()
    return redirect('all_quizzes')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django import forms

# Profile Update Form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

# Profile View
@login_required(login_url='/login/')
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')  # Redirect to the same page after saving
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'profile.html', {'form': form, 'user': user})

# Delete Account View
@login_required(login_url='/login/')
def delete_account(request):
    user = request.user
    if request.method == 'POST':
        user.delete()  # Delete the user account
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('index')  # Redirect to home page after account deletion
    
    return render(request, 'delete_account.html', {'user': user})
