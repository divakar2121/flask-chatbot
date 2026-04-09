# 🏥 HealthGuard AI - Insurance Policy Analyzer

An intelligent AI-powered health insurance policy analyzer with dual modes (Analyst & Salesman) for the Indian market.

## 🌟 Features

### 🤖 AI Capabilities
- **Policy Analysis** - Detailed breakdown of health insurance policies
- **Loophole Detection** - Find hidden exclusions and clauses  
- **Policy Comparison** - Compare different policies objectively
- **Claim Guidance** - Tips for smooth claim settlement

### 📊 Dual Mode System
- **Analyst Mode** 🔍 - Professional, analytical, thorough
- **Salesman Mode** 🤝 - Persuasive, customer-focused, sales-oriented

### 🔐 User Authentication
- Email-based login
- User profiles with: name, gender, age, salary range, phone, family details
- Chats linked to user_id for personalization

### 💾 Data Management
- **Local SQLite** - Server database at `/app/chat_history.db`
- **Offline Queue** - Messages queued when offline
- **Cloud Sync** - Optional InsForge backup
- **JSON Export** - Organized by date/month

### 📁 Organized Data Storage
```
data/chat_history/
├── latest.json      # All messages
├── by_date/        # Grouped by day
└── by_month/     # Grouped by month
```

### 🔧 SQL Analysis
- Convert JSON to SQL database for analysis
- Query with: `sqlite3 chat_data.db`

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- OpenRouter API Key

### Run Locally
```bash
python run.py
# Open http://localhost:5000
```

### Deploy to Production
```bash
./sync_all.sh
```
This downloads chats and creates SQL database.

## 📁 Project Structure

```
flask_app/
├── app/
│   └── __init__.py          # Flask app factory
├── routes/
│   ├── main.py            # Home, health endpoints
│   ├── chat.py           # Chat API  
│   ├── upload.py         # PDF upload
│   ├── sync.py          # Sync endpoints
│   └── auth.py         # Login/profile
├── utils/
│   ├── openrouter.py     # AI integration
│   ├── database.py      # SQLite operations
│   └── sync.py         # Cloud sync
├── templates/
│   └── index.html       # Frontend UI
├── data/
│   └── chat_history/  # Exported chats
├── sync_all.sh          # Complete workflow
├── sync_chats.sh       # Download chats
├── json_to_sql.py     # Convert to SQL
└── chat_data.db      # SQL analytics DB
```

## 🌐 Deployment

### Diploi (Current)
- **URL:** https://my-dev--flsk-chtbt-th8v.diploi.me
- **Repo:** https://github.com/divakar2121/flask-chatbot
- Auto-deploys on push to master

## 🖥️ Local Workflow

### Download Chats from Server
```bash
./sync_all.sh
```

This:
1. Downloads from Diploi server
2. Saves to `data/chat_history/`
3. Converts to `chat_data.db`

### Query Data
```bash
sqlite3 chat_data.db "SELECT * FROM chats WHERE date = '2026-04-09'"
```

## 🔐 Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENROUTER_API_KEY` | AI API key (from openrouter.ai) |
| `INSFORGE_BASE_URL` | Cloud backup URL |
| `INSFORGE_ANON_KEY` | Cloud backup key |
| `GOOGLE_CLIENT_ID` | Google OAuth |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret |

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/health` | GET | Health check |
| `/upload` | POST | Upload PDF |
| `/upload/chat` | POST | Chat with mode |
| `/auth/login` | POST | Login |
| `/auth/profile` | GET/POST | User profile |
| `/chat/history` | GET | All messages |
| `/sync/status` | GET | Sync status |
| `/sync/export` | GET | Export JSON |

## 🏗️ Architecture

```
User → Frontend (index.html)
     → Flask API (routes/)
     → OpenRouter AI (utils/openrouter.py)
     → SQLite (utils/database.py)
          → messages table (with user_id)
          → users table (profile data)
          → sync_queue table (offline)
     → Optional: InsForge Cloud
```

## 📊 Database Schema

### messages table
```sql
id, user_id, role, content, created_at, synced
```

### users table  
```sql
id, google_id, email, name, gender, age, 
salary_range, phone, family_members, family_ages, created_at
```

## 🎯 Usage Tips

1. **Login first** - Click Login button to save your profile
2. **Fill profile** - Gender, age, salary help personalize responses
3. **Upload PDF** - Analyze specific policies
4. **Use Analyst** - For detailed analysis
5. **Run sync** - Keep local backup updated

## ✅ What's Implemented

- [x] Flask web app with dark theme
- [x] PDF upload and analysis
- [x] Dual mode (Analyst/Salesman)
- [x] OpenRouter AI integration
- [x] SQLite database
- [x] User login/profile system
- [x] Chat history with user_id
- [x] Offline sync queue
- [x] JSON to SQL converter
- [x] Organized data folders
- [x] Complete workflow script

## 🔜 Future Enhancements

- [ ] Google OAuth
- [ ] InsForge cloud backup
- [ ] Admin panel
- [ ] Analytics dashboard
- [ ] Chat export to CSV

## 👨‍💻 Author

Divakar Ravi

## 🙏 Thanks

- [OpenRouter.ai](https://openrouter.ai) - Free AI API
- [Flask](https://flask.palletsprojects.com) - Web framework  
- [Tailwind CSS](https://tailwindcss.com) - CSS framework
- [Diploi](https://diploi.com) - Hosting