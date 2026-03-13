from groq import Groq
import json
import os

# Load Groq client from environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_tasks_llm(transcript):

    prompt = f"""
You are an AI assistant that extracts actionable software engineering tasks from meeting transcripts.

Return ONLY valid JSON with no extra text.

JSON format:

{{
 "summary": ["point1","point2","point3"],
 "tasks":[
   {{
     "title":"short task title",
     "description":"clear explanation of the issue or task",
     "priority":"High | Medium | Low",
     "category":"Frontend | Backend | Authentication | DevOps | General",
     "status":"Open"
   }}
 ]
}}

Rules:
- Summary must be 3–6 short bullet points
- Extract only actionable engineering issues
- Tasks must be concise and realistic
- Always return valid JSON

Transcript:
{transcript}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        # Remove accidental markdown if model returns ```json
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        data = json.loads(content)

        summary = data.get("summary", [])
        tasks = data.get("tasks", [])

        return summary, tasks

    except Exception as e:

        print("LLM JSON parsing failed:", e)
        print("LLM RAW OUTPUT:", content)

        # fallback to avoid frontend crash
        return ["Unable to generate summary from meeting"], []