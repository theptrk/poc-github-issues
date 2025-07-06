#!/usr/bin/env python3
import requests
import subprocess
from typing import Optional
from schemas import GitHubIssue, GitHubPullRequest
from git_utils import GitUtils

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
        base_branch_name = f"issue-{issue_number}"
        return GitUtils.create_unique_branch(base_branch_name)
    
    def make_placeholder_change(self, title: str) -> None:
        with open('placeholder_change.txt', 'w') as f:
            f.write(f'Placeholder change for: {title}')
    
    def commit_changes(self, commit_message: str) -> None:
        GitUtils.add_all()
        GitUtils.commit(commit_message)
    
    def push_branch(self, branch_name: str) -> None:
        GitUtils.push_branch(branch_name)
    
    def create_placeholder_pull_request(self, branch_name: str, title: str) -> Optional[GitHubPullRequest]:
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
        
        return GitHubPullRequest(**pr)
    
    def create_full_pull_request_workflow(self, issue_number: int, issue_title: str) -> Optional[str]:
        """Complete workflow: create branch, make changes, commit, push, and create PR"""
        try:
            # Create branch
            branch_name = self.create_branch(issue_number)
            print(f"Created branch: {branch_name}")
            
            # Make placeholder change
            self.make_placeholder_change(issue_title)
            print("Made placeholder change")
            
            # Commit changes
            commit_message = f"AI Implementation: {issue_title}"
            self.commit_changes(commit_message)
            print("Committed changes")
            
            # Push branch
            self.push_branch(branch_name)
            print(f"Pushed branch: {branch_name}")
            
            # Create PR
            pr_title = f"AI Implementation: {issue_title}"
            pr = self.create_placeholder_pull_request(branch_name, pr_title)
            print(f"Created PR: {pr.html_url}")
            
            return pr.html_url
            
        except Exception as e:
            print(f"Error in workflow: {e}")
            return None
        finally:
            # Always return to main branch
            try:
                GitUtils.checkout_main()
                print("Returned to main branch")
            except subprocess.CalledProcessError:
                print("Warning: Could not return to main branch")

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
    
    print("Testing full PR workflow...")
    try:
        # Test the complete workflow
        pr_url = implementer.create_full_pull_request_workflow(888, "Test full workflow")
        
        if pr_url:
            print(f"✅ Full workflow completed successfully!")
            print(f"Pull request created: {pr_url}")
        else:
            print("❌ Workflow failed")
        
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()