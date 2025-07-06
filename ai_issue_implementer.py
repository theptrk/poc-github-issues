#!/usr/bin/env python3
import requests
import subprocess
from typing import Optional
from schemas import GitHubIssue

class AIIssueImplementer:
    def __init__(self, config):
        self.token = config['github_token']
        self.owner = config['repo_owner']
        self.repo = config['repo_name']
    
    def get_most_recent_issue(self) -> Optional[GitHubIssue]:
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues"
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        params = {
            'state': 'open',
            'sort': 'updated',
            'direction': 'desc',
            'per_page': 1
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        issues = response.json()
        
        if not issues:
            return None
        
        return GitHubIssue(**issues[0])
    
    def create_branch(self, issue_number: int) -> str:
        branch_name = f"issue-{issue_number}"
        subprocess.run(['git', 'checkout', '-b', branch_name], check=True)
        return branch_name
    
    def make_placeholder_change(self, title: str) -> None:
        with open('placeholder_change.txt', 'w') as f:
            f.write(f'Placeholder change for: {title}')
    
    def commit_changes(self, commit_message: str) -> None:
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
    
    def push_branch(self, branch_name: str) -> None:
        subprocess.run(['git', 'push', 'origin', branch_name], check=True)
    
    def create_placeholder_pull_request(self, branch_name: str, title: str) -> Optional[str]:
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/pulls"
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        data = {
            'title': title,
            'body': 'Placeholder PR - AI implementation will go here',
            'head': branch_name,
            'base': 'main'
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        pr = response.json()
        
        return pr['html_url']

def main():
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    config = {
        'github_token': os.getenv('GITHUB_TOKEN'),
        'repo_owner': os.getenv('REPO_OWNER'),
        'repo_name': os.getenv('REPO_NAME')
    }
    
    if not all(config.values()):
        print("Error: Missing required environment variables (GITHUB_TOKEN, REPO_OWNER, REPO_NAME)")
        return
    
    implementer = AIIssueImplementer(config)
    
    print("Testing branch creation...")
    try:
        branch_name = implementer.create_branch(999)
        print(f"Successfully created branch: {branch_name}")
        
        print("Making placeholder change...")
        implementer.make_placeholder_change("Test issue")
        print("Created placeholder_change.txt")
        
        print("Committing changes...")
        implementer.commit_changes("Test commit for branch creation")
        print("Changes committed successfully")
        
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()