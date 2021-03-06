# Generated by Django 2.2.7 on 2020-05-03 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExaminationModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('total', models.PositiveSmallIntegerField(default=10, verbose_name='总题数')),
                ('correct_num', models.PositiveSmallIntegerField(default=0, verbose_name='正确题数')),
                ('finished', models.BooleanField(default=False, verbose_name='是否完成')),
            ],
            options={
                'verbose_name': '测验',
                'verbose_name_plural': '测验',
                'db_table': 'examination',
            },
        ),
        migrations.CreateModel(
            name='WordModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('english', models.CharField(max_length=30, unique=True, verbose_name='单词')),
                ('chinese_translation', models.CharField(blank=True, max_length=250, null=True, verbose_name='汉语意思')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('translate_into_chinese_total', models.PositiveSmallIntegerField(default=0, verbose_name='翻译成中文的总次数')),
                ('translate_into_chinese_success', models.PositiveSmallIntegerField(default=0, verbose_name='翻译成中文正确的次数')),
                ('translate_into_english_total', models.PositiveSmallIntegerField(default=0, verbose_name='中译英总次数')),
                ('translate_into_english_success', models.PositiveSmallIntegerField(default=0, verbose_name='中译英正确的次数')),
                ('is_delete', models.BooleanField(default=False, verbose_name='已逻辑删除')),
            ],
            options={
                'verbose_name': '单词',
                'verbose_name_plural': '单词',
                'db_table': 'english_word',
                'ordering': ['-create_time'],
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='QuestionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(default=None, max_length=50, verbose_name='输入的答案')),
                ('is_correct', models.BooleanField(default=False, verbose_name='是否正确')),
                ('examination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='english_app.ExaminationModel', verbose_name='属于哪次测验')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='english_app.WordModel', verbose_name='是哪个单词')),
            ],
            options={
                'verbose_name': '详细题目',
                'verbose_name_plural': '详细题目',
                'db_table': 'question',
                'unique_together': {('examination', 'word')},
            },
        ),
    ]
