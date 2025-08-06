# 🖱️ Mini-Cursor

**Mini-Cursor** is a Python-based command-line assistant powered by Gemini (Google Generative AI).  
It works in a smart **Step-by-Step planning mode** — where it plans, picks tools, performs actions, and gives you useful results.

Linkedin Profile : https://www.linkedin.com/in/sadiq-ameen-657b90278/

Perfect for:
- Running system commands
- Performing small tasks with tools like `run_command`, `get_weather`
- Building AI-powered CLI workflows using LLMs

---

## ⚙️ Tech Stack
- Python
- Google Gemini API (via OpenAI-compatible endpoint)
- dotenv
- Langsmith (optional tracing)
- Tools integration (`run_command`, etc.)

---

## 📦 Installation Guide

### 1. **Clone the Repository**
```bash
git clone https://github.com/Mohd-Sadiq-Ameen/Mini-Cursor.git
```

---

### 2. **Create Virtual Environment (optional)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. **Install Dependencies
```bash
pip install -r requirements.txt
```
If there's no requirements.txt, install manually:

```bash
pip install openai python-dotenv requests
```

### 4. **Setup Environment Variables
   Create a .env file in the root folder:
env
```bash
GEMINI_API_KEY=your_google_gemini_api_key_here
```


### 5. ** Run the Assistant

```bash
python index.py
```
You’ll see a prompt like this:

```bash
> 

