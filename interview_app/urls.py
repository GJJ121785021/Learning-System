from django.urls import path, include

from interview_app import views

app_name = 'interview_app'


api_patterns = [
    path('interview_questions/', views.InterviewView.as_view(), name='interviewquestion-list'),
    path('interview_questions/<int:pk>/', views.InterviewDetailView.as_view(), name='interviewquestion-detail'),
]



urlpatterns = [
    path('', views.index, name='index'),
    path('add_question/', views.add_question, name='add_question'),
    path('delete_question/', views.delete_question, name='delete_question'),


    path('api/', include(api_patterns)),
]

