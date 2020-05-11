from rest_framework import serializers

from english_app.models import WordModel, ExaminationModel, QuestionModel


class WordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WordModel
        fields = ['url', 'english', 'chinese_translation']


class QuestionListingField(serializers.RelatedField):
    def to_representation(self, value):
        return {'english': value.word.english, 'answer': value.answer}


class ExaminationSerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionListingField(many=True, read_only=True)
    correct_odds = serializers.SerializerMethodField(label='正确率')

    class Meta:
        model = ExaminationModel
        fields = ['id', 'url', 'total', 'correct_num', 'finished', 'questions', 'correct_odds']

    def get_correct_odds(self, obj):
        return f'{round(obj.correct_num / obj.total, 4) * 100}%'

