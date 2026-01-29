# 🎯 AI Job Skills Analyzer

> **An intelligent CLI tool that analyzes real job market data to identify in-demand skills and generate personalized learning challenges**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Groq](https://img.shields.io/badge/Powered%20by-Groq%20AI-orange.svg)](https://groq.com/)

---

## 📋 Overview

Job descriptions can be overwhelming and vague. This tool cuts through the noise by:
- ✅ Fetching **real job postings** from the market
- ✅ Using **AI to extract** the most in-demand skills
- ✅ **Comparing** those skills to your resume (optional)
- ✅ Generating **daily hands-on challenges** to help you learn what matters

Perfect for anyone navigating career transitions, upskilling, or job hunting in competitive markets.

---

## 🎬 Demo

```bash
$ python job_skills_agent.py

╔══════════════════════════════════════════════════════════╗
║         AI JOB SKILLS ANALYZER                          ║
╚══════════════════════════════════════════════════════════╝

Enter your target job title: Data Engineer
Enter your location: Dallas, TX
Do you want to add a resume? (y/n): y

✓ Fetching job postings...
✓ Analyzing skills with AI...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SKILLS MARKET REPORT - Data Engineer in Dallas, TX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Top 10 In-Demand Skills:
┌────┬─────────────────┬──────────────┬──────────┬──────────┬────────────────────┐
│ #  │ Skill           │ Category     │ Priority │ Status   │ Description        │
├────┼─────────────────┼──────────────┼──────────┼──────────┼────────────────────┤
│ 1  │ Apache Spark    │ Big Data     │ HIGH     │ ✓ Have   │ Distributed...     │
│ 2  │ Python          │ Programming  │ HIGH     │ ✓ Have   │ Primary lang...    │
│ 3  │ DBT             │ Data Tools   │ HIGH     │ ✗ Learn  │ Data transform...  │
...
```

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| **🌍 Universal Job Analysis** | Works for any role: Data Engineer, Product Manager, UX Designer, QA Engineer, etc. |
| **📈 Real Market Data** | Fetches live job postings via JSearch API (falls back to sample data if unavailable) |
| **🤖 AI-Powered Extraction** | Uses Groq's LLM to intelligently parse job descriptions and identify key skills |
| **📄 Resume Integration** | Upload your resume (.txt, .docx, .pdf) to get personalized "Have vs Learn" analysis |
| **🎯 Daily Challenges** | Generates practical, hands-on tasks focused on your skill gaps |
| **💾 Local-First Privacy** | All data stored locally; only job text sent to AI for analysis |
| **🔄 Easy Updates** | Modify job title, location, or resume anytime without losing progress |

---

## 🛠️ Technical Stack

- **Language:** Python 3.8+
- **AI Model:** Groq API (LLaMA 3.1 70B)
- **Job Data:** JSearch API (RapidAPI)
- **Document Parsing:** `python-docx`, `pypdf`
- **Data Storage:** Local JSON files

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key ([Get one free](https://console.groq.com/))
- (Optional) RapidAPI key for JSearch ([Get here](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch))

### Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-skills-analyzer.git
cd ai-skills-analyzer

# Install dependencies
pip install -r requirements.txt

# Set up API keys
export GROQ_API_KEY='your-groq-api-key'
export RAPID_API_KEY='your-rapid-api-key'  # Optional

# Run the tool
python job_skills_agent.py
```

---

## 💡 How It Works

### 1️⃣ **Configuration**
On first run, you'll be prompted to enter:
- Target job title (e.g., "Machine Learning Engineer")
- Location (e.g., "San Francisco, CA")
- (Optional) Resume file or pasted text

All settings saved to `./data/config.json` and can be updated anytime.

### 2️⃣ **Job Fetching**
The tool fetches recent job postings matching your criteria:
- **Live mode:** Uses JSearch API for real-time data
- **Fallback mode:** Uses curated sample postings if API unavailable

### 3️⃣ **AI Analysis**
Job descriptions are sent to Groq's LLM, which:
- Extracts the most frequently mentioned skills
- Categorizes them (e.g., Programming, Cloud, Tools)
- Assigns priority levels (HIGH/MEDIUM/LOW)
- If resume provided: Marks each skill as "Have" or "Learn"

### 4️⃣ **Report Generation**
You receive:
- **Skills Summary:** Top 10-15 in-demand skills with metadata
- **Skill Gap Analysis:** (If resume provided) What you know vs. need to learn
- **Daily Challenge:** One actionable task to practice a high-priority skill

### 5️⃣ **Progress Tracking**
The tool tracks:
- Number of challenges completed
- Skills you've worked on
- Your learning journey over time

---

## 📊 Sample Output

### Skills Report
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SKILLS MARKET REPORT - Machine Learning Engineer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Analysis based on 15 recent job postings

Top In-Demand Skills:
┌────┬─────────────────┬──────────────┬──────────┬──────────┐
│ #  │ Skill           │ Category     │ Priority │ Status   │
├────┼─────────────────┼──────────────┼──────────┼──────────┤
│ 1  │ PyTorch         │ ML Framework │ HIGH     │ ✓ Have   │
│ 2  │ MLOps           │ Engineering  │ HIGH     │ ✗ Learn  │
│ 3  │ Kubernetes      │ Cloud/DevOps │ HIGH     │ ✗ Learn  │
│ 4  │ Python          │ Programming  │ HIGH     │ ✓ Have   │
│ 5  │ AWS SageMaker   │ Cloud        │ MEDIUM   │ ✗ Learn  │
└────┴─────────────────┴──────────────┴──────────┴──────────┘
```

### Daily Challenge
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 TODAY'S CHALLENGE (#3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Title: Build a Simple MLOps Pipeline

What to do:
Create a basic ML model deployment pipeline using Docker and GitHub Actions:
1. Train a simple scikit-learn model on a dataset
2. Containerize it using Docker
3. Set up automated testing with pytest
4. Create a CI/CD pipeline that retrains on new data

Skills practiced: MLOps, Docker, CI/CD, Python

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Progress: 3 challenges completed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📁 Project Structure

```
ai-skills-analyzer/
├── job_skills_agent.py      # Main CLI application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── LICENSE                   # MIT License
└── data/                     # Auto-generated on first run
    ├── config.json           # User configuration
    ├── resume.txt            # Your resume (if provided)
    ├── progress.json         # Challenge tracking
    └── latest_skills.json    # Most recent analysis
```

---

## 🎓 Use Cases

### 1. **Career Changers**
Identify the exact skills needed to transition into a new role (e.g., from Software Engineer → ML Engineer)

### 2. **Job Seekers**
Tailor your resume and interview prep based on what employers actually want

### 3. **Students & Bootcamp Grads**
Bridge the gap between academic learning and industry requirements

### 4. **Upskilling Professionals**
Stay current with evolving tech stacks in your field

---

## 🔒 Privacy & Data

- ✅ All data stored **locally** in `./data/` folder
- ✅ Only job descriptions and (optionally) your resume are sent to Groq API for analysis
- ✅ No user data is collected, stored, or shared by this tool
- ✅ You can delete `./data/` anytime to reset

---

## 🤝 Contributing

Contributions are welcome! Here are some ideas:

- [ ] Add support for more job search APIs (LinkedIn, Indeed)
- [ ] Create a web UI (Streamlit/Gradio)
- [ ] Export reports to PDF
- [ ] Track learning progress over time with visualizations
- [ ] Multi-language support

Feel free to open an issue or submit a PR!

---

## 🙏 Acknowledgments

- **Groq** for providing fast, reliable LLM inference
- **JSearch API** for job market data
- Inspired by the frustration of vague job descriptions and the need for actionable upskilling guidance

---

## 📬 Contact

**Pragnya Lipsa Mishra**
- 💼 LinkedIn: [linkedin.com/in/pragnya-lipsa-mishra](https://www.linkedin.com/in/pragnya-lipsa-mishra/)
- 🐙 GitHub: [github.com/pragnyamishra](https://github.com/pragnyamishra)

---

## 🌟 Star this repo if you find it helpful!

*Built with ❤️ to help people navigate their career journeys with data-driven insights*
