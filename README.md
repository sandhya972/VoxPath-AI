# 🎙️ VoxPath AI – Your Voice-Powered Career Mentor

VoxPath AI is a career guidance application that allows students to interact with a virtual career mentor using voice or text. It provides guidance on programming, internships, projects, resumes, technical interviews, and learning roadmaps.

The application integrates Gnani AI's speech technologies to convert spoken questions into text and generate spoken responses.

## ✨ Features

- 🎤 Voice-based interaction
- 💬 Text-based chat
- 📝 Speech-to-text using Gnani Prisma v3.0
- 🔊 Text-to-speech using Gnani Timbre v2.5
- 🧠 Rule-based career response engine
- 🔄 Conversation context for basic follow-up questions
- 🗑️ Reset conversation functionality
- 🌐 Responsive web interface

## 🛠️ Technology Stack

**Frontend:** HTML, CSS, JavaScript  
**Backend:** Python, Flask  
**Speech Recognition:** Gnani Prisma v3.0  
**Voice Generation:** Gnani Timbre v2.5  
**Audio Processing:** imageio-ffmpeg  
**Environment Management:** python-dotenv

## 📁 Project Structure

```text
Voxpath-AI/
│
├── app.py
├── requirements.txt
├── .gitignore
├── .env
│
├── services/
│   ├── prisma.py
│   ├── timbre.py
│   ├── response_engine.py
│   └── voice_pipeline.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── audio/
│
└── uploads/
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Voxpath-AI
```

### 2. Create a virtual environment

```bash
py -3.13 -m venv .venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
GNANI_API_KEY=your_gnani_api_key
FLASK_SECRET_KEY=your_secret_key
```

Keep your API credentials private. Never upload your `.env` file to GitHub.

### 6. Run the application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## 🔌 Main API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Display the application |
| `/api/health` | GET | Check application status |
| `/api/voice` | POST | Process voice input |
| `/api/chat` | POST | Process typed messages |
| `/api/reset` | POST | Reset conversation |

## 🔄 Application Workflow

**Voice Interaction:**

User Speech → Gnani Prisma STT → VoxPath Response Engine → Gnani Timbre TTS → Spoken Response

**Text Interaction:**

Typed Message → VoxPath Response Engine → Gnani Timbre TTS → Audio Response

## 📌 Current Implementation

The current MVP uses a keyword-based, rule-driven response engine for career guidance. It demonstrates voice integration, text interaction, backend processing, and basic conversation context.

## 🚀 Future Enhancements

- AI-powered conversational reasoning
- Career and skill-gap analysis
- Resume analysis
- Technical interview preparation
- Coding practice
- Conversation history
- Student progress tracking
- Job and internship readiness guidance

## 🙌 Acknowledgements

Built using Gnani AI speech technologies as part of the **Great Indian AI Internship Challenge 2026**.

**Developed by Sandhya Yerragudi**