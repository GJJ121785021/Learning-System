from django.db import models
from you_dao_api import youdao


class WordManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_delete= False)


class WordModel(models.Model):
    english = models.CharField(max_length=30, null=False, unique=True, verbose_name='单词')
    chinese_translation = models.CharField(max_length=100, blank=True, null=True, verbose_name='汉语意思')
    create_time = models.DateField(auto_now=True, null=False, verbose_name='添加时间')
    translate_into_chinese_total = models.PositiveSmallIntegerField(default=0, verbose_name='翻译成中文的总次数')
    translate_into_chinese_success = models.PositiveSmallIntegerField(default=0, verbose_name='翻译成中文正确的次数')
    translate_into_english_total = models.PositiveSmallIntegerField(default=0, verbose_name='中译英总次数')
    translate_into_english_success = models.PositiveSmallIntegerField(default=0, verbose_name='中译英正确的次数')
    is_delete = models.BooleanField('已逻辑删除', default=False)

    # 自定义的管理器，默认查询未删除的单词
    objects = WordManager()
    # base管理器，查询所有单词，包括已删除的（is_delete=True）
    all_objects = models.Manager()

    def __str__(self):
        return self.english

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.chinese_translation:
            # 由翻译API提供结果
            self.chinese_translation = youdao.english_translate_chinese(self.english)
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        db_table = 'English_word'
        ordering = ['-create_time']
        verbose_name = '单词'
        verbose_name_plural = '单词'
        # 用它的名字 指定一个默认使用的管理器， 如果不指定则会默认使用上面第一个声明的
        default_manager_name = 'objects'
