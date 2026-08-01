from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)


def generar_respuestas(cv: str, job: str):

    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": """
You are an expert career coach.

Generate excellent answers for common job application questions.

Return JSON with exactly this format:

{
    "tell_me_about_yourself": "...",
    "why_this_company": "...",
    "why_should_we_hire_you": "...",
    "greatest_strength": "...",
    "greatest_weakness": "..."
}

Do not invent experience.
Use only information from the CV.
Tailor every answer to the Job Description.
""",
            },
            {
                "role": "user",
                "content": f"""
CV

{cv}

----------------

JOB DESCRIPTION

{job}
""",
            },
        ],
    )

    return completion.choices[0].message.content