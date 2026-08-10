import os
import json
from openai import OpenAI

from app.career.prompts import SYSTEM_PROMPT

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)

def analizar_cv_vs_job(cv: str, job: str):

    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"""
CANDIDATE CV

{cv}

-------------------------

JOB DESCRIPTION

{job}
""",
            },
        ],
        response_format={"type": "json_object"},
    )

    contenido = completion.choices[0].message.content

    print(contenido)

    return json.loads(contenido)


def analizar_job(job: str):

    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": """
You are an expert technical recruiter.

Analyze the job description.

Return ONLY valid JSON:

{
    "match_score": 0,
    "recommendation": "",
    "summary": "",
    "why": [],
    "strengths": [],
    "missing_skills": [],
    "next_steps": [],
    "required_skills": [],
    "soft_skills": [],
    "seniority": "",
    "difficulty": ""
}

Rules:

- recommendation must be one of:
  "Strong Match"
  "Good Match"
  "Possible Match"
  "Weak Match"

- why must contain 3 concise reasons.

- next_steps must contain practical actions the candidate should take before applying.

- match_score must realistically reflect the job requirements.

""",
            },
            {
                "role": "user",
                "content": job,
            },
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(
        completion.choices[0].message.content
    )