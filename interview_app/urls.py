from django.urls import path

from interview_app import views

app_name = 'interview_app'


urlpatterns = [
    path('', views.index, name='index'),
]

