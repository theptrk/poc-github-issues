#!/usr/bin/env python3
import requests
from typing import Optional
from schemas import GitHubIssue, GitHubPullRequest

class GitHubUtils:
    """Utility class for GitHub API operations"""
    
    def __init__(self, config):
        self.token = config['github_token']
        self.owner = config['repo_owner']
        self.repo = config['repo_name']
    
    def get_most_recent_issue(self) -> Optional[GitHubIssue]:
        """Get the most recent open issue from the repository"""
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
    
    def create_pull_request(self, branch_name: str, title: str) -> Optional[GitHubPullRequest]:
        """Create a pull request on GitHub"""
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