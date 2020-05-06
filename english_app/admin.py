from django.contrib import admin
from english_app.models import *


admin.site.register([WordModel, ExaminationModel, QuestionModel])

