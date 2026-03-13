from groq import Groq
import json
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_tasks_llm(transcript):

    prompt = f"""
You are an AI assistant that extracts actionable software tasks from meeting transcripts.

Return ONLY valid JSON in this format:

{{
 "summary": ["point1","point2","point3"],
 "tasks":[
   {{
     "title":"",
     "description":"",
     "priority":"High | Medium | Low",
     "category":"Frontend | Backend | Authentication | DevOps | General",
     "status":"Open"
   }}
 ]
}}

Transcript:
{transcript}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    try:

        data = json.loads(content)

        summary = data.get("summary", [])
        tasks = data.get("tasks", [])

        return summary, tasks

    except Exception as e:

        print("LLM JSON parsing failed:", e)
        print("LLM RAW OUTPUT:", content)

        return ["Failed to generate summary"], []