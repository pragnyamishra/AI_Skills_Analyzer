# Job Skills Analyzer

An AI-powered CLI that helps you learn the skills employers actually want for any job title. You set your target role and location (and optionally add your resume); the tool fetches real job postings, analyzes in-demand skills with Groq AI, compares them to your resume, and generates a personalized daily challenge. AData and config are stored locally in `./data/`.

---

## What it does

- **Universal job analysis** — Works for any role (Data Engineer, QA Engineer, Product Manager, UX Designer, etc.).
- **Real job data** — Fetches live postings from the market (JSearch API) or uses sample data when the API is unavailable.
- **Skills report** — Extracts the top in-demand skills from postings, with category, job count, priority, and a short description.
- **Resume-based personalization** — If you add a resume (txt, docx, or pdf), it identifies which skills you already have vs. which to learn and shows **Have** / **Learn** per skill. Optional skill-gap summary is included.
- **Daily challenges** — Generates one hands-on challenge per run, focused on high-priority or missing skills.
- **Progress** — Tracks how many challenges you’ve received; progress is shown in one line at the end of each run.
- **Configuration** — Interactive setup for job title, location, and resume. You can update these anytime by running again and choosing to update configuration.

---

## How it works

1. **First run** — You run `python job_skills_agent.py`. The script asks for your target job title, location, and whether you want to add a resume (paste text or provide a path to a .txt, .docx, or .pdf file). It saves this in `config.json` and creates the `data/` folder.
2. **Job fetch** — It fetches recent job postings for your role and location (or uses built-in sample postings if the API key is missing or the request fails).
3. **Skills analysis** — Job descriptions are sent to the Groq API. The model returns a structured list of top skills, categories, importance, and—if a resume was provided—which skills you have vs. need to develop.
4. **Report** — A skills market report is printed: summary, optional skill-gap analysis, and a table of top skills with Status (Have/Learn when resume is used).
5. **Challenge** — The same API is used to generate one daily challenge (title, what to build, skills practiced), tailored to high-priority or missing skills when a resume is present.
6. **Data** — Config, resume (if any), progress, and the latest skills JSON are stored under `./data/`. You can re-run anytime; you’re prompted to update configuration so you can change job title, location, or resume without deleting files.

---

## Features

| Feature | Description |
|--------|-------------|
| **Any job title** | Data Engineer, Software Developer, Product Manager, QA Engineer, UX Designer, Marketing Manager, etc. |
| **Resume support** | .txt, .docx, or .pdf. Place a file with "resume" in the name in `data/`, or add it during setup (paste or file path). |
| **Skill gap** | When a resume is provided, the report shows which skills you have vs. need to learn and can include a short skill-gap summary. |
| **Daily challenge** | One challenge per run; focuses on skills you need when resume is used, otherwise on high-priority skills. |
| **Update config** | On each run you can choose to update job title, location, or resume without deleting `config.json`. |
| **Local-first** | All data stays in your project (`config.json`, `data/`). Only job text and resume (if added) are sent to Groq for analysis. |

---

## Requirements

- **Python 3** with `requests`, `python-docx`, `pypdf` (see `requirements.txt`).
- **Groq API key** (required) — Used for skills analysis and challenge generation.
- **RAPID_API_KEY** (optional) — For live job postings via JSearch; if unset or failing, sample postings are used.

---

## Quick start

```bash
pip install -r requirements.txt
export GROQ_API_KEY='your-groq-key'
python job_skills_agent.py
```

Follow the prompts to set your target role, location, and optional resume. Re-run daily for new challenges; say **y** when asked to update configuration to change role, location, or resume.
