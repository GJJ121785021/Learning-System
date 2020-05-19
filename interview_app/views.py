from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics

from interview_app.models import InterviewQuestion
from interview_app.serializers import InterviewSerializer


class InterviewView(generics.ListCreateAPIView):
    queryset = InterviewQuestion.objects.all()
    serializer_class = InterviewSerializer


class InterviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InterviewQuestion.objects.all()
    serializer_class = InterviewSerializer



