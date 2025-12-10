# LingoLab Project File Structure

## 📁 Complete Directory Tree

```
LingoLab/
├── final/                                      # Django Project Root
│   ├── db.sqlite3                              # SQLite Database
│   ├── manage.py                               # Django Management CLI
│   ├── package.json                            # Node.js Dependencies
│   ├── package-lock.json                       # Node.js Lock File
│   ├── node_modules/                           # Node.js Packages
│   ├── socket_server.js                        # Socket.IO Server (Port 3001)
│   ├── media/                                  # User Uploads & Media
│   │   └── LingoLab/profile/                   # Learner Profile Pictures
│   │
│   ├── final/                                  # Django Project Configuration
│   │   ├── __init__.py
│   │   ├── settings.py                         # Django Settings (Database, Apps, Middleware)
│   │   ├── urls.py                             # Main URL Router
│   │   ├── wsgi.py                             # WSGI Application Entry Point
│   │   └── asgi.py                             # ASGI Application Entry Point
│   │
│   ├── Lingolab/                               # Main Django Application
│   │   ├── migrations/                         # Database Migration Files
│   │   │   └── __init__.py
│   │   ├── templates/
│   │   │   └── Lingolab/
│   │   │       ├── layout.html                 # Base Template (navbar, footer)
│   │   │       ├── components/
│   │   │       │   ├── head.html               # HTML Head (CSS, Meta)
│   │   │       │   ├── navbar.html             # Navigation Bar
│   │   │       │   ├── sidebar.html            # Sidebar Navigation
│   │   │       │   └── modals.html             # Reusable Modals
│   │   │       ├── index.html                  # Landing/Home Page
│   │   │       ├── signin.html                 # Login Form
│   │   │       ├── signup.html                 # User Registration
│   │   │       ├── dashboard.html              # Mentor Analytics Dashboard
│   │   │       ├── learners.html               # Learner List & Registration
│   │   │       ├── tracker.html                # Individual Learner Metrics
│   │   │       ├── quiz-me.html                # Quiz Interface
│   │   │       └── quiz-me-scoring.html        # Quiz Results & Scoring
│   │   │
│   │   ├── static/
│   │   │   └── Lingolab/
│   │   │       ├── css/
│   │   │       │   └── style.css               # Global Styles
│   │   │       ├── js/
│   │   │       │   └── main.js                 # JavaScript Logic
│   │   │       └── images/                     # Icons, Logos, Assets
│   │   │
│   │   ├── __init__.py
│   │   ├── admin.py                            # Django Admin Configuration
│   │   ├── apps.py                             # App Configuration
│   │   ├── models.py                           # Database Models
│   │   │   ├── User                            # Mentor/Admin User
│   │   │   ├── Learner                         # Student Profile
│   │   │   ├── QuizTaken                       # Quiz Attempt History
│   │   │   └── currentQuizzes                  # Active Quiz Items
│   │   ├── views.py                            # View Logic & API Endpoints
│   │   ├── urls.py                             # App URL Patterns
│   │   ├── tests.py                            # Unit Tests
│   │   ├── story_english.txt                   # English Text Corpus (Markov Model)
│   │   ├── story_tagalog.txt                   # Tagalog Text Corpus (Markov Model)
│   │   └── words_tagalog.txt                   # Tagalog Vocabulary List
│   │
│   └── LingoLab-Learner/                       # React Native (Expo) Mobile App
│       ├── app/
│       │   ├── _layout.js                      # Expo Router Layout
│       │   ├── index.jsx                       # Home/Landing Screen
│       │   ├── quiz.js                         # Quiz Game Screen
│       │   └── scanner.js                      # QR Code Scanner Screen
│       │
│       ├── components/
│       │   ├── BgmAudio.js                     # Background Music Toggle Hook
│       │   └── Particles.jsx                   # Particle Animation Component
│       │
│       ├── constants/
│       │   └── colors.js                       # Color Palette & Theme
│       │
│       ├── package.json                        # React Native Dependencies
│       ├── app.json                            # Expo Configuration
│       ├── babel.config.js                     # Babel Transpiler Config
│       ├── .gitignore
│       └── node_modules/
│
├── Include/                                    # Python Virtual Environment Headers
├── Lib/                                        # Python Virtual Environment Libraries
│   └── site-packages/                          # Installed Packages (Django, markovify, Pillow, etc.)
│
├── Scripts/                                    # Python Virtual Environment Scripts
│   ├── activate                                # Activate venv (bash)
│   ├── activate.bat                            # Activate venv (cmd)
│   ├── Activate.ps1                            # Activate venv (PowerShell)
│   ├── deactivate.bat
│   └── __pycache__/
│
├── pyvenv.cfg                                  # Virtual Environment Config
├── APP_DOCUMENTATION.md                        # Full Application Documentation
├── BUG_REPORT.md                               # Bug Tracking & Issues
└── README.md                                   # Project README
```

---

## 📊 Component Relationships

### Backend (Django)

```
Django Settings (final/settings.py)
    ↓
Django URLs (final/urls.py)
    ↓
Lingolab URLs (Lingolab/urls.py) → Views (Lingolab/views.py)
    ↓
Models (Lingolab/models.py)
    ↓
SQLite Database (db.sqlite3)
```

### Frontend (React Native)

```
Expo Router (_layout.js)
    ↓
    ├── index.jsx (Home Screen)
    ├── scanner.js (QR Scanner)
    └── quiz.js (Quiz Game)
        ↓
    components/ (BgmAudio, Particles)
    constants/ (colors.js)
```

### Data Flow

```
Mobile App (React Native)
    ↓
QR Code Scanner
    ↓
Django Backend API
    ↓
Database (currentQuizzes, QuizTaken)
    ↓
Mentor Dashboard (HTML Templates)
```

---

## 🔑 Key Files Overview

| File                   | Purpose                                        | Type                      |
| ---------------------- | ---------------------------------------------- | ------------------------- |
| `final/settings.py`    | Django configuration, database, installed apps | Python                    |
| `Lingolab/models.py`   | Database schema (User, Learner, QuizTaken)     | Python                    |
| `Lingolab/views.py`    | API endpoints & page rendering                 | Python                    |
| `Lingolab/urls.py`     | URL routing configuration                      | Python                    |
| `quiz.js`              | Quiz game logic, timer, scoring                | JavaScript (React Native) |
| `scanner.js`           | QR code parsing & navigation                   | JavaScript (React Native) |
| `quiz-me-scoring.html` | Quiz results display & mentor scoring          | HTML/Jinja2               |
| `dashboard.html`       | Analytics & progress charts                    | HTML/Jinja2               |
| `story_english.txt`    | English sentence corpus                        | Text                      |
| `story_tagalog.txt`    | Tagalog sentence corpus                        | Text                      |
| `words_tagalog.txt`    | Tagalog vocabulary list                        | Text                      |

---

## 🗂️ Directory Purpose Guide

| Directory             | Contents                     | Usage                           |
| --------------------- | ---------------------------- | ------------------------------- |
| `final/`              | Django project configuration | Core settings, WSGI/ASGI        |
| `Lingolab/`           | Main Django app              | Models, views, URLs, templates  |
| `Lingolab/templates/` | HTML templates               | Jinja2 templates for rendering  |
| `Lingolab/static/`    | CSS, JS, images              | Frontend assets                 |
| `LingoLab-Learner/`   | React Native app             | Mobile app source code          |
| `media/`              | Uploaded files               | User profile pictures           |
| `Lib/site-packages/`  | Python packages              | Django, markovify, Pillow, etc. |
| `Scripts/`            | Virtual env scripts          | Python environment activation   |

---

## 🚀 Running the Project

### Django Backend

```bash
cd LingoLab/final
python manage.py runserver
# Access at: http://127.0.0.1:8000/
```

### Socket.IO Server

```bash
cd LingoLab/final
npm install socket.io
node socket_server.js
# Running on: localhost:3001
```

### React Native App

```bash
cd LingoLab/final/LingoLab-Learner
npm start
# Scan with Expo Go app or press 'a' for Android emulator
```

---

## 📝 Summary

**LingoLab** follows a **three-tier architecture**:

1. **Backend**: Django REST API + SQLite database
2. **Frontend**: React Native (Expo) mobile app + Jinja2 web templates
3. **Real-time**: Socket.IO server for live event communication

The project supports **bilingual learning** (English/Tagalog) with features for:

- Mentor dashboard analytics
- QR code-based quiz distribution
- Real-time pronunciation scoring
- Learner progress tracking
