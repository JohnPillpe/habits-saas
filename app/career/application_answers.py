from openai import OpenAI
import os
import json

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

You MUST return ONLY valid JSON.

Do not use markdown.
Do not use ```json.
Do not add explanations before or after the JSON.

Return EXACTLY this structure:

{
  "tell_me_about_yourself": "...",
  "why_this_company": "...",
  "why_should_we_hire_you": "...",
  "greatest_strength": "...",
  "greatest_weakness": "..."
}

Rules:
- Use only information supported by the CV.
- Do not invent experience, skills, companies, tools, achievements or education.
- Tailor every answer to the specific job description.
- Each value must be a string.
""",
            },
            {
                "role": "user",
                "content": f"""
CV:

{cv}

----------------

JOB DESCRIPTION:

{job}
""",
            },
        ],
    )

    response = completion.choices[0].message.content.strip()

    print("\n========== APPLICATION ANSWERS ==========")
    print(response)
    print("=========================================\n")

    try:
        parsed = json.loads(response)
    except json.JSONDecodeError as e:
        print("INVALID APPLICATION ANSWERS RESPONSE:")
        print(response)

        raise ValueError(
            "DeepSeek returned invalid JSON for application answers."
        ) from e

    required_keys = [
        "tell_me_about_yourself",
        "why_this_company",
        "why_should_we_hire_you",
        "greatest_strength",
        "greatest_weakness",
    ]

    for key in required_keys:
        if key not in parsed:
            raise ValueError(
                f"Application answers missing required field: {key}"
            )

    return response