from django.db import models


class InterviewQuestion(models.Model):
    question = models.CharField(max_length=255, null=False, unique=True, verbose_name='面试题目')
    answer = models.TextField(max_length=2000, null=True, verbose_name='面试题答案')
    create_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='创建时间')

    def __str__(self):
        return self.question[:20]

    class Meta:
        db_table = 'interview_question'
        ordering = ['-create_time']
        verbose_name = '面试题'
        verbose_name_plural = verbose_name
