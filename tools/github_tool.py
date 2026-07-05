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
   
def check_ci_failures(limit: int = 5) -> dict:
    try:
        token = os.getenv("GITHUB_TOKEN")
        v1 = Github(token)
        repo = v1.get_repo(os.getenv('GITHUB_REPO'))
        runs = repo.get_workflow_runs(status="failure")
        failures = []
        count = 0
        for run in runs:
            if count >= limit:
                break
            failures.append({
                "workflow_name": run.name,
                "run_number": run.run_number,
                "conclusion": run.conclusion,
                "html_url": run.html_url,
                "created_at": run.created_at.isoformat()
            })
            count += 1
        return {"success": True, "failures": failures}
    except Exception as e:
        return {"success": False, "message": str(e)}
