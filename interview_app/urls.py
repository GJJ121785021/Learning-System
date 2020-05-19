from django.urls import path, include
from django.views.generic import TemplateView

from interview_app import views

app_name = 'interview_app'


api_patterns = [
    path('interview_questions/', views.InterviewView.as_view(), name='interviewquestion-list'),
    path('interview_questions/<int:pk>/', views.InterviewDetailView.as_view(), name='interviewquestion-detail'),
]


urlpatterns = [
    path('', TemplateView.as_view(template_name='interview_app/index.html'), name='index'),
    path('add_question/', TemplateView.as_view(template_name='interview_app/add_question.html'), name='add_question'),
    path('delete_question/', TemplateView.as_view(template_name='interview_app/delete_question.html'), name='delete_question'),


    path('api/', include(api_patterns)),
]

