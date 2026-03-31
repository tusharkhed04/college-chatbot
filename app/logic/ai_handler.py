import os
from flask import current_app


def get_ai_response(user_message, context, db_response):
    api_key = current_app.config.get("OPENAI_API_KEY", "")
    if not api_key:
        return None

    try:
        import openai
        openai.api_key = api_key

        system_prompt = (
            "You are a helpful college assistant chatbot. "
            "You help students with timetables, syllabus, faculty info, and exam schedules. "
            "Use the following data fetched from the database to answer the student's query. "
            "Be concise, friendly, and helpful. Format responses clearly.\n\n"
            f"Database Result:\n{db_response}\n\n"
            f"Context: Branch={context.get('branch', 'CSE')}, Year={context.get('year', 3)}"
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=400,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None
