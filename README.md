# 🏥 HealthGuard AI - Insurance Policy Analyzer

An intelligent AI-powered health insurance policy analyzer with dual modes (Analyst & Salesman) for the Indian market.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-2.2.5-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### Dual Mode System
- **Analyst Mode** 🔍 - Professional policy analysis, comparison, finding loopholes
- **Salesman Mode** 🤝 - Persuasive sales, customer handling, closing deals

### Core Capabilities
- 📄 **PDF Upload** - Upload and analyze policy documents
- 📊 **Policy Comparison** - Compare different health insurance policies
- 🔍 **Loophole Detection** - Find hidden exclusions and clauses
- 💰 **Premium Analysis** - Value assessment and recommendations
- 📝 **Claim Tips** - Guidance for smooth claim settlement
- 🇮🇳 **India-Focused** - Tailored for Indian insurance market

### UI Features
- 🌑 **Dark Theme** - Modern dark UI with white/bright text
- 🎬 **Video Background** - Animated background support
- 📱 **Responsive** - Works on desktop and mobile
- 🎨 **Professional Design** - Glass-morphism effects

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- OpenRouter API Key

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/divakar2121/flask_insurance_bot.git
cd flask_insurance_bot
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables:**
```bash
# Create .env file
echo "OPENROUTER_API_KEY=your_api_key_here" > .env
```

5. **Get your OpenRouter API key:**
   - Visit [OpenRouter.ai](https://openrouter.ai)
   - Create account and get free API key
   - Add to `.env` file

6. **Run the application:**
```bash
python run.py
```

7. **Open in browser:**
```
http://localhost:5000
```

## 🎯 Usage

### Mode Selection
- Click **Analyst** for detailed policy analysis
- Click **Salesman** for sales-oriented conversations

### Upload PDF
1. Click "Upload Policy Document" to select a PDF
2. Select from dropdown to switch between documents
3. Ask questions about the uploaded policy

### Quick Actions
- **Compare** - Compare two policies
- **Loopholes** - Find hidden exclusions
- **Claim Tips** - Get claim guidance
- **Your Rights** - Understand policyholder rights

## 📁 Project Structure

```
flask_insurance_bot/
├── app/
│   └── __init__.py          # Flask app factory
├── routes/
│   ├── main.py              # Main routes (home, health)
│   ├── chat.py              # Chat endpoints
│   └── upload.py            # PDF upload & document chat
├── utils/
│   ├── openrouter.py         # LLM integration
│   └── database.py          # SQLite database
├── templates/
│   └── index.html            # Frontend UI
├── static/
│   └── background.mp4       # Video background
├── .env                     # Environment variables (not in git)
├── requirements.txt          # Python dependencies
└── run.py                   # Application entry point
```

## 🔧 Configuration

### Environment Variables
| Variable | Description |
|----------|-------------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key |

### Changing Models
Edit `utils/openrouter.py` to change the AI model:
```python
def chat(messages, model="deepseek/deepseek-chat-v3"):
```

## 🌐 Deployment

### Deploy to Diploi
1. Push code to GitHub
2. Connect repository in Diploi dashboard
3. Add `OPENROUTER_API_KEY` in Environment settings
4. Deploy

### Deploy to Render/Railway/Vercel
1. Push to GitHub
2. Connect to your preferred platform
3. Add `OPENROUTER_API_KEY` environment variable
4. Deploy

## 🤖 AI Models

- **Default:** DeepSeek Chat V3 (free tier)
- **Alternative:** Google Gemma 3 (free tier)

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/health` | GET | Health check |
| `/upload` | POST | Upload PDF |
| `/upload/chat` | POST | Chat with mode |
| `/upload/reset` | POST | Reset documents |

## 🔐 Security

- API key stored in `.env` file (not committed to git)
- Use environment variables in production
- Never hardcode API keys in source code

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Divakar Singh

## 🙏 Acknowledgments

- [OpenRouter](https://openrouter.ai) - AI API provider
- [Flask](https://flask.palletsprojects.com) - Web framework
- [Tailwind CSS](https://tailwindcss.com) - CSS framework