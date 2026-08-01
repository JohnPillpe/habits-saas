from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)


def generar_cover_letter(cv: str, job: str):

    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": """
You are an expert career coach.

Write a highly personalized cover letter.

Rules:

- Professional.
- Natural.
- ATS friendly.
- Do not invent experience.
- Use only information from the CV.
- Tailor everything to the Job Description.

Return ONLY the cover letter in Markdown.
""",
            },
            {
                "role": "user",
                "content": f"""
CV

{cv}

---------------------

JOB DESCRIPTION

{job}
""",
            },
        ],
    )

    return completion.choices[0].message.content