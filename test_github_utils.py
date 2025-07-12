#!/usr/bin/env python3
import unittest
from unittest.mock import Mock, patch
from github_utils import GitHubUtils
from schemas import GitHubIssue, GitHubPullRequest

class TestGitHubUtils(unittest.TestCase):
    
    def setUp(self):
        self.config = {
            'github_token': 'test_token',
            'repo_owner': 'test_owner',
            'repo_name': 'test_repo'
        }
    
    @patch('github_utils.requests.get')
    def test_get_most_recent_issue_returns_github_issue_schema(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            'number': 123,
            'title': 'Add feature X',
            'body': 'Please implement feature X that does Y',
            'state': 'open',
            'html_url': 'https://github.com/test/repo/issues/123',
            'updated_at': '2023-01-01T00:00:00Z',
            'labels': []
        }]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        github_utils = GitHubUtils(self.config)
        result = github_utils.get_most_recent_issue()
        
        self.assertIsInstance(result, GitHubIssue)
        self.assertEqual(result.title, 'Add feature X')
        self.assertEqual(result.number, 123)
        self.assertEqual(result.body, 'Please implement feature X that does Y')
    
    @patch('github_utils.requests.post')
    def test_create_pull_request_returns_github_pr_schema(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'number': 1347,
            'html_url': 'https://github.com/test/repo/pull/1347',
            'title': 'AI Implementation: Fix bug X',
            'state': 'open',
            'id': 1,
            'body': 'Placeholder PR - AI implementation will go here'
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        github_utils = GitHubUtils(self.config)
        result = github_utils.create_pull_request('issue-123', 'AI Implementation: Fix bug X')
        
        self.assertIsInstance(result, GitHubPullRequest)
        self.assertEqual(result.html_url, 'https://github.com/test/repo/pull/1347')
        self.assertEqual(result.number, 1347)
        self.assertEqual(result.title, 'AI Implementation: Fix bug X')

if __name__ == '__main__':
    unittest.main()