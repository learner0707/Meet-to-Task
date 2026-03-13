import requests


def create_github_issue(repo, token, task):

    url = f"https://api.github.com/repos/{repo}/issues"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "title": task["title"],
        "body": f"""
Description: {task['description']}

Priority: {task['priority']}
Category: {task['category']}
Status: {task['status']}
"""
    }

    try:

        response = requests.post(url, json=data, headers=headers)

        issue = response.json()

        if "html_url" in issue:
            return {
                "issue_title": issue["title"],
                "issue_url": issue["html_url"]
            }

        else:
            return {
                "issue_title": task["title"],
                "issue_url": "#"
            }

    except Exception as e:

        return {
            "issue_title": task["title"],
            "issue_url": "#"
        }