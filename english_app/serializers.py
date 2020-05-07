from rest_framework import serializers

from english_app.models import WordModel


class WordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WordModel
        fields = ['url', 'english', 'chinese_translation']

