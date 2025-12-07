from django.contrib import admin
from .models import User, Learner, QuizTaken

# Register your models here.

admin.site.register(User)
admin.site.register(Learner)
admin.site.register(QuizTaken)