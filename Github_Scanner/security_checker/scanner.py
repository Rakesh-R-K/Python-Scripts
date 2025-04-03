import os
import re
import git
from security_checker.alerts import send_alert

# Define sensitive patterns
SENSITIVE_PATTERNS = [
    r"API_KEY\s*=\s*['\"]\w+['\"]",
    r"SECRET_KEY\s*=\s*['\"]\w+['\"]",
    r"PASSWORD\s*=\s*['\"]\w+['\"]",
    r"AWS_ACCESS_KEY_ID\s*=\s*['\"]\w+['\"]",
    r"AWS_SECRET_ACCESS_KEY\s*=\s*['\"]\w+['\"]"
]

# List of sensitive files
SENSITIVE_FILES = ["config.json", ".env", "id_rsa", "id_rsa.pub"]

def scan_file(file_path):
    """Scan a file for sensitive data."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            for pattern in SENSITIVE_PATTERNS:
                if re.search(pattern, content):
                    print(f"[WARNING] Secret found in: {file_path}")
                    send_alert("GitHub Security Alert", f"Secret detected in: {file_path}")
    except:
        pass  # Ignore unreadable files

def scan_repo(repo_path):
    """Scan repository for sensitive files & secrets."""
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file in SENSITIVE_FILES:
                print(f"[ALERT] Sensitive file found: {file_path}")
                send_alert("GitHub Security Alert", f"Sensitive file detected: {file_path}")
            elif file.endswith(".py") or file.endswith(".env"):  # Scan Python & Env files
                scan_file(file_path)
