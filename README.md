# Job Skills Analyzer Agent

An AI-powered tool that helps you learn the skills employers actually want for ANY job title. Analyzes real job postings, identifies skill gaps based on your resume, and generates personalized daily challenges to make you job-ready.

## Features

- **Universal Job Analysis**: Works for ANY job title (Data Engineer, Product Manager, UX Designer, etc.)
- **Resume-Based Personalization**: Analyzes your resume to identify skill gaps
- **Real Job Data**: Fetches actual job postings from the market
- **Daily Challenges**: Generates hands-on practice exercises
- **Progress Tracking**: Monitors your learning journey

## Quick Start

### 1. Install Dependencies

```bash
pip install requests
```

### 2. Get API Keys

**Groq API (Required - No Credit Card)**
1. Visit https://console.groq.com
2. Sign up for free
3. Create an API key
4. Copy the key (starts with `gsk_`)

**JSearch API (Optional - For Real Jobs)**
1. Visit https://rapidapi.com/jsearch
2. Sign up for RapidAPI
3. Subscribe to BASIC (free) plan
4. Copy your API key

### 3. Set Environment Variables

**Mac/Linux:**
```bash
export GROQ_API_KEY='your-groq-key-here'
export RAPID_API_KEY='your-rapidapi-key-here'  # Optional
```

**Windows Command Prompt:**
```cmd
set GROQ_API_KEY=your-groq-key-here
set RAPID_API_KEY=your-rapidapi-key-here
```

**Windows PowerShell:**
```powershell
$env:GROQ_API_KEY='your-groq-key-here'
$env:RAPID_API_KEY='your-rapidapi-key-here'
```

### 4. Run First Time Setup

```bash
python job_skills_agent.py
```

The agent will ask you:
1. What job title you're targeting
2. Your preferred location
3. Whether you want to add your resume (optional but recommended)

## How It Works

### First Run: Interactive Setup

```
WELCOME TO JOB SKILLS ANALYZER
======================================================================

First-time setup - Let's configure your preferences

What job title are you targeting?
Examples: Data Engineer, Software Developer, Product Manager,
          Marketing Manager, UX Designer, etc.

Enter job title: Product Manager

What location are you interested in?
Examples: United States, New York, Remote, San Francisco, etc.

Enter location: San Francisco

Do you want to add your resume now? (y/n): y
```

### Adding Your Resume

You have two options:

**Option 1: Paste directly**
```
Paste your resume below (press Ctrl+D when done):
----------------------------------------------------------------------
[Your resume text here]
```

**Option 2: Import from file**
```
Enter path to resume file: /path/to/resume.txt
```

### Daily Usage

After setup, just run:
```bash
python job_skills_agent.py
```

The agent will:
1. Fetch recent job postings for your target role
2. Analyze required skills
3. Compare against your resume (if provided)
4. Show skill gaps
5. Generate a personalized daily challenge

## Example Output

```
======================================================================
PRODUCT MANAGER SKILLS MARKET REPORT
======================================================================

Current market shows strong demand for product managers with technical
background and data analysis skills.

YOUR SKILL GAP ANALYSIS:
Based on your resume, you have strong communication and stakeholder 
management skills. Focus on developing SQL, data analysis, and A/B 
testing expertise to match market demands.

TOP 10 IN-DEMAND SKILLS:

#    Skill                     Category              Jobs    Priority    Status
-----------------------------------------------------------------------------------
1    SQL                       Technical Skill       5/5      High        Learn
     -> Essential for data-driven decision making

2    A/B Testing               Technical Skill       4/5      High        Learn
     -> Required for feature experimentation

3    Stakeholder Management    Soft Skill            5/5      High        Have
     -> Critical for cross-functional collaboration
...

======================================================================
YOUR DAILY CHALLENGE
======================================================================

Challenge: Build a Simple Product Metrics Dashboard

What You'll Build:
Create a basic SQL-based dashboard that tracks key product metrics...
[Detailed instructions follow]
```

## File Structure

After running the agent, your directory will look like this:

```
job-skills-agent/
├── job_skills_agent.py       # Main script
├── config.json               # Your preferences (auto-generated)
├── data/
│   ├── resume.txt            # Your resume (if added)
│   ├── progress.json         # Learning progress
│   └── current_skills.json   # Latest skills analysis
└── README.md                 # This file
```

## Configuration File (config.json)

```json
{
  "job_title": "Product Manager",
  "location": "San Francisco",
  "resume_path": "data/resume.txt",
  "setup_date": "2026-01-29",
  "last_run": "2026-01-29"
}
```

## Updating Your Configuration

### Change Job Title or Location
Simply delete `config.json` and run the agent again. It will re-run the setup.

### Update Your Resume
Edit `data/resume.txt` directly with any text editor.

### View Your Progress
```bash
cat data/progress.json
```

## Daily Workflow

1. **Morning**: Run the agent
2. **Review**: Check the skills report and your personalized challenge
3. **Complete**: Do the challenge (30-60 minutes)
4. **Document**: Save your solution to GitHub
5. **Track**: Mark challenge as complete in progress.json

## Use Cases

### Data Engineer
- Analyzes data engineering job requirements
- Identifies technical skills like Python, SQL, Spark, Airflow
- Generates ETL/data pipeline challenges

### Product Manager
- Finds PM roles in your target location
- Identifies skills like SQL, analytics, roadmapping
- Creates challenges around PRDs, metrics, user research

### UX Designer
- Searches for UX/UI designer positions
- Highlights tools like Figma, user testing, prototyping
- Generates design challenges and portfolio projects

### Software Developer
- Fetches developer jobs by specialty
- Analyzes required languages and frameworks
- Creates coding challenges and project ideas

### Marketing Manager
- Finds marketing leadership roles
- Identifies analytics, SEO, campaign management skills
- Generates marketing strategy exercises

## Advanced Features

### Skill Gap Analysis

When you provide your resume, the agent:
- Compares your experience against market requirements
- Identifies which skills you already have
- Highlights skills you need to develop
- Prioritizes learning based on demand

### Personalized Challenges

Challenges are customized based on:
- Your target job title
- Skills you're missing (from resume analysis)
- Current market demand
- Your learning progress

## Tips for Best Results

1. **Be Specific with Job Titles**: Use exact titles like "Senior Data Engineer" instead of just "Engineer"

2. **Keep Resume Updated**: Update `data/resume.txt` as you learn new skills

3. **Run Daily**: Consistency matters - make it part of your morning routine

4. **Complete Challenges**: Actually do the work, don't just read them

5. **Document Everything**: Save solutions to GitHub to build your portfolio

6. **Track Progress**: Manually update `completed_challenges` in progress.json

## Troubleshooting

**"GROQ_API_KEY not set"**
- Export the environment variable in your current terminal session
- Add it to your `.bashrc` or `.zshrc` for persistence

**"No jobs found"**
- Check your internet connection
- Verify your job title is spelled correctly
- The agent will use sample data as fallback

**"Request timed out"**
- Normal for slow connections
- Agent automatically uses sample data
- Try again with better internet

**Resume not being analyzed**
- Make sure `data/resume.txt` exists and has content
- Check `config.json` has "resume_path" set
- Re-run setup to add resume if missing

## Privacy & Data

- All data stays local on your machine
- Resume is only sent to Groq API for analysis
- No data is shared with third parties
- You can delete all data anytime by removing the `data/` folder

## Limitations

- Requires API keys (both are free tier)
- JSearch API: 100 requests/month (plenty for daily use)
- Sample data used when API unavailable
- Generic challenges for less common job titles

## Future Enhancements

- Email/Slack notifications for daily challenges
- Web dashboard for progress visualization
- Integration with LinkedIn for automatic resume import
- Company-specific skill analysis
- Salary insights based on skill levels
- Collaborative challenges for group learning

## Contributing

This is an open-source learning tool. Feel free to:
- Fork and customize for your needs
- Add support for more job boards
- Improve challenge generation
- Submit pull requests

## Support

For issues or questions:
1. Check this README
2. Review the code comments
3. Check existing issues on GitHub
4. Open a new issue with details

## License

MIT License - Use freely for personal or educational purposes

## Acknowledgments

Built to help job seekers focus their learning on skills that actually matter in the current job market. Instead of random tutorials, learn what employers are actually hiring for today.

---

**Ready to start?** Just run:
```bash
python job_skills_agent.py
```

Your journey to landing your dream job begins now.
