import re
import random


def extract_tasks(transcript):

    # normalize spaces
    text = transcript.replace("\n", " ").strip()

    # split only on proper sentence endings
    sentences = re.split(r"[.!?]", text)

    summary = []
    tasks = []
    seen = set()

    for sentence in sentences:

        s = sentence.strip()

        if len(s) < 15:
            continue

        # ---- summary (clean short point) ----
        clean = s.capitalize()
        if clean not in summary:
            summary.append(clean)

        # ---- task detection keywords ----
        keywords = [
            "bug", "error", "issue", "fix",
            "implement", "improve", "optimize",
            "redesign", "add", "create"
        ]

        if any(k in s.lower() for k in keywords):

            key = s.lower()
            if key in seen:
                continue

            seen.add(key)

            task = {
                "title": generate_title(s),
                "description": s.capitalize(),
                "priority": detect_priority(s),
                "category": detect_category(s),
                "status": random.choice(["Not Started", "In Progress", "Completed"])
            }

            tasks.append(task)

    return summary[:6], tasks



def generate_title(sentence):

    words = sentence.split()

    # short clear title
    return " ".join(words[:6]).capitalize()



def detect_priority(text):

    t = text.lower()

    if "bug" in t or "error" in t:
        return "High"

    if "implement" in t or "optimize" in t:
        return "Medium"

    return "Low"



def detect_category(text):

    t = text.lower()

    if "login" in t or "auth" in t:
        return "Authentication"

    if "api" in t:
        return "Backend"

    if "dashboard" in t or "ui" in t:
        return "Frontend"

    if "payment" in t:
        return "Payments"

    return "General"