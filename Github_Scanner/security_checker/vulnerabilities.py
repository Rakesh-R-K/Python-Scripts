import os
import re
import requests
from security_checker.alerts import send_alert
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def check_vulnerabilities(package_name):
    """Check if a package has known vulnerabilities."""
    url = f"https://api.github.com/advisories?query={package_name}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers).json()

    if response:
        print(f"[WARNING] {package_name} has known vulnerabilities!")
        send_alert("GitHub Security Alert", f"Vulnerable package detected: {package_name}")
    else:
        print(f"[SAFE] {package_name} is secure.")

def scan_dependencies(repo_path):
    """Scan package.json (for MERN stack) and requirements.txt (for Python projects)."""
    package_json_path = os.path.join(repo_path, "package.json")
    requirements_txt_path = os.path.join(repo_path, "requirements.txt")

    if os.path.exists(package_json_path):
        print("[INFO] Scanning package.json for vulnerable dependencies...")
        with open(package_json_path, "r", encoding="utf-8") as f:
            for line in f:
                match = re.search(r'"(.+)":\s*".+"', line)
                if match:
                    check_vulnerabilities(match.group(1))

    if os.path.exists(requirements_txt_path):
        print("[INFO] Scanning requirements.txt for vulnerabilities...")
        with open(requirements_txt_path, "r", encoding="utf-8") as f:
            for package in f.readlines():
                check_vulnerabilities(package.strip())
