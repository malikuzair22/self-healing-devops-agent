from dotenv import load_dotenv
load_dotenv()
from github import Github
import os
def  create_issue(diagnosis: str, confidence: float, logs: str) -> dict:
    try:
        token = os.getenv("GITHUB_TOKEN")
        v1 = Github(token)
        repo = v1.get_repo(os.getenv('GITHUB_REPO'))
        title = f"Incident: {diagnosis} (Confidence: {confidence})"
        body = f"Logs:\n```\n{logs}\n```"
        issue = repo.create_issue(title=title, body=body)
        return {"success": True, "issue_url": issue.html_url, "message": "Issue created"}
    except Exception as e:
        return {"success": False, "message": str(e)}
   

