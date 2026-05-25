import os
import json
import pdfplumber
from docx import Document
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file from backend folder
load_dotenv(r"C:\resume_analyzer\backend\.env")


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY not found. Check C:\\resume_analyzer\\backend\\.env file"
        )

    return OpenAI(api_key=api_key)


def extract_text_from_resume(file_path):
    text = ""

    if file_path.lower().endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    elif file_path.lower().endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text


def ai_resume_score(resume_text):
    prompt = f"""
You are an expert resume analyzer.

Analyze this resume and give score out of 100 based on:
1. Skills - 25 marks
2. Projects - 25 marks
3. Experience - 20 marks
4. Education - 10 marks
5. Resume structure and clarity - 20 marks

Return ONLY valid JSON. No markdown. No explanation.

JSON format:
{{
  "overall_score": 75,
  "skills_score": 20,
  "projects_score": 18,
  "experience_score": 15,
  "education_score": 8,
  "structure_score": 14,
  "strengths": ["Good technical skills", "Projects are mentioned"],
  "improvements": ["Add measurable achievements", "Add GitHub/project links"]
}}

Resume text:
{resume_text}
"""

    try:
        client = get_openai_client()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional ATS resume analyzer. Return only valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        result = response.choices[0].message.content.strip()

        # Safety cleanup if AI returns ```json
        result = result.replace("```json", "").replace("```", "").strip()

        return json.loads(result)
    except Exception as exc:
        print("OpenAI API unavailable or invalid key. Using fallback resume analyzer.", exc)
        return ai_resume_score_fallback(resume_text)


def ai_resume_score_fallback(resume_text):
    text = resume_text.lower()
    skills_keywords = [
        "python", "java", "javascript", "react", "node", "typescript",
        "sql", "django", "flask", "aws", "azure", "docker", "kubernetes",
        "machine learning", "ml", "data analysis", "tensorflow", "pandas"
    ]

    skills_count = sum(1 for keyword in skills_keywords if keyword in text)
    skills_score = min(25, skills_count * 2)

    projects_score = 25 if "project" in text or "github" in text or "portfolio" in text else 12
    experience_score = 20 if "year" in text or "years" in text or "experience" in text else 10
    education_score = 10 if any(term in text for term in ["bachelor", "master", "phd", "degree"]) else 5
    structure_score = 20 if len(text.split()) > 300 else 12

    overall_score = skills_score + projects_score + experience_score + education_score + structure_score
    overall_score = min(100, overall_score)

    strengths = []
    improvements = []

    if skills_count >= 3:
        strengths.append("Resume contains multiple strong technical keywords.")
    else:
        improvements.append("Add more technical skills and technologies used.")

    if projects_score == 25:
        strengths.append("Projects are described in the resume.")
    else:
        improvements.append("Include project details, links, or outcomes.")

    if experience_score == 20:
        strengths.append("Experience section is present.")
    else:
        improvements.append("Add work experience with clear duration and impact.")

    if education_score == 10:
        strengths.append("Education details are included.")
    else:
        improvements.append("Add education credentials or certifications.")

    if structure_score == 20:
        strengths.append("Resume length and structure are appropriate.")
    else:
        improvements.append("Expand the resume text with more details and structure.")

    return {
        "overall_score": overall_score,
        "skills_score": skills_score,
        "projects_score": projects_score,
        "experience_score": experience_score,
        "education_score": education_score,
        "structure_score": structure_score,
        "strengths": strengths,
        "improvements": improvements,
        "fallback_used": True
    }


def get_job_recommendations(resume_text, score):
    prompt = f"""
You are an expert career advisor and job matching specialist.

Based on the following resume text and its overall score ({score}/100), suggest 5 relevant job positions that this candidate can apply to.

Return ONLY valid JSON with no extra explanation.

JSON format:
{{
  "jobs": [
    {{
      "title": "Job Title",
      "company": "Company Name",
      "description": "Short job description explaining why this role fits the candidate.",
      "required_skills": ["Skill 1", "Skill 2", "Skill 3"],
      "match_percentage": 85
    }}
  ]
}}

Resume text:
{resume_text[:2000]}
"""

    client = get_openai_client()
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a career advisor who matches candidates with ideal jobs."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        result = response.choices[0].message.content.strip()
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    except Exception as exc:
        print("OpenAI API unavailable or invalid key. Using fallback job recommendations.", exc)
        return get_job_recommendations_fallback(resume_text, score)


def get_job_recommendations_fallback(resume_text, score):
    text = resume_text.lower()
    categories = []

    if any(word in text for word in ["machine learning", "data science", "data analysis", "tensorflow", "pandas"]):
        categories.append("Data Scientist")
    if any(word in text for word in ["react", "angular", "vue", "javascript", "typescript"]):
        categories.append("Frontend Developer")
    if any(word in text for word in ["django", "flask", "python", "node", "express"]):
        categories.append("Backend Developer")
    if any(word in text for word in ["aws", "azure", "docker", "kubernetes", "cloud"]):
        categories.append("Cloud Engineer")
    if any(word in text for word in ["marketing", "seo", "content", "sales"]):
        categories.append("Marketing Specialist")

    if not categories:
        categories = ["Software Engineer", "Data Analyst", "IT Support Engineer", "Technical Writer", "Product Analyst"]

    jobs = []
    base_skills = {
        "Data Scientist": ["Python", "Machine Learning", "Data Analysis", "SQL"],
        "Frontend Developer": ["JavaScript", "React", "HTML", "CSS"],
        "Backend Developer": ["Python", "Django", "REST APIs", "SQL"],
        "Cloud Engineer": ["AWS", "Docker", "Kubernetes", "Linux"],
        "Marketing Specialist": ["SEO", "Content Creation", "Analytics", "Social Media"],
        "Software Engineer": ["Python", "Java", "Git", "Problem Solving"],
        "Data Analyst": ["Excel", "SQL", "Tableau", "Data Visualization"],
        "IT Support Engineer": ["Troubleshooting", "Windows", "Networking", "Customer Service"],
        "Technical Writer": ["Technical Writing", "Documentation", "Communication", "Word"],
        "Product Analyst": ["Product Management", "User Research", "Data Analysis", "Roadmaps"]
    }

    for idx, category in enumerate(categories[:5]):
        jobs.append({
            "title": f"{category}",
            "company": f"Top {category} Company",
            "description": f"A great role for candidates with experience in {category.lower()} and strong relevant skills.",
            "required_skills": base_skills.get(category, ["Communication", "Teamwork"]),
            "match_percentage": max(60, min(95, score))
        })

    return {"jobs": jobs, "fallback_used": True}


def ai_resume_score_all_fields(resume_text):
    """
    Analyze resume and provide scores for ALL career fields.
    """
    prompt = f"""
You are an expert resume analyzer specializing in multiple career fields.

Analyze this resume and provide a score out of 100 for EACH of these career fields:
1. IT/Software Development
2. Data Science & Analytics
3. Business & Management
4. Sales & Business Development
5. Marketing & Communications
6. Finance & Accounting
7. Human Resources
8. Project Management
9. Design & UX
10. Consulting

For each field, evaluate based on:
- Relevant Skills (25%)
- Relevant Projects/Experience (25%)
- Work Experience (20%)
- Education (15%)
- Overall Resume Quality (15%)

Return ONLY valid JSON. No markdown. No explanation.

JSON format:
{{
  "field_scores": {{
    "IT/Software Development": {{
      "score": 85,
      "strengths": ["Python", "React", "SQL"],
      "gaps": ["Cloud platforms"]
    }},
    "Data Science & Analytics": {{
      "score": 72,
      "strengths": ["SQL", "Data analysis"],
      "gaps": ["Machine Learning"]
    }},
    "Business & Management": {{
      "score": 55,
      "strengths": ["Experience"],
      "gaps": ["Leadership examples"]
    }},
    "Sales & Business Development": {{
      "score": 48,
      "strengths": [],
      "gaps": ["Sales metrics", "Client management"]
    }},
    "Marketing & Communications": {{
      "score": 50,
      "strengths": ["Writing skills"],
      "gaps": ["Marketing tools", "Campaign examples"]
    }},
    "Finance & Accounting": {{
      "score": 42,
      "strengths": [],
      "gaps": ["Financial knowledge", "Accounting software"]
    }},
    "Human Resources": {{
      "score": 58,
      "strengths": ["Communication"],
      "gaps": ["HR specific tools"]
    }},
    "Project Management": {{
      "score": 65,
      "strengths": ["Experience"],
      "gaps": ["PM certifications"]
    }},
    "Design & UX": {{
      "score": 35,
      "strengths": [],
      "gaps": ["Design tools", "Portfolio"]
    }},
    "Consulting": {{
      "score": 62,
      "strengths": ["Problem solving"],
      "gaps": ["Consulting background"]
    }}
  }},
  "best_fit_fields": ["IT/Software Development", "Data Science & Analytics", "Project Management"],
  "overall_versatility_score": 75
}}

Resume text:
{resume_text}
"""

    try:
        client = get_openai_client()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional resume analyzer with expertise in multiple career fields. Return only valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        result = response.choices[0].message.content.strip()
        result = result.replace("```json", "").replace("```", "").strip()

        return json.loads(result)
    except Exception as exc:
        print("OpenAI API unavailable or invalid key. Using fallback multi-field analyzer.", exc)
        return ai_resume_score_all_fields_fallback(resume_text)


def ai_resume_score_all_fields_fallback(resume_text):
    """
    Fallback function to score resume across all career fields.
    """
    text = resume_text.lower()

    # Define keywords for each field
    field_keywords = {
        "IT/Software Development": {
            "keywords": ["python", "java", "javascript", "react", "node", "sql", "git", "api", "developer", "software", "code", "programming"],
            "boost": 15
        },
        "Data Science & Analytics": {
            "keywords": ["python", "sql", "data", "analysis", "analytics", "tableau", "power bi", "machine learning", "ml", "statistics", "pandas"],
            "boost": 10
        },
        "Business & Management": {
            "keywords": ["management", "manager", "business", "strategic", "operations", "leadership", "lead", "team"],
            "boost": 8
        },
        "Sales & Business Development": {
            "keywords": ["sales", "business development", "crm", "salesforce", "revenue", "client", "account", "pipeline"],
            "boost": 7
        },
        "Marketing & Communications": {
            "keywords": ["marketing", "content", "seo", "social media", "brand", "campaign", "communication", "copywriting"],
            "boost": 7
        },
        "Finance & Accounting": {
            "keywords": ["finance", "accounting", "financial", "cpa", "audit", "budgeting", "excel", "quickbooks", "sap"],
            "boost": 8
        },
        "Human Resources": {
            "keywords": ["hr", "human resources", "recruitment", "talent", "onboarding", "employee", "benefits", "hris"],
            "boost": 7
        },
        "Project Management": {
            "keywords": ["project management", "pm", "agile", "scrum", "jira", "pmp", "waterfall", "stakeholder"],
            "boost": 8
        },
        "Design & UX": {
            "keywords": ["design", "ux", "ui", "figma", "photoshop", "adobe", "prototype", "wireframe", "css"],
            "boost": 8
        },
        "Consulting": {
            "keywords": ["consulting", "consultant", "strategy", "advisory", "client", "problem solving", "business case"],
            "boost": 7
        }
    }

    # Base score components
    has_experience = any(word in text for word in ["year", "years", "experience"])
    has_education = any(term in text for term in ["bachelor", "master", "phd", "degree"])
    has_projects = any(word in text for word in ["project", "github", "portfolio"])

    experience_score = 20 if has_experience else 10
    education_score = 15 if has_education else 5
    projects_score = 15 if has_projects else 5
    quality_score = 15 if len(text.split()) > 300 else 8

    field_scores = {}
    best_fit_fields = []

    for field, data in field_keywords.items():
        # Count keyword matches
        keyword_count = sum(1 for keyword in data["keywords"] if keyword in text)
        skills_score = min(25, keyword_count * 3)

        # Calculate total score
        total_score = skills_score + projects_score + experience_score + education_score + quality_score
        total_score = min(100, total_score)

        # Boost score for best matches
        if keyword_count >= 3:
            total_score = min(100, total_score + data["boost"])
            best_fit_fields.append(field)

        strengths = []
        gaps = []

        if keyword_count >= 2:
            strengths.append(f"Strong {field.lower()} fundamentals")
        if has_experience:
            strengths.append("Professional experience")
        if has_projects:
            strengths.append("Project portfolio")

        if keyword_count < 2:
            gaps.append(f"Limited {field.lower()} specific skills")
        if not has_projects:
            gaps.append("No projects mentioned")
        if not has_education:
            gaps.append("No formal education listed")

        field_scores[field] = {
            "score": total_score,
            "strengths": strengths[:2],
            "gaps": gaps[:2]
        }

    # Sort and get best fit fields
    sorted_fields = sorted(field_scores.items(), key=lambda x: x[1]["score"], reverse=True)
    best_fit_fields = [field for field, _ in sorted_fields[:3]]

    # Calculate versatility score
    avg_score = sum(score["score"] for score in field_scores.values()) / len(field_scores)
    versatility_score = int(avg_score)

    return {
        "field_scores": {field: score for field, score in field_scores.items()},
        "best_fit_fields": best_fit_fields,
        "overall_versatility_score": versatility_score,
        "fallback_used": True
    }