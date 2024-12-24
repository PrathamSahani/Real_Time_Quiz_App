from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('quiz/', views.quiz, name='quiz'),
    path('api/get-quiz/', views.get_quiz, name='get_quiz'),
    path('api/submit-quiz/', views.submit_quiz, name='submit_quiz'),  # New endpoint for submitting the quiz
    path('create-quiz/', views.create_quiz, name='create_quiz'),
    path('all-quizzes/', views.all_quizzes, name='all_quizzes'),
    path('edit-quiz/<uuid:uid>/', views.edit_quiz, name='edit_quiz'),
    path('delete-quiz/<uuid:uid>/', views.delete_quiz, name='delete_quiz'),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('profile/', views.profile, name='profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
]

