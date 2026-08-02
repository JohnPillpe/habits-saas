import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)


def evaluate_interview(role, questions, answers):

    conversation = ""

    for q, a in zip(questions, answers):
        conversation += f"""
Question:
{q}

Answer:
{a}

"""

    prompt = f"""
You are a senior technical interviewer.

Role:
{role}

Interview:

{conversation}

Evaluate the candidate.

Return:

Score: 0-100

Strengths

Weaknesses

Recommendations

Final summary.
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content