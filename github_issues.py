#!/usr/bin/env python3
import requests
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_github_issues(owner, repo, token=None):
    """
    Fetch issues from a GitHub repository
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'GitHub-Issues-Fetcher'
    }
    
    if token:
        headers['Authorization'] = f'token {token}'
    
    params = {
        'state': 'all',
        'sort': 'updated',
        'direction': 'desc',
        'per_page': 100
    }
    
    try:
        logging.info(f"Making request to GitHub API: {url}")
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 401:
            logging.error("Authentication failed - token is invalid or expired")
            return None
        elif response.status_code == 403:
            logging.error("API rate limit exceeded or insufficient permissions")
            return None
        elif response.status_code == 404:
            logging.error(f"Repository {owner}/{repo} not found or not accessible")
            return None
        
        response.raise_for_status()
        logging.info(f"Successfully fetched {len(response.json())} issues")
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
        return None
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Connection error occurred: {e}")
        return None
    except requests.exceptions.Timeout as e:
        logging.error(f"Timeout error occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error occurred: {e}")
        return None

def print_most_recent_issue(issues):
    """
    Print the most recently updated issue
    """
    if not issues:
        print("No issues found")
        return
    
    most_recent = issues[0]
    
    print(f"\n# Most Recently Updated Issue:")
    print(f"Title: {most_recent['title']}")
    print(f"Number: #{most_recent['number']}")
    print(f"State: {most_recent['state']}")
    print(f"Updated: {most_recent['updated_at']}")
    print(f"URL: {most_recent['html_url']}")
    print(most_recent)
    
    if most_recent['body']:
        body_preview = most_recent['body'][:200] + "..." if len(most_recent['body']) > 200 else most_recent['body']
        print(f"Body: {body_preview}")

def main():
    token = os.getenv('GITHUB_TOKEN')
    owner = os.getenv('REPO_OWNER')
    repo = os.getenv('REPO_NAME')
    
    if not owner or not repo:
        logging.error("Missing required environment variables")
        return
    
    if not token:
        logging.warning("No GitHub token provided - API rate limits will be lower")
    
    logging.info(f"Fetching issues from {owner}/{repo}")
    issues = get_github_issues(owner, repo, token)

    logging.info("\n# Issues (sort: updated desc):")
    for issue in issues:
        logging.info(f"#{issue['number']} {issue['title']}")
    
    if issues:
        print_most_recent_issue(issues)
        logging.info("Successfully completed fetching and displaying issues")
    else:
        logging.error("Failed to fetch issues")

if __name__ == "__main__":
    main()