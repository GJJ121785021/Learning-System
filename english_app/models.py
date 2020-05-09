from django.db import models
from you_dao_api import youdao


class WordManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_delete= False)


class WordModel(models.Model):
    english = models.CharField(max_length=30, null=False, unique=True, verbose_name='单词')
    chinese_translation = models.CharField(max_length=250, blank=True, null=True, verbose_name='汉语意思')
    create_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='添加时间')
    translate_into_chinese_total = models.PositiveSmallIntegerField(default=0, verbose_name='翻译成中文的总次数')
    translate_into_chinese_success = models.PositiveSmallIntegerField(default=0, verbose_name='翻译成中文正确的次数')
    translate_into_english_total = models.PositiveSmallIntegerField(default=0, verbose_name='中译英总次数')
    translate_into_english_success = models.PositiveSmallIntegerField(default=0, verbose_name='中译英正确的次数')
    is_delete = models.BooleanField('已逻辑删除', default=False)

    # 自定义的管理器，默认查询未删除的单词
    objects = WordManager()
    # base管理器，查询所有单词，包括已删除的（is_delete=True）
    all_objects = models.Manager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # 存入以前存过但是现在删除了的单词（把is_delete改为False）
        if WordModel.all_objects.filter(is_delete=True, english=self.english).exists():
            WordModel.all_objects.filter(english=self.english).update(is_delete=False)
            return
        # 如果没有存汉语翻译
        if not self.chinese_translation:
            # 由翻译API提供结果
            self.chinese_translation = youdao.english_translate_chinese(self.english)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.english

    class Meta:
        db_table = 'english_word'
        ordering = ['-create_time']
        verbose_name = '单词'
        verbose_name_plural = verbose_name
        # 用它的名字 指定一个默认使用的管理器， 如果不指定则会默认使用上面第一个声明的
        default_manager_name = 'objects'


class ExaminationModel(models.Model):
    """试卷"""
    create_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='创建时间')
    total = models.PositiveSmallIntegerField(default=10, verbose_name='总题数')
    correct_num = models.PositiveSmallIntegerField(default=0, verbose_name='正确题数')
    finished = models.BooleanField('是否完成', default=False)

    def __str__(self):
        return f'No.{self.pk} 测验'

    class Meta:
        db_table = 'examination'
        verbose_name = '测验'
        verbose_name_plural = verbose_name


class QuestionModel(models.Model):
    """试题"""
    examination = models.ForeignKey(ExaminationModel, on_delete=models.CASCADE, verbose_name='属于哪次测验')
    word = models.ForeignKey(WordModel, on_delete=models.CASCADE, verbose_name='是哪个单词')
    answer = models.CharField(max_length=50, default=None, verbose_name='输入的答案')
    is_correct = models.BooleanField('是否正确', default=False)

    def __str__(self):
        return f'{self.examination}.{self.word}'

    class Meta:
        unique_together = ['examination', 'word']
        db_table = 'question'
        verbose_name = '详细题目'
        verbose_name_plural = verbose_name
