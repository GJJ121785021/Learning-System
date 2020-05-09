import random

from django.db import transaction
from django.db.models import F
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from english_app.english_app_constant import RESULT_RIGHT, RESULT_FAULT
from english_app.models import WordModel, ExaminationModel, QuestionModel
from rest_framework import generics

from rest_framework.filters import OrderingFilter, SearchFilter
from english_app.serializers import WordSerializer, ExaminationSerializer

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


def random_exam(request):
    return render(request, 'english_app/random_exam.html')


def history_exam(request):
    return render(request, 'english_app/history_exam.html')


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

    @transaction.atomic
    def post(self, request, format=None):
        # into data -> {words:[], answers:[]}
        if type(request.data) == QueryDict:
            words = request.data.getlist('words')
            answers = request.data.getlist('answers')
        else:  # if type(request.data) == dict:
            words = request.data.get('words')
            answers = request.data.get('answers')
        if (not words) or (not answers) or (len(words) != len(answers)):
            return Response({'status': RESULT_FAULT, 'msg': '错误提交'})
        # 提交无误后的逻辑
        try:
            # 使用Django事务
            with transaction.atomic():
                # 正确题数
                correct_num = 0
                # 创建一个试卷对象
                exam = ExaminationModel.objects.create(total=len(words))
                # 检查题目
                for item in zip(words, answers):
                    english, answer = item[0], item[1].strip()
                    word = WordModel.all_objects.get(english=english)
                    word.translate_into_chinese_total = word.translate_into_chinese_total + 1
                    if answer and (answer in word.chinese_translation):
                        correct_num += 1
                        QuestionModel.objects.create(examination=exam, word=word, answer=answer, is_correct=True)
                        word.translate_into_chinese_success = word.translate_into_chinese_success + 1
                    else:
                        QuestionModel.objects.create(examination=exam, word=word, answer=answer, is_correct=False)
                    # 更新单词的翻译次数
                    word.save(update_fields=['translate_into_chinese_total', 'translate_into_chinese_success'])
                # 更新试题对象
                exam.correct_num = correct_num
                exam.finished = True
                exam.save()
        except WordModel.DoesNotExist:
            return Response({'status': RESULT_FAULT, 'msg': '错误提交'})

        return Response({'status': RESULT_RIGHT, 'msg': '提交成功'})


# 这里的创建逻辑，是在每次提交试题时，而不是发布试题时
# 正规的是在发布时创建
# 提交试题时创建，则直接根据提交的表单创建，
# 发布时创建，可以把逻辑写在create中
class ExaminationView(generics.ListAPIView):
    queryset = ExaminationModel.objects.all()
    serializer_class = ExaminationSerializer


class ExaminationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExaminationModel.objects.all()
    serializer_class = ExaminationSerializer


