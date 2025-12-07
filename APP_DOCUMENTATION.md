# LingoLab - Complete Application Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Database Models](#database-models)
5. [User Authentication](#user-authentication)
6. [Core Features](#core-features)
7. [API Endpoints](#api-endpoints)
8. [File Organization](#file-organization)
9. [How It Works](#how-it-works)

---

## 🎯 Project Overview

**LingoLab** is a Django-based web application designed for **language learning and pronunciation tracking**. It enables mentors to:
- Register and manage learners
- Track learner progress through language quizzes
- Analyze pronunciation, speed, and fluency metrics
- Generate spoken content for practice exercises using Markov text generation
- View detailed analytics and performance reports

### Key Purpose
LingoLab serves as a **mentor-led language learning platform** where mentors can create learner profiles, assign quizzes, and monitor performance metrics across multiple languages (English, Tagalog).

---

## 🛠 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django 5.2.8 |
| **Database** | SQLite3 |
| **Language** | Python 3.x |
| **Authentication** | Django Authentication System |
| **Text Generation** | Markovify (Markov Chain-based) |
| **Frontend** | HTML5, CSS3, JavaScript |
| **File Uploads** | Django ImageField |
| **API Responses** | JSON |

### Key Dependencies
- **markovify** - Generates random sentences from text models
- **django** - Web framework and ORM
- **PIL/Pillow** - Image handling (via ImageField)

---

## 📁 Project Structure

```
LingoLab/final/
├── db.sqlite3                          # SQLite database
├── manage.py                           # Django management commands
├── media/                              # User uploads (profile pictures)
│   └── LingoLab/profile/              # Profile picture storage
├── final/                              # Django project settings
│   ├── settings.py                     # Configuration
│   ├── urls.py                         # Main URL router
│   ├── wsgi.py                         # WSGI application
│   └── asgi.py                         # ASGI application
└── Lingolab/                           # Main Django app
    ├── models.py                       # Database models
    ├── views.py                        # View logic
    ├── urls.py                         # App URL patterns
    ├── admin.py                        # Django admin config
    ├── apps.py                         # App config
    ├── tests.py                        # Test suite
    ├── story_english.txt               # English text corpus
    ├── story_tagalog.txt               # Tagalog text corpus
    ├── words_tagalog.txt               # Tagalog word list
    ├── migrations/                     # Database migrations
    ├── static/                         # Static assets (CSS, JS, images)
    │   └── Lingolab/
    └── templates/                      # HTML templates
        └── Lingolab/
            ├── layout.html             # Base template
            ├── sidebar.html            # Sidebar component
            ├── modals.html             # Modal components
            ├── index.html              # Landing page
            ├── signin.html             # Login page
            ├── signup.html             # Registration page
            ├── dashboard.html          # Mentor dashboard
            ├── learners.html           # Learner management
            ├── tracker.html            # Learner progress tracker
            ├── quiz-me.html            # Quiz interface
            └── quiz-me-scoring.html    # Quiz results page
```

---

## 🗄 Database Models

### 1. **User Model**
Extends Django's `AbstractUser` for custom authentication.

```python
class User(AbstractUser):
    pass
```
- **Inherits**: username, email, password, first_name, last_name, etc.
- **Role**: Mentors/Teachers
- **Related to**: Learner (one-to-many)

---

### 2. **Learner Model**
Represents students/learners being taught.

```python
class Learner(models.Model):
    name                 # str, max 64 chars
    profile_picture      # Image, upload_to 'LingoLab/profile/'
    grade                # str, educational level
    age                  # int
    score                # Decimal, auto-calculated from QuizTaken
    mentor_id            # ForeignKey → User (CASCADE delete)
```

**Key Method:**
- `get_profile_picture_url()` - Returns profile picture URL or default placeholder

**Auto-Update Method:**
- `save()` - Automatically calculates average score from all associated quizzes

---

### 3. **QuizTaken Model**
Stores individual quiz attempt records with performance metrics.

```python
class QuizTaken(models.Model):
    learner_id              # ForeignKey → Learner
    language                # str, quiz language (English/Tagalog)
    type                    # str, quiz type (word/sentence)
    number_of_questions     # int, total questions
    words_length            # int, word difficulty level
    time_limit              # int, seconds allowed
    date                    # DateTime, auto-set on creation
    
    # Speech Metrics (both types)
    stutter                 # Decimal, stutter frequency %
    repetition              # Decimal, word repetition %
    
    # Sentence Metrics
    speed                   # Decimal, words per minute (WPM)
    pause                   # Decimal, pause duration (seconds)
    
    # Word Metrics
    correctness             # int, correct pronunciation %
    pronunciation           # int, clarity score %
    
    # Overall
    comment                 # text, mentor/system feedback
    score                   # Decimal, overall score (0-100)
```

**Relationships:**
- Many QuizTaken → One Learner (CASCADE delete)

---

## 🔐 User Authentication

### Authentication Flow

#### 1. **Sign Up** (`/Lingolab/signup`)
- User provides: username, email, password, confirmation
- Password validation (must match)
- User created via `User.objects.create_user()`
- User auto-logged in and redirected to dashboard
- Error handling for duplicate usernames

```python
def signup(request):
    # Validates password match
    # Creates user
    # Handles IntegrityError for duplicates
    # Auto-login and redirect
```

#### 2. **Sign In** (`/Lingolab/signin`)
- User provides: email, password
- Email lookup (case-insensitive)
- Authentication against stored password hash
- Session creation on success
- Redirect to dashboard on success

```python
def signin(request):
    user_obj = User.objects.get(email__iexact=email)
    user = authenticate(request, username=user_obj.username, password=password)
    # Sessions and redirects
```

#### 3. **Sign Out** (`/Lingolab/logout`)
- Clears user session
- Redirects to sign-in page

### Session Management
- Django session middleware handles user state
- Login required decorator protects views
- Redirect to signin for unauthenticated access

---

## ✨ Core Features

### 1. **Dashboard** (`/Lingolab/dashboard`)
**Overview for mentors showing:**
- Total learners count
- Total quizzes taken
- Average score across all learners
- Recent 10 quizzes
- **Weekly Activity Chart** - Last 7 days average scores by day

```python
def dashboard(request):
    - Calculates learners_count, quizzes_taken_count
    - Aggregates average scores
    - Generates 7-day weekly_data for charts
    - Returns context with all metrics
```

---

### 2. **Learner Management** (`/Lingolab/learners`)
**Features:**
- View all registered learners (sorted by score descending)
- Register new learners with profile picture
- Click learner to view detailed tracker

#### Learner Registration (`/Lingolab/register-learner`)
**Form Fields:**
- Name (required)
- Grade (required)
- Age (required)
- Profile Picture (optional, auto-renamed with UUID)

**File Upload Security:**
- Profile pictures renamed with UUID to prevent name collisions
- Stored in `media/LingoLab/profile/` directory
- Preserves original file extension

```python
def register_learner(request):
    # Validates authentication
    # Gets form data
    # Generates random filename for profile picture
    # Creates Learner instance
    # Redirects to learner's tracker
```

---

### 3. **Learner Tracker** (`/Lingolab/tracker/<learner_id>`)
**Displays individual learner metrics:**
- Learner profile information
- Average WPM (Words Per Minute) - Speaking speed
- Average Score - Overall performance
- Average Stutter - Speech fluency metric
- Quiz history sorted by date (newest first)

```python
def tracker(request, learner_id):
    - Validates learner belongs to authenticated mentor (security)
    - Aggregates metrics from QuizTaken
    - Displays learner profile and history
```

---

### 4. **Quiz System**

#### 4.1 Sentence Generation (`/Lingolab/get-sentences/<number>/<language>/`)
**Purpose:** Generate random sentences for pronunciation practice

**Using Markov Models:**
- Pre-loaded text files into `markovify.Text` models
- Generates coherent sentences based on n-grams from corpus

**English Sentences:**
- Source: `story_english.txt`
- Model: `eng_model.make_sentence()` with 0.7 overlap ratio
- Fallback: `eng_model.make_short_sentence(120)` if generation fails

**Tagalog Sentences:**
- Source: `story_tagalog.txt`
- Same generation logic as English
- Supports bilingual practice

```python
def get_sentences(request, number, language):
    - Iterates 'number' times
    - Calls appropriate language model
    - Returns JSON array of sentences
```

**Response:**
```json
{
    "sentences": [
        "This is a generated sentence.",
        "Another random sentence here.",
        ...
    ]
}
```

---

#### 4.2 Word Generation (`/Lingolab/get-tagalog-word/<length>/<number>`)
**Purpose:** Generate Tagalog words of specific length for pronunciation drills

**Process:**
1. Loads word list from `words_tagalog.txt`
2. Filters words by exact character length
3. Randomly samples without replacement

```python
def get_tagalog_word(request, length, number):
    - Filters words by length
    - Uses random.sample() for diversity
    - Returns JSON array of words
```

**Response:**
```json
{
    "words": ["salita", "bahay", "libro", ...]
}
```

---

#### 4.3 Quiz Submission (`/Lingolab/submit-score`)
**Receives:** Quiz results with performance metrics

**Form Data Expected:**
- `name` - Learner ID
- `quiz_language` - Language practiced (English/Tagalog)
- `type` - Quiz type (word/sentence)
- `number_of_questions` - Total questions in quiz
- `words_length` - Word difficulty
- `time_limit` - Time taken (seconds)
- `stutter_score` - Speech stuttering metric
- `repetition_score` - Word repetition metric
- `correctness_score` - Pronunciation correctness %
- `pronunciation_score` - Overall clarity %
- `overall_score` - Final quiz score %
- `quiz_comments` - Feedback/comments

**Processing:**
```python
def submit_score(request):
    - Validates authentication
    - Fetches learner (with error handling)
    - Creates QuizTaken record with metrics
    - Learner.save() triggers auto-score update
    - Redirects to learner tracker
```

**Data Persistence:**
- All metrics stored in `QuizTaken` model
- Learner's average score auto-updated
- Historical data retained for analytics

---

#### 4.4 Quiz Scoring Interface (`/Lingolab/quiz-me-scoring`)
**Purpose:** Display quiz results and metrics

```python
def quiz_me_scoring(request):
    - Requires POST method with quiz_data JSON
    - Parses quiz data
    - Renders scoring template with data
```

---

## 🔗 API Endpoints

| Method | URL | Function | Purpose |
|--------|-----|----------|---------|
| GET | `/Lingolab/` | index | Landing page |
| GET/POST | `/Lingolab/signin` | signin | User login |
| GET/POST | `/Lingolab/signup` | signup | User registration |
| GET | `/Lingolab/logout` | logout_view | Logout & clear session |
| GET | `/Lingolab/dashboard` | dashboard | Mentor analytics |
| GET | `/Lingolab/learners` | learners | List all learners |
| GET/POST | `/Lingolab/register-learner` | register_learner | Add new learner |
| GET | `/Lingolab/tracker/<id>` | tracker | Individual learner stats |
| GET | `/Lingolab/get-sentences/<num>/<lang>/` | get_sentences | Generate practice sentences |
| GET | `/Lingolab/get-tagalog-word/<len>/<num>` | get_tagalog_word | Generate word drills |
| GET/POST | `/Lingolab/quiz-me-scoring` | quiz_me_scoring | Display quiz results |
| POST | `/Lingolab/submit-score` | submit_score | Save quiz attempt |

---

## 📁 File Organization

### Text Corpora (Markov Training Data)
- **`story_english.txt`** - English sentences for sentence generation
- **`story_tagalog.txt`** - Tagalog sentences for sentence generation
- **`words_tagalog.txt`** - Tagalog vocabulary word list (one per line)

### Media Directory
- **`media/LingoLab/profile/`** - Stores learner profile pictures
- Default avatar: `LingoLab/profile/default.jpg`

### Templates (`templates/Lingolab/`)
| Template | Purpose |
|----------|---------|
| `layout.html` | Base template with navbar, footer |
| `sidebar.html` | Navigation sidebar component |
| `modals.html` | Reusable modal dialogs |
| `index.html` | Landing/home page |
| `signin.html` | Login form |
| `signup.html` | Registration form |
| `dashboard.html` | Mentor dashboard with charts |
| `learners.html` | Learner list & registration form |
| `tracker.html` | Individual learner metrics |
| `quiz-me.html` | Quiz interface |
| `quiz-me-scoring.html` | Quiz results display |

### Static Assets (`static/Lingolab/`)
- CSS stylesheets
- JavaScript files (quiz logic, API calls)
- Images and icons

---

## 🎮 How It Works - User Flow

### Mentor Workflow

```
1. SIGNUP/LOGIN
   ↓
2. DASHBOARD
   ├─ View overall statistics
   ├─ See recent quiz activity
   └─ Check weekly performance trends
   ↓
3. LEARNERS PAGE
   ├─ View all registered learners
   ├─ Sort by performance score
   └─ Register new learner
      ├─ Enter: name, grade, age
      └─ Upload: profile picture (auto-renamed)
   ↓
4. TRACKER (per Learner)
   ├─ View learner profile
   ├─ Check performance metrics (WPM, score, stutter)
   ├─ Review quiz history
   └─ Analyze trends
```

### Learner Quiz Workflow

```
1. QUIZ GENERATION
   ├─ Type Selection (word/sentence)
   ├─ Language Selection (English/Tagalog)
   └─ Difficulty Selection (word length/number of questions)
   ↓
2. QUIZ CONTENT LOADED
   ├─ API: /get-sentences/ or /get-tagalog-word/
   ├─ Frontend displays content
   └─ Learner completes quiz
   ↓
3. PERFORMANCE MEASUREMENT
   ├─ Calculate metrics:
   │  ├─ Stutter rate
   │  ├─ Repetition rate
   │  ├─ Speaking speed (WPM)
   │  ├─ Pronunciation accuracy
   │  └─ Overall score
   ↓
4. SUBMISSION
   ├─ POST to /submit-score/
   ├─ Create QuizTaken record
   ├─ Auto-update Learner.score
   └─ Redirect to Tracker
   ↓
5. FEEDBACK
   ├─ View quiz results
   ├─ See performance metrics
   └─ Optional: Read mentor comments
```

---

## 🔄 Data Flow Diagram

```
USER AUTHENTICATION
    ↓
    ├─ Signup → Create User → Auto-login → Dashboard
    ├─ Signin → Authenticate → Create Session → Dashboard
    └─ Logout → Clear Session → Signin Page
    
LEARNER MANAGEMENT
    ↓
    ├─ Create Learner → Store Profile Picture (UUID renamed)
    ├─ View Learners → Query Learner.objects.filter(mentor_id=user)
    └─ Tracker → Aggregate metrics from QuizTaken

QUIZ GENERATION
    ↓
    ├─ Load Corpus → markovify.Text(corpus)
    ├─ Generate Content → make_sentence() or random.sample()
    └─ Return JSON → Frontend Display

QUIZ SUBMISSION
    ↓
    ├─ Receive Metrics → Parse POST data
    ├─ Create QuizTaken → Store in database
    ├─ Update Learner.score → Aggregate from QuizTaken
    └─ Display Results → Redirect to Tracker
```

---

## 🔧 Key Technologies & Techniques

### 1. **Markov Text Generation**
Uses `markovify` library to generate realistic sentences:
- Trains on corpus text files
- Generates n-gram based sentences
- Provides fallback to shorter sentences if generation fails

### 2. **Database Aggregation**
Django ORM aggregations for analytics:
```python
.aggregate(Avg('score'))['score__avg']  # Calculate average
.filter(...).count()                     # Count records
.order_by('-date')                       # Sort descending
```

### 3. **File Upload Security**
- UUID-based random filenames prevent collisions
- Original extension preserved for file type integrity
- Automatic upload path management via Django ImageField

### 4. **Authentication & Authorization**
- Django's built-in `authenticate()` and `login()` functions
- Session-based authentication
- View decorators for permission checks
- Learner ownership verification (mentor can only see own learners)

### 5. **API Design**
- RESTful JSON endpoints for dynamic content
- Stateless API calls for sentence/word generation
- POST submissions for data persistence

---

## 📊 Performance Metrics Explained

| Metric | Range | Meaning |
|--------|-------|---------|
| **Stutter** | 0-100% | Lower is better - frequency of hesitations |
| **Repetition** | 0-100% | Lower is better - unwanted word repetitions |
| **Speed (WPM)** | 0-∞ | Words per minute - reading/speaking rate |
| **Pause** | 0-∞ | Seconds - duration of pauses |
| **Correctness** | 0-100% | Higher is better - pronunciation accuracy |
| **Pronunciation** | 0-100% | Higher is better - overall speech clarity |
| **Score** | 0-100% | Overall quiz performance |

---

## 🚀 Deployment Considerations

### Settings to Update for Production
1. **DEBUG = False** (currently True)
2. **SECRET_KEY** - Move to environment variables
3. **ALLOWED_HOSTS** - Add production domain
4. **STATIC_ROOT** - Configure for static file collection
5. **Email Backend** - For production notifications
6. **Database** - Consider PostgreSQL instead of SQLite

### Security Improvements Needed
- HTTPS enforcement
- CSRF token validation
- SQL injection prevention (ORM handles this)
- XSS prevention
- Rate limiting on API endpoints
- Input validation on all forms

---

## 📝 Summary

**LingoLab** is a comprehensive language learning platform that:
- ✅ Enables mentors to manage and track learner progress
- ✅ Generates dynamic practice content (sentences, words)
- ✅ Measures multiple speech/pronunciation metrics
- ✅ Provides analytics and performance dashboards
- ✅ Supports bilingual learning (English & Tagalog)
- ✅ Handles secure file uploads with collision prevention
- ✅ Maintains historical data for trend analysis

The application is well-structured with clear separation of concerns, follows Django best practices, and provides a solid foundation for language learning and assessment.

