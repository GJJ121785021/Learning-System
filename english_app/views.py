import random

from django.db.models import F
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
        if self.request.query_params.get('ordering') == 'error_odds':
            queryset = super().get_queryset()
            # 这里按错误率排序，总数是0的计算结果为None（不报错），按空值排序（好像是在最前面）
            queryset = queryset.annotate(
                error_odds=F('translate_into_chinese_success') / F('translate_into_chinese_total'))
            return queryset.order_by('error_odds')
        return super().get_queryset()


class WordDetailView(generics.RetrieveDestroyAPIView):
    queryset = WordModel.objects.all()
    serializer_class = WordSerializer


def get_random_word():
    """返回一个随机单词
    目前也有可能不返回"""
    count = 30
    while count:
        random_id = random.choice(WordModel.objects.values_list('pk', flat=True))
        try:
            word = WordModel.objects.get(pk=random_id)
            # 在这里根据正确率稍微筛选一下
            if word.translate_into_chinese_total != 0:
                success_odds = word.translate_into_chinese_success / word.translate_into_chinese_total
                if random.random() <= success_odds * 0.7:  # 0.7只是一个调节平衡的值
                    count -= 1
                    continue
            return word.english
        except WordModel.DoesNotExist:
            print('单词在查询之前已被删除')
            count -= 1


class RandomWord(APIView):
    def get(self, request, format=None):
        english_word = get_random_word()
        if english_word:
            return JsonResponse({'english': english_word})
        else:
            last_word = WordModel.objects.last()
            if english_word:
                return JsonResponse({'english': last_word.english})
            return JsonResponse({'msg': '未找到合适的单词', 'english': 'python'}, status=400)

    def post(self, request, format=None):
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


def get_random_exam(question_num=10):
    # 得到随机的十个单词的列表
    count = 30
    words = []
    while count:
        word = get_random_word()
        if word not in words:
            words.append(word)
            if len(words) == question_num:
                return words
        else:
            count -= 1
    return words


class RandomExam(APIView):
    def get(self, request, format=None):
        if WordModel.objects.count() <= 10:
            return Response({'words': WordModel.objects.all().values_list('english', flat=True)})
        return Response({'words': get_random_exam()})

    def post(self, request, format=None):
        # into data -> {words:[], answers:[]}
        words = request.data.get('words')
        answers = request.data.get('answers')
        if (not words) or (not answers) or (len(words) != len(answers)):
            return Response({'status': RESULT_FAULT, 'msg': '错误提交'})
        # 提交无误后的逻辑


        return Response({'status': RESULT_RIGHT, 'msg': '提交成功'})
