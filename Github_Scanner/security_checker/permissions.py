from github import Github
import os
from dotenv import load_dotenv
from security_checker.alerts import send_alert

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def check_repo_permissions(repo_name):
    """Check if the repository is public & inspect collaborators."""
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_name)

    # Check if the repo is public
    if not repo.private:
        print(f"[WARNING] {repo_name} is public! Consider making it private.")
        send_alert("GitHub Security Alert", f"Repository {repo_name} is public!")

    # Check for weak collaborators
    for collab in repo.get_collaborators():
        print(f"[INFO] Collaborator: {collab.login} - Permission: {collab.permissions}")
