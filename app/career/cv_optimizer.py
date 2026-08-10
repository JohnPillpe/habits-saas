from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)


def optimizar_cv(cv: str, job: str):

    completion = client.chat.completions.create(
        model="deepseek-chat",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": """
You are a world-class Resume Writer.

Your job is to rewrite the candidate's CV so it is highly optimized for ONE specific job description.

Rules:

- Never invent experience.
- Never invent companies.
- Never invent achievements.
- Reorder information.
- Rewrite bullets.
- Prioritize the most relevant experience.
- Improve ATS compatibility.
- Keep everything truthful.

Return ONLY the optimized CV in Markdown.
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