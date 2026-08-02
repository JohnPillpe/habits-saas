import os

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)


def generate_career_insights(
    career_score: int,
    average_match: int,
    interview_score: int,
    habits: int,
    missing_skills: list,
):

    prompt = f"""
You are an elite Career Coach.

Analyze this candidate.

Career Score:
{career_score}

Average Match:
{average_match}

Interview Score:
{interview_score}

Habits:
{habits}

Missing Skills:
{", ".join(missing_skills)}

Return:

Strengths

Weaknesses

Next recommendation

Keep it under 180 words.
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "You are an expert Career Coach."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return response.choices[0].message.content