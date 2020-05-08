from rest_framework import serializers

from interview_app.models import InterviewQuestion


class InterviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = ['url', 'question', 'answer']

