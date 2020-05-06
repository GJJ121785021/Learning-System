import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from english_app.english_app_constant import RESULT_RIGHT, RESULT_FAULT
from english_app.models import WordModel
from rest_framework import generics

from rest_framework.filters import OrderingFilter, SearchFilter
from english_app.serializers import WordSerializer

from django.core import serializers as django_serializers


def home(request):
    return render(request, 'home.html', {'test_data': '传递参数成功'})


def index(request):
    return render(request, 'english_app/index.html')


def random_word(request):
    return render(request, 'english_app/random_word.html')


def all_words(request):
    return render(request, 'english_app/all_words.html')


def add_word(request):
    return render(request, 'english_app/add_word.html')


class WordListView(generics.ListCreateAPIView):
    queryset = WordModel.objects.all()
    serializer_class = WordSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['create_time']
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['create_time', 'english']
    search_fields = ['english', 'chinese_translation']

    def get_queryset(self):
        if self.request.query_params.get('ordering') == 'error':
            return super().get_queryset().filter(english__startswith='e')
        return super().get_queryset()


class WordDetailView(generics.RetrieveDestroyAPIView):
    queryset = WordModel.objects.all()
    serializer_class = WordSerializer


class Random_word(APIView):
    def get(self, request):
        count = 30
        while count:
            random_id = random.choice(WordModel.objects.values_list('pk', flat=True))
            try:
                word = WordModel.objects.get(pk=random_id)
                # 在这里根据正确率稍微筛选一下
                if word.translate_into_chinese_total != 0:
                    success_odds = word.translate_into_chinese_success / word.translate_into_chinese_total
                    if random.random() <= success_odds:
                        count -= 1
                        continue
                return JsonResponse({'english': word.english})
            except WordModel.DoesNotExist:
                print('单词在查询之前已被删除')
                count -= 1
        return JsonResponse({'msg': '未找到合适的单词', 'english': 'python'}, status=400)

    def post(self, request):
        english = request.data.get('english')
        into_chinese_translation = request.data.get('chinese_translation')
        if not (english and into_chinese_translation):
            return JsonResponse({'msg': '请输入正确的信息'}, status=400)
        try:
            word = WordModel.objects.get(english=english)
        except WordModel.DoesNotExist:
            return JsonResponse({'msg': '单词不存在'}, status=400)
        data = {'english': english, 'chinese_translation': word.chinese_translation}
        word.translate_into_chinese_total = word.translate_into_chinese_total + 1
        if into_chinese_translation in word.chinese_translation:
            word.translate_into_chinese_success = word.translate_into_chinese_success + 1
            word.save()
            data['status'] = RESULT_RIGHT
            data['msg'] = '上题答案正确'
            return JsonResponse(data)
        else:
            word.save()
            data['status'] = RESULT_FAULT
            data['msg'] = '上题答案错误'
            return JsonResponse(data)
