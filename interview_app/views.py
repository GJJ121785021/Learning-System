from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics

from interview_app.models import InterviewQuestion
from interview_app.serializers import InterviewSerializer


def index(request):
    return render(request, 'interview_app/index.html')


def add_question(request):
    return render(request, 'interview_app/add_question.html')


def delete_question(request):
    return render(request, 'interview_app/delete_question.html')


class InterviewView(generics.ListCreateAPIView):
    queryset = InterviewQuestion.objects.all()
    serializer_class = InterviewSerializer


class InterviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InterviewQuestion.objects.all()
    serializer_class = InterviewSerializer



