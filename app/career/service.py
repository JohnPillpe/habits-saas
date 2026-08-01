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