#!/usr/bin/env python3
"""
Job Skills Analyzer Agent
Analyzes job market data for ANY job title and generates personalized daily challenges
"""

import json
import os
import shutil
import sys
from datetime import datetime

import requests

# Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
CONFIG_FILE = "config.json"
PROGRESS_FILE = "data/progress.json"
SKILLS_FILE = "data/current_skills.json"
DATA_DIR = "data"
RESUME_EXTENSIONS = (".txt", ".docx", ".pdf")
# Default path when saving resume from setup (pasted or imported)
DEFAULT_RESUME_SAVE = os.path.join(DATA_DIR, "resume.txt")


def load_config():
    """Load user configuration"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None


def setup_configuration(is_update=False):
    """Interactive setup for first-time users or configuration update"""
    print("\n" + "=" * 70)
    print("WELCOME TO JOB SKILLS ANALYZER" if not is_update else "UPDATE CONFIGURATION")
    print("=" * 70)
    print("\nUpdate your preferences\n" if is_update else "\nFirst-time setup - Let's configure your preferences\n")
    
    # Get job title
    print("What job title are you targeting?")
    print("Examples: Data Engineer, Software Developer, Product Manager,")
    print("          Marketing Manager, UX Designer, etc.\n")
    job_title = input("Enter job title: ").strip()
    
    if not job_title:
        print("ERROR: Job title cannot be empty")
        sys.exit(1)
    
    # Get location preference
    print("\nWhat location are you interested in?")
    print("Examples: United States, New York, Remote, San Francisco, etc.\n")
    location = input("Enter location (or press Enter for 'United States'): ").strip()
    if not location:
        location = "United States"
    
    # Ask about resume
    print("\n" + "=" * 70)
    print("RESUME SETUP (Optional but Recommended)")
    print("=" * 70)
    print("\nAdding your resume helps the agent:")
    print("- Identify your skill gaps")
    print("- Generate personalized challenges")
    print("- Focus on areas where you need improvement\n")
    
    has_resume = input("Do you want to add your resume now? (y/n): ").lower().strip()
    
    resume_path = None
    if has_resume == 'y':
        print("\nYou can either:")
        print("1. Paste your resume text directly")
        print("2. Provide a path to a text file\n")
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == '1':
            print("\nPaste your resume below (press Ctrl+D on Mac/Linux or Ctrl+Z on Windows when done):")
            print("-" * 70)
            try:
                resume_lines = []
                while True:
                    try:
                        line = input()
                        resume_lines.append(line)
                    except EOFError:
                        break
                resume_text = "\n".join(resume_lines)
                
                # Save resume
                os.makedirs(DATA_DIR, exist_ok=True)
                with open(DEFAULT_RESUME_SAVE, 'w', encoding='utf-8') as f:
                    f.write(resume_text)
                resume_path = DEFAULT_RESUME_SAVE
                print("\nResume saved successfully!")
            except Exception as e:
                print(f"\nWARNING: Could not save resume: {e}")
        
        elif choice == '2':
            file_path = input("Enter path to resume file (.txt, .docx, or .pdf): ").strip()
            if os.path.exists(file_path):
                try:
                    ext = os.path.splitext(file_path)[1].lower()
                    if ext == ".txt":
                        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                            resume_text = f.read()
                        os.makedirs(DATA_DIR, exist_ok=True)
                        with open(DEFAULT_RESUME_SAVE, 'w', encoding='utf-8') as f:
                            f.write(resume_text)
                        resume_path = DEFAULT_RESUME_SAVE
                    elif ext in (".docx", ".pdf"):
                        os.makedirs(DATA_DIR, exist_ok=True)
                        dest = os.path.join(DATA_DIR, "resume" + ext)
                        src_abs = os.path.abspath(file_path)
                        dest_abs = os.path.abspath(dest)
                        if os.path.normpath(src_abs) == os.path.normpath(dest_abs) or (
                            os.path.exists(dest_abs) and os.path.samefile(src_abs, dest_abs)
                        ):
                            # File is already in data/ with resume name; no copy needed
                            resume_path = dest
                            print("Resume already in place.")
                        else:
                            shutil.copy2(file_path, dest)
                            resume_path = dest
                            print("Resume imported successfully!")
                    else:
                        print("WARNING: Use .txt, .docx, or .pdf. Skipping.")
                        resume_path = None
                    if resume_path and ext == ".txt":
                        print("Resume imported successfully!")
                except Exception as e:
                    print(f"WARNING: Could not read resume file: {e}")
                    resume_path = None
            else:
                print("WARNING: File not found. Skipping resume setup.")
    
    # Save configuration
    config = {
        "job_title": job_title,
        "location": location,
        "resume_path": resume_path,
        "setup_date": datetime.now().strftime("%Y-%m-%d"),
        "last_run": None
    }
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n" + "=" * 70)
    print("SETUP COMPLETE!")
    print("=" * 70)
    print(f"\nTarget Job: {job_title}")
    print(f"Location: {location}")
    print(f"Resume: {'Added' if resume_path else 'Not added (you can add it later)'}")
    print("\nYou can change these settings anytime by editing config.json")
    print("or deleting it and running setup again.\n")
    
    return config


def fetch_job_listings(config):
    """
    Fetch jobs based on user's target job title
    """
    
    rapid_api_key = os.environ.get("RAPID_API_KEY", "")
    job_title = config['job_title']
    location = config['location']
    
    if not rapid_api_key:
        print("INFO: No RAPID_API_KEY found - using sample data")
        print("To use real jobs: Get key at rapidapi.com/jsearch\n")
        return get_sample_jobs(job_title)
    
    print(f"Fetching {job_title} jobs in {location}...")
    
    try:
        url = "https://jsearch.p.rapidapi.com/search"
        querystring = {
            "query": f"{job_title} in {location}",
            "page": "1",
            "num_pages": "1",
            "date_posted": "week"
        }
        
        headers = {
            "X-RapidAPI-Key": rapid_api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            jobs = []
            
            for job in data.get('data', [])[:5]:
                jobs.append({
                    'title': job.get('job_title', 'Unknown'),
                    'company': job.get('employer_name', 'Unknown'),
                    'description': job.get('job_description', '')[:1500]
                })
            
            print(f"SUCCESS: Found {len(jobs)} {job_title} jobs\n")
            return jobs
        else:
            print(f"WARNING: API returned status {response.status_code}, using sample data\n")
            return get_sample_jobs(job_title)
            
    except requests.exceptions.Timeout:
        print("WARNING: Request timed out, using sample data\n")
        return get_sample_jobs(job_title)
    except Exception as e:
        print(f"WARNING: Error fetching jobs: {e}")
        print("Using sample data instead\n")
        return get_sample_jobs(job_title)


def get_sample_jobs(job_title):
    """Generate sample job data based on job title"""
    
    # Generic sample jobs that work for any title
    return [
        {
            "title": f"Senior {job_title}",
            "company": "Tech Company",
            "description": f"""
            We're seeking a Senior {job_title} to join our growing team.
            
            This role involves working on challenging projects, collaborating with 
            cross-functional teams, and delivering high-quality results.
            
            Required Skills:
            - Strong communication and collaboration skills
            - Problem-solving and analytical thinking
            - Experience with relevant tools and technologies
            - Ability to work in a fast-paced environment
            - Bachelor's degree or equivalent experience
            """
        },
        {
            "title": f"{job_title}",
            "company": "Innovative Startup",
            "description": f"""
            Join our dynamic team as a {job_title}.
            
            You'll be responsible for key initiatives that drive our business forward.
            
            Requirements:
            - 3-5 years of relevant experience
            - Strong technical or domain expertise
            - Excellent written and verbal communication
            - Self-motivated and able to work independently
            - Passion for innovation and continuous learning
            """
        },
        {
            "title": f"{job_title} (Mid-Level)",
            "company": "Enterprise Corp",
            "description": f"""
            We're looking for a motivated {job_title} to support our operations.
            
            This is a great opportunity to grow your career at an established company.
            
            Must Have:
            - Relevant education or certifications
            - Professional experience in the field
            - Strong attention to detail
            - Team player with good interpersonal skills
            - Willingness to learn and adapt
            """
        }
    ]


def find_resume_file():
    """Find first file in data/ whose name contains 'resume' and has extension .txt, .docx, or .pdf."""
    if not os.path.isdir(DATA_DIR):
        return None
    # Skip temp/lock files (e.g. Word ~$resume.docx)
    def is_resume_file(name):
        if name.startswith("~") or name.startswith(".$"):
            return False
        return "resume" in name.lower()
    # Prefer .txt, then .docx, then .pdf
    by_ext = {ext: [] for ext in RESUME_EXTENSIONS}
    for name in os.listdir(DATA_DIR):
        if not is_resume_file(name):
            continue
        path = os.path.join(DATA_DIR, name)
        if not os.path.isfile(path):
            continue
        ext = os.path.splitext(name)[1].lower()
        if ext in RESUME_EXTENSIONS:
            by_ext[ext].append(path)
    for ext in RESUME_EXTENSIONS:
        if by_ext[ext]:
            return by_ext[ext][0]
    return None


def load_resume():
    """Load resume text from data/ (any file with 'resume' in name, .txt / .docx / .pdf)."""
    path = find_resume_file()
    if not path:
        return None
    ext = os.path.splitext(path)[1].lower()
    if ext == ".txt":
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
        except OSError:
            return None
    if ext == ".docx":
        try:
            import docx
            doc = docx.Document(path)
            return "\n".join(p.text for p in doc.paragraphs)
        except ImportError:
            print("Resume is .docx. Use .txt/.pdf or: pip install python-docx")
            return None
        except Exception:
            return None
    if ext == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(path)
            return "\n".join(
                p.extract_text() or ""
                for p in reader.pages
            ).strip()
        except ImportError:
            print("Resume is .pdf. Use .txt/.docx or: pip install pypdf")
            return None
        except Exception:
            return None
    return None


def analyze_skills_with_groq(job_listings, config):
    """
    Use Groq API to analyze skills
    """
    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY not set!\n")
        print("Get your API key:")
        print("1. Go to: https://console.groq.com")
        print("2. Sign up")
        print("3. Go to 'API Keys' and create one")
        print("4. Set it: export GROQ_API_KEY='your-key-here'\n")
        return None
    
    print("Analyzing skills with Groq AI...\n")
    
    # Prepare job descriptions
    jobs_text = "\n\n---\n\n".join([
        f"Job {i+1}: {job['title']} at {job['company']}\n{job['description']}"
        for i, job in enumerate(job_listings)
    ])
    
    # Load resume if available
    resume_text = load_resume()
    resume_context = ""
    if resume_text:
        resume_context = f"\n\nUser's Current Resume/Background:\n{resume_text[:2000]}\n"
    
    resume_instruction = (
        "5. For EACH skill, set \"user_has\": true if the user's resume clearly shows they have this skill, "
        "otherwise \"user_has\": false. You MUST include user_has for every skill."
    ) if resume_text else ""
    json_user_line = '\n            "user_has": true or false,' if resume_text else ""
    json_skill_gap = ',\n    "skill_gap_summary": "Brief analysis of user\'s skill gaps based on resume"' if resume_text else ""
    prompt = f"""Analyze these {config['job_title']} job postings and extract the required skills.

{jobs_text}
{resume_context}

Provide a JSON response with:
1. Top 10 most frequently mentioned technical skills/tools/competencies
2. Categorize each appropriately (Technical Skill, Soft Skill, Tool, Certification, etc.)
3. Count how many jobs mention each skill
4. Rate importance (High/Medium/Low) based on frequency
{resume_instruction}

JSON format:
{{
    "top_skills": [
        {{
            "skill": "Example Skill",
            "category": "Category",
            "job_count": 3,
            "importance": "High",
            "description": "Why this skill matters"{json_user_line}
        }}
    ],
    "summary": "Brief market trends summary"{json_skill_gap}
}}

Return ONLY valid JSON, no markdown or extra text."""
    
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are a career advisor specializing in {config['job_title']} roles. Always respond with valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 2500
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            response_text = result['choices'][0]['message']['content']
            
            # Clean response - extract JSON
            response_text = response_text.strip()
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            
            skills_data = json.loads(response_text)
            
            # Save to file
            os.makedirs("data", exist_ok=True)
            with open(SKILLS_FILE, 'w') as f:
                json.dump(skills_data, f, indent=2)
            
            return skills_data
        else:
            print(f"ERROR: API Error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return None
            
    except json.JSONDecodeError as e:
        print(f"ERROR: Error parsing JSON response: {e}")
        print(f"Response was: {response_text[:200]}...")
        return None
    except Exception as e:
        print(f"ERROR: Error analyzing skills: {e}")
        return None


def display_skills_report(skills_data, config, num_jobs=None):
    """Display the skills analysis in a structured report format"""
    job_count_str = f"{num_jobs} recent job postings" if num_jobs else "recent job postings"
    
    print("\n" + "─" * 70)
    print("📊 SKILLS MARKET REPORT – " + config["job_title"])
    print("─" * 70)
    print(f"Analysis based on {job_count_str}.")
    print(f"\n{skills_data.get('summary', 'Market analysis complete.')}\n")
    
    if "skill_gap_summary" in skills_data:
        print("YOUR SKILL GAP ANALYSIS:")
        print(skills_data["skill_gap_summary"])
        print()
    
    print("Top In-Demand Skills:\n")
    # Table with borders: # | Skill | Category | Priority | Status
    col_w = {"#": 3, "Skill": 22, "Category": 18, "Priority": 8, "Status": 10}
    sep = "+" + "-" * (col_w["#"] + 2) + "+" + "-" * (col_w["Skill"] + 2) + "+" + "-" * (col_w["Category"] + 2) + "+" + "-" * (col_w["Priority"] + 2) + "+" + "-" * (col_w["Status"] + 2) + "+"
    
    w = [col_w["#"], col_w["Skill"], col_w["Category"], col_w["Priority"], col_w["Status"]]
    def row(*cells):
        return "| " + " | ".join(str(c).ljust(w[i])[:w[i]] for i, c in enumerate(cells)) + " |"
    
    print(sep)
    print(row("#", "Skill", "Category", "Priority", "Status"))
    print(sep)
    
    for i, skill in enumerate(skills_data.get("top_skills", [])[:10], 1):
        importance = (skill.get("importance") or "Medium").upper()[:col_w["Priority"]]
        user_has = skill.get("user_has", None)
        if user_has is not None:
            if isinstance(user_has, str):
                user_has = user_has.strip().lower() in ("true", "yes", "1")
            status = "✓ Have" if user_has else "✗ Learn"
        else:
            status = ""
        skill_name = (skill.get("skill") or "")[:col_w["Skill"]]
        category = (skill.get("category") or "")[:col_w["Category"]]
        print(row(str(i), skill_name, category, importance, status))
    
    print(sep)
    # Descriptions below table
    for i, skill in enumerate(skills_data.get("top_skills", [])[:10], 1):
        desc = skill.get("description", "Important skill")
        if desc:
            print(f"  {i}. {skill.get('skill', '')}: {desc}")
    print()


def generate_daily_challenge(skills_data, config):
    """Generate a daily challenge using Groq AI"""
    if not GROQ_API_KEY:
        return None
    
    # Focus on skills the user needs to learn
    resume_text = load_resume()
    if resume_text:
        skills_to_focus = [s for s in skills_data.get('top_skills', []) if not s.get('user_has', True)]
        if not skills_to_focus:
            skills_to_focus = [s for s in skills_data.get('top_skills', []) if s.get('importance') == 'High'][:3]
    else:
        skills_to_focus = [s for s in skills_data.get('top_skills', []) if s.get('importance') == 'High'][:3]
    
    if not skills_to_focus:
        skills_to_focus = skills_data.get('top_skills', [])[:3]
    
    skills_list = ", ".join([s['skill'] for s in skills_to_focus[:3]])
    progress = load_progress()
    challenge_num = progress['total_challenges'] + 1
    
    prompt = f"""You're a career mentor for {config['job_title']} professionals. Create ONE practical challenge.

Focus on these skills: {skills_list}

Requirements:
- Completable in 30-60 minutes
- Hands-on and practical
- Portfolio-worthy for {config['job_title']} role
- Uses accessible tools

Respond in this exact format (use these section headers):

Title: [One short challenge title]

What to do:
1. [First step]
2. [Second step]
3. [Third step]
4. [Fourth step - add more if needed]

Skills practiced: [comma-separated list of skills]

Keep it simple and actionable. No extra intro or outro."""
    
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are a practical career mentor for {config['job_title']} who creates beginner-friendly challenges. Always use the exact section headers: Title:, What to do:, Skills practiced:"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1500
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            challenge = result['choices'][0]['message']['content'].strip()
            
            # Structured Daily Challenge output
            print("\n" + "─" * 70)
            print("Daily Challenge")
            print("─" * 70)
            print(f"\n🎯 TODAY'S CHALLENGE (#{challenge_num})\n")
            print(challenge)
            print("\n" + "─" * 70)
            print(f"Skills practiced: {skills_list}")
            completed = progress.get("completed_challenges", 0)
            print(f"Progress: {completed} challenges completed")
            print("─" * 70)
            
            # Save challenge
            today = datetime.now().strftime("%Y-%m-%d")
            challenge_data = {
                "date": today,
                "challenge": challenge,
                "skills_focused": skills_list,
                "job_title": config['job_title']
            }
            
            progress['challenges'].append(challenge_data)
            progress['total_challenges'] += 1
            save_progress(progress)
            
            # Update last run date
            config['last_run'] = today
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
            
            return challenge
        else:
            print(f"ERROR: Error generating challenge: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"ERROR: Error generating challenge: {e}")
        return None


def load_progress():
    """Load user progress"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {
            "started_date": datetime.now().strftime("%Y-%m-%d"),
            "total_challenges": 0,
            "completed_challenges": 0,
            "challenges": [],
            "skills_learned": []
        }


def save_progress(progress):
    """Save user progress"""
    os.makedirs("data", exist_ok=True)
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def show_progress(config):
    """Display learning progress (minimal one-line summary)"""
    progress = load_progress()
    total = progress['total_challenges']
    done = progress['completed_challenges']
    if total > 0:
        print(f"\nProgress: {done}/{total} challenges completed.")
    else:
        print(f"\nProgress: {total} challenge(s) ready in ./data/")


def main():
    """Main function"""
    print("\n" + "=" * 70)
    print("JOB SKILLS ANALYZER AGENT")
    print("Learn What Employers Actually Want")
    print("=" * 70 + "\n")
    
    # Load or create configuration
    config = load_config()
    if not config:
        config = setup_configuration()
    else:
        print(f"Configuration loaded:")
        print(f"Target Role: {config['job_title']}")
        print(f"Location: {config['location']}")
        resume_found = find_resume_file()
        print(f"Resume: {'Added (' + resume_found + ')' if resume_found else 'Not added'}\n")
        update = input("Update configuration? (y/n) [n]: ").strip().lower()
        if update == "y" or update == "yes":
            config = setup_configuration(is_update=True)
            print()

    # Step 1: Fetch jobs
    jobs = fetch_job_listings(config)
    
    if not jobs:
        print("ERROR: No jobs found.")
        return
    
    # Step 2: Analyze with Groq
    skills_data = analyze_skills_with_groq(jobs, config)
    
    if not skills_data:
        print("ERROR: Could not analyze skills. Please check your GROQ_API_KEY.")
        return
    
    # Step 3: Display report
    display_skills_report(skills_data, config, num_jobs=len(jobs))
    
    # Step 4: Generate challenge
    generate_daily_challenge(skills_data, config)
    
    show_progress(config)
    print()


if __name__ == "__main__":
    main()
