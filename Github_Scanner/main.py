# -*- coding: utf-8 -*-

import os
import git
from security_checker.scanner import scan_repo
from security_checker.permissions import check_repo_permissions
from security_checker.vulnerabilities import scan_dependencies

def main():
    repo_url = input("Enter GitHub repository URL: ").strip()
    repo_name = repo_url.split("github.com/")[-1].replace(".git", "")
    repo_path = "temp_repo"

    # Clone the repository
    if os.path.exists(repo_path):
        os.system(f"rm -rf {repo_path}")  # Remove old repo
    print(f"[INFO] Cloning repository {repo_url}...")
    git.Repo.clone_from(repo_url, repo_path)

    # Run security scans
    scan_repo(repo_path)
    check_repo_permissions(repo_name)
    scan_dependencies(repo_path)

    # Cleanup
    os.system(f"rm -rf {repo_path}")
    print("[✔] Security scan completed!")

if __name__ == "__main__":
    main()
