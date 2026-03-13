import requests


def create_github_issue(repo, token, task):

    url = f"https://api.github.com/repos/{repo}/issues"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    body = f"""
Priority: {task.get("priority")}

Category: {task.get("category")}

Status: {task.get("status")}

Description:
{task.get("description")}
"""

    data = {
        "title": task.get("title"),
        "body": body
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:

        issue = response.json()

        return {
            "url": issue["html_url"]
        }

    else:

        print("GitHub API ERROR:", response.text)

        return {
            "url": None
        }