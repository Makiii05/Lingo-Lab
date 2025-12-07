from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.db import IntegrityError
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
import os
import random
import json
import uuid
from django.conf import settings
import markovify
# Absolute path to your file
eng_file_path = os.path.join(settings.BASE_DIR, 'Lingolab', 'story_english.txt')
with open(eng_file_path, encoding='utf-8') as f:
    eng_text = f.read()
eng_model = markovify.Text(eng_text)

# Absolute path to your file
tag_file_path = os.path.join(settings.BASE_DIR, 'Lingolab', 'story_tagalog.txt')
with open(tag_file_path, encoding='utf-8') as f:
    tag_text = f.read()
tag_model = markovify.Text(tag_text)

# Load once at module import
word_file_path = os.path.join(settings.BASE_DIR, 'Lingolab', 'words_tagalog.txt')
with open(word_file_path, encoding='utf-8') as f:
    tagalog_words = [w.strip() for w in f if w.strip()]


from .models import User, Learner, QuizTaken

def generate_random_filename(file):
    """
    Generate a random filename while preserving the original file extension.
    """
    if not file:
        return None
    
    # Get file extension
    file_extension = os.path.splitext(file.name)[1]
    
    # Generate random filename with UUID
    random_filename = f"{uuid.uuid4().hex}{file_extension}"
    
    return random_filename

def index(request):
    return render(request, 'Lingolab/index.html')

# AUTHENTICATION
def signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        User = get_user_model()

        try:
            user_obj = User.objects.get(email__iexact=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return render(request, "Lingolab/signin.html", {
                "message": "Invalid email and/or password.",
                "color" : "red"
            })
    else:
        return render(request, 'Lingolab/signin.html')

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, 'Lingolab/signup.html', {
                "message": "Passwords must match."
            })
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as error:
            return render(request, "Lingolab/signup.html", {
                "message": str(error)
            })
        login(request, user)
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return render(request, 'Lingolab/signup.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("signin"))

# PAGE
def dashboard(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("signin"))

    mentor_id = request.user.id
    learners = Learner.objects.filter(mentor_id=mentor_id).count()
    quizzes_taken = QuizTaken.objects.filter(learner_id__mentor_id=mentor_id).count()
    ave_score = QuizTaken.objects.filter(learner_id__mentor_id=mentor_id).aggregate(Avg('score'))['score__avg'] or 0
    quizzes = QuizTaken.objects.filter(learner_id__mentor_id=mentor_id).order_by('-date')[:10]
    
    # Calculate weekly activity data (last 7 days)
    today = timezone.now()
    weekly_data = []
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    for i in range(6, -1, -1):  # Get last 7 days including today
        day = today - timedelta(days=i)
        start_of_day = day.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        daily_avg = QuizTaken.objects.filter(
            learner_id__mentor_id=mentor_id,
            date__gte=start_of_day,
            date__lt=end_of_day
        ).aggregate(Avg('score'))['score__avg'] or 0
        
        weekly_data.append({
            'day': days[(today - timedelta(days=i)).weekday()],
            'score': float(daily_avg)
        })
    
    return render(request, 'Lingolab/dashboard.html',{
        "learners_count" : learners,
        "quizzes_taken_count": quizzes_taken,
        "ave_score": round(ave_score, 2),
        "quizzes": quizzes,
        "weekly_data": weekly_data
    })

def learners(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("signin"))

    mentor_id = request.user.id
    learners = Learner.objects.filter(mentor_id=mentor_id).order_by('-score')
    return render(request, 'Lingolab/learners.html', {
        "learners": learners
    })

def tracker(request, learner_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("signin"))

    learner = Learner.objects.get(id=learner_id, mentor_id=request.user)
    speed = QuizTaken.objects.filter(learner_id=learner_id).aggregate(Avg('speed'))['speed__avg'] or 0  
    score = QuizTaken.objects.filter(learner_id=learner_id).aggregate(Avg('score'))['score__avg'] or 0
    stutter = QuizTaken.objects.filter(learner_id=learner_id).aggregate(Avg('stutter'))['stutter__avg'] or 0

    return render(request, 'Lingolab/tracker.html', {
        "learner": learner,
        "wpm": round(speed, 2),
        "score": round(score, 2),
        "stutter": round(stutter, 2),
        "quizzes": QuizTaken.objects.filter(learner_id=learner_id).order_by('-date')
    })

def quiz_me_scoring(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("signin"))

    if request.method != "POST":
        return HttpResponseRedirect(reverse("learners"))

    if request.method == "POST":
        data = json.loads(request.POST['quiz_data'])

    return render(request, 'Lingolab/quiz-me-scoring.html', {
        "data": data,
        "now": timezone.now()
    })

# HELPER
@csrf_exempt
def register_learner(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("signin"))

    if request.method == "POST":
        name = request.POST["name"]
        grade = request.POST["grade"]
        age = request.POST["age"]
        profile_picture = request.FILES.get("profile_picture")

        mentor_id = request.user

        # Generate random filename for profile picture
        if profile_picture:
            random_filename = generate_random_filename(profile_picture)
            profile_picture.name = random_filename

        learner = Learner(
            name=name,
            grade=grade,
            age=age,
            mentor_id=mentor_id,
            profile_picture=profile_picture
        )
        learner.save()

        return HttpResponseRedirect(reverse("tracker", args=[learner.id]))
    else:
        return render(request, 'Lingolab/learners.html')

def get_sentences(request, number, language):
    sentences = []
    for _ in range(number):
        if language == "english":
            sentence = eng_model.make_sentence(max_overlap_ratio=0.7, tries=100)
            
            if sentence is None:
                sentence = eng_model.make_short_sentence(120)
        elif language == "tagalog":
            sentence = tag_model.make_sentence(max_overlap_ratio=0.7, tries=100)
            
            if sentence is None:
                sentence = tag_model.make_short_sentence(120)
        
        sentences.append(sentence)
    
    return JsonResponse({"question": sentences})

def get_tagalog_word(request, length, number):
    number = int(number)  # ensure it’s an integer
    length = int(length)
    filtered_words = [w for w in tagalog_words if len(w) == length]
    words = random.sample(filtered_words, min(number, len(filtered_words)))
    return JsonResponse({"words": words})

def submit_score(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("signin"))

    if request.method == "POST":
        # Create QuizTaken record
        learner_id = request.POST.get("name")
        try:
            learner = Learner.objects.get(id=learner_id)
        except Learner.DoesNotExist:
            return render(request, 'Lingolab/learners.html', {'error': 'Learner not found'})
         
        # Get form data
        language = request.POST.get("quiz_language")
        quiz_type = request.POST.get("type")
        number_of_questions = request.POST.get("number_of_questions")
        words_length = request.POST.get("words_length")
        time_limit = request.POST.get("time_limit")
        stutter_score = float(request.POST.get("stutter_score", 0))
        repetition_score = float(request.POST.get("repetition_score", 0))
        correctness_score = request.POST.get("correctness_score", "0").rstrip('%')
        pronunciation_score = request.POST.get("pronunciation_score", "0").rstrip('%')
        overall_score = request.POST.get("overall_score", "0").rstrip('%')
        comments = request.POST.get("quiz_comments", "")
        
        quiz_taken = QuizTaken(
            learner_id=learner,
            language=language,
            type=quiz_type,
            number_of_questions=number_of_questions,
            words_length=words_length,
            time_limit=time_limit,
            stutter=stutter_score,
            repetition=repetition_score,
            correctness=float(correctness_score),
            pronunciation=float(pronunciation_score),
            score=float(overall_score),
            comment=comments
        )
        quiz_taken.save()
        
        # Redirect to tracker
        return HttpResponseRedirect(reverse("tracker", args=[learner.id]))
    
    return HttpResponseRedirect(reverse("learners"))