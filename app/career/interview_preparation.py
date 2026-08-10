from openai import OpenAI
import os
import json

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)


def generar_preparacion_entrevista(cv: str, job: str):

    completion = client.chat.completions.create(
        model="deepseek-chat",
        response_format={
            "type": "json_object"
        },
        max_tokens=4000,
        messages=[
            {
                "role": "system",
                "content": """
You are an expert technical recruiter.

Generate interview preparation as valid JSON.

The response MUST be a JSON object with EXACTLY these keys:

{
  "technical_questions": [
    "...",
    "...",
    "...",
    "..."
  ],
  "behavioral_questions": [
    "...",
    "...",
    "...",
    "..."
  ],
  "tips": [
    "...",
    "...",
    "...",
    "..."
  ]
}

Rules:

- Return ONLY valid JSON.
- Do not use markdown.
- Do not use ```json.
- Do not add explanations outside the JSON.
- All values must be valid JSON strings.
- Tailor the questions and tips to both the candidate CV and the job description.
- The word JSON must be respected literally.
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

--------------------

Return the interview preparation as valid JSON.
""",
            },
        ],
    )

    content = completion.choices[0].message.content

    print("========== INTERVIEW PREPARATION ==========")
    print(content)
    print("===========================================")

    # Validación inmediata.
    # Si DeepSeek devuelve algo inválido, fallamos aquí
    # y no después al intentar guardarlo en DB.
    json.loads(content)

    return content