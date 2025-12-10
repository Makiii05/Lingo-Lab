from django.contrib import admin
from .models import User, Learner, QuizTaken, currentQuizzes

# Register your models here.

admin.site.register(User)
admin.site.register(Learner)
admin.site.register(QuizTaken)
admin.site.register(currentQuizzes)