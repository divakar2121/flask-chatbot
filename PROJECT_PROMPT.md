# 🏥 HealthGuard AI - Complete Project Prompt & Architecture

## 📋 PROJECT OVERVIEW

**Project Name:** HealthGuard AI - Insurance Policy Analyzer  
**Purpose:** AI-powered chatbot for analyzing health insurance policies in India  
**Deployment:** Diploi Cloud (https://my-dev--flsk-chtbt-th8v.diploi.me)  
**GitHub:** https://github.com/divakar2121/flask-chatbot

---

## 🏗️ SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                               │
│                   (index.html - Dark Theme)                            │
│  • Login/Profile Modal    • Quick Actions    • Chat Box            │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      FLASK APP                                 │
│                     (app/__init__.py)                          │
│  • Routes: main, chat, upload, sync, auth                          │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
          ┌─────────────────────┼─────────────────────┐
          ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  OPENROUTER API   │ │  DATABASE      │ │   SYNC         │
│ (openrouter.py)   │ │ (database.py)   │ │ (sync.py)       │
│                │ │                │ │                │
│ DeepSeek AI     │ │ SQLite         │ │ InsForge       │
│                │ │ /app/chat_    │ │ (optional)     │
│                │ │   history.db   │ │               │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

---

## 🗂️ FILE STRUCTURE

```
flask_app/
├── app/
│   └── __init__.py           # Flask app factory
├── routes/
│   ├── main.py             # /, /health, /static
│   ├── chat.py            # /chat, /chat/reset, /chat/history
│   ├── upload.py          # /upload, /upload/chat, /upload/reset
│   ├── sync.py          # /sync/status, /sync/upload, /sync/export
│   └── auth.py          # /auth/login, /auth/profile
├── utils/
│   ├── openrouter.py       # AI integration + PROMPTS
│   ├── database.py      # SQLite operations
│   └── sync.py        # Cloud sync functions
├── templates/
│   └── index.html       # Frontend UI
├── data/
│   └── chat_history/   # Downloaded chats
│       ├── latest.json
│       ├── by_date/
│       └── by_month/
├── sync_all.sh           # Complete workflow
├── json_to_sql.py       # JSON to SQL converter
└── chat_data.db      # SQL analytics
```

---

## 🤖 AI PROMPTS

### ANALYST PROMPT
```
You are HealthGuard AI - Health Insurance Policy Analyst.

CRITICAL RULES:
1. TOPIC: Only health insurance India. Anything else: "Sorry, I only help with Indian health insurance."
2. MAX WORDS: 120 words ONLY
3. FORMAT: One short paragraph (2 sentences max). Then 3-4 bullet points with -
4. NEVER USE: ### OR ** OR * OR : OR # IN YOUR RESPONSE
5. END: With one 💡 Tip sentence

WRITE LIKE THIS EXAMPLE:
This policy covers hospital costs but has limits you should know.
- Room rent capped at 1% of sum insured
- Pre-existing disease wait 3 years
- Claim within 30 days of discharge

💡 Tip: Always disclose medical history to avoid claim rejection.

THATS IT. NO FORMATTING. SIMPLE TEXT. COPY THIS STYLE.
```

### SALESMAN PROMPT
```
You are HealthGuard AI - Health Insurance Sales Expert.

CRITICAL RULES:
1. TOPIC: Only health insurance India. Anything else: "Sorry, I only help with Indian health insurance."
2. MAX WORDS: 120 words ONLY
3. FORMAT: One short paragraph (2 sentences max). Then 3-4 bullet points with -
4. NEVER USE: ### OR ** OR * OR : OR # IN YOUR RESPONSE
5. END: With one 💡 Tip sentence

WRITE LIKE THIS EXAMPLE:
HDFC Ergo is good for families. Decent coverage with affordable premium.
- 5L sum insured covers most hospitalizations
- Premium around 25000/year
- 10000+ network hospitals

💡 Tip: Check claim settlement ratio before buying.

THATS IT. NO FORMATTING. SIMPLE TEXT. COPY THIS STYLE.
```

---

## 🗄️ DATABASE SCHEMA

### messages table
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    role TEXT NOT NULL,          -- 'user' or 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    synced INTEGER DEFAULT 0
);
```

### users table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    google_id TEXT UNIQUE,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    gender TEXT,
    age INTEGER,
    salary_range TEXT,
    phone TEXT,
    family_members TEXT,
    family_ages TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### sync_queue table
```sql
CREATE TABLE sync_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    synced INTEGER DEFAULT 0,
    retry_count INTEGER DEFAULT 0
);
```

---

## 🌐 API ENDPOINTS

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/health` | GET | Health check |
| `/chat` | POST | Send message |
| `/chat/history` | GET | Get chat history |
| `/chat/reset` | POST | Reset chat |
| `/upload` | POST | Upload PDF |
| `/upload/chat` | POST | Chat with PDF |
| `/upload/reset` | POST | Reset documents |
| `/auth/login` | POST | Login |
| `/auth/profile` | GET/POST | Profile |
| `/sync/status` | GET | Sync status |
| `/sync/upload` | POST | Upload to cloud |
| `/sync/export` | GET | Export JSON |

---

## ⚙️ ENVIRONMENT VARIABLES

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | Yes | From openrouter.ai |
| `INSFORGE_BASE_URL` | No | Cloud backup |
| `INSFORGE_ANON_KEY` | No | Cloud backup key |
| `GOOGLE_CLIENT_ID` | No | Google OAuth |
| `GOOGLE_CLIENT_SECRET` | No | Google OAuth |
| `SECRET_KEY` | Auto | Flask secret |

---

## 🔄 WORKFLOW SCRIPTS

### Download Chats
```bash
./sync_all.sh
```

Output:
- `data/chat_history/latest.json`
- `data/chat_history/by_date/`
- `data/chat_history/by_month/`
- `chat_data.db` (SQL)

### Query SQL
```bash
sqlite3 chat_data.db "SELECT * FROM chats WHERE date = '2026-04-09'"
```

---

## 📱 FRONTEND FEATURES

- Dark theme with white text
- Video background support
- Login/Profile buttons
- Mode selector (Analyst/Salesman)
- PDF upload
- Quick actions (Compare, Loopholes, Claims, Rights)
- Sync indicator
- Chat messages with user/assistant roles

---

## 🚀 DEPLOYMENT

### Diploi (Current)
1. Connect GitHub repo
2. Add environment variables
3. Auto-deploys on push

### Local Run
```bash
python run.py
# Open http://localhost:5000
```

---

## ✅ COMPLETED FEATURES

- [x] Flask web app
- [x] Dark themed UI
- [x] PDF upload
- [x] AI chat (OpenRouter)
- [x] Dual mode (Analyst/Salesman)
- [x] SQLite database
- [x] User login/profile
- [x] User data storage
- [x] Chat history with user_id
- [x] Offline queue
- [x] JSON export
- [x] SQL converter
- [x] Organized data folders

## 🔜 PENDING

- [ ] Google OAuth
- [ ] InsForge backup
- [ ] Admin panel
- [ ] Analytics dashboard