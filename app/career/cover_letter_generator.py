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
You are an expert Resume Writer, ATS specialist and Career Coach.

Write a professional Cover Letter tailored to ONE job description.

Rules:

- Use ONLY information present in the CV.
- NEVER invent:
  - experience
  - companies
  - projects
  - technologies
  - certifications
  - achievements
  - dates
- Do not exaggerate skills.
- Focus on the experience most relevant to the job.
- Professional, concise and natural tone.
- 250–350 words.
- Avoid generic phrases.
- Do not use placeholders.
- Return ONLY the Cover Letter in Markdown.
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