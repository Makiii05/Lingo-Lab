from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # pages
    path('', views.index, name='index'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('learners', views.learners, name='learners'),
    path('tracker/<int:learner_id>', views.tracker, name='tracker'),
    path('quiz-me-scoring', views.quiz_me_scoring, name='quiz-me-scoring'),

    # #functions
    path('register-learner', views.register_learner, name='register-learner'),
    path('get-sentences/<int:number>/<str:language>/', views.get_sentences, name='get-sentences'),
    path('tracker/get-sentences/<int:number>/<str:language>/', views.get_sentences, name='tracker-get-sentences'),
    path('get-tagalog-word/<int:length>/<int:number>', views.get_tagalog_word, name='get-tagalog-word'),
    path('tracker/get-tagalog-word/<int:length>/<int:number>', views.get_tagalog_word, name='tracker-get-tagalog-word'),
    path('submit-score', views.submit_score, name='submit-score'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)