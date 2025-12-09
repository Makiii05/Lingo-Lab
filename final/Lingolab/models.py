from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db.models import Avg

class User(AbstractUser):
    pass

class Learner(models.Model):
    name = models.CharField(max_length=64)
    profile_picture = models.ImageField(upload_to='LingoLab/profile/', default='LingoLab/profile/default.jpg', blank=True)
    grade = models.CharField(max_length=64)
    age = models.IntegerField()
    score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    mentor_id = models.ForeignKey(User, related_name="mentor", on_delete=models.CASCADE)
    
    def get_profile_picture_url(self):
        """Return profile picture URL or a placeholder if it doesn't exist"""
        if self.profile_picture and self.profile_picture.name:
            try:
                return self.profile_picture.url
            except Exception:
                return '/static/images/default-avatar.png'
        return '/static/images/default-avatar.png'
    
class QuizTaken(models.Model):
    learner_id = models.ForeignKey(Learner, related_name="quizzes_taken", on_delete=models.CASCADE)
    language = models.CharField(max_length=64, blank=True)
    type = models.CharField(max_length=64, blank=True)
    number_of_questions = models.PositiveIntegerField(default=0)
    words_length = models.PositiveIntegerField(default=0)
    time_limit = models.PositiveIntegerField(help_text="seconds", default=0)
    date = models.DateTimeField(default=timezone.now)
    # wpm for sentence
    speed = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    # accuracy for word
    correctness = models.PositiveSmallIntegerField(null=True, blank=True)
    # miscues
    stutter = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    repetition = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pause = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    pronunciation = models.PositiveSmallIntegerField(null=True, blank=True)
    # other
    total_words = models.PositiveIntegerField(default=0)
    comment = models.TextField(null=True, blank=True)
    score = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    
    