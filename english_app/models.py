from django.db import models


class WordModel(models.Model):
    english = models.CharField(max_length=30, null=False, unique=True, verbose_name='单词')
    chinese_translation = models.CharField(max_length=100, blank=True, null=True, verbose_name='汉语意思')
    create_time = models.DateField(auto_now=True, null=False, verbose_name='添加时间')

    def __str__(self):
        return self.english

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.chinese_translation:
            # TODO 接入翻译API
            self.chinese_translation = '由翻译API提供'
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        db_table = 'English_word'
        ordering = ['-create_time']
        verbose_name = '单词'
        verbose_name_plural = '单词'

