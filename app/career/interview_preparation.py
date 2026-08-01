from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)


def generar_preparacion_entrevista(cv: str, job: str):

    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": """
You are an expert technical recruiter.

Generate interview preparation in JSON.

Return EXACTLY this format:

{
  "technical_questions": [
    "...",
    "...",
    "..."
  ],
  "behavioral_questions": [
    "...",
    "...",
    "..."
  ],
  "tips": [
    "...",
    "...",
    "..."
  ]
}

Tailor everything to the candidate CV and the Job Description.
Return ONLY valid JSON.
""",
            },
            {
                "role": "user",
                "content": f"""
CV

{cv}

--------------------

JOB DESCRIPTION

{job}
""",
            },
        ],
    )

    print(completion.choices[0].message.content)
    return completion.choices[0].message.content