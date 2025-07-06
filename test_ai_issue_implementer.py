#!/usr/bin/env python3
import unittest
from unittest import mock
from unittest.mock import Mock, patch
import subprocess
from schemas import GitHubIssue, GitHubPullRequest
from ai_issue_implementer import AIIssueImplementer

class TestAIIssueImplementer(unittest.TestCase):
    
    def setUp(self):
        self.config = {
            'github_token': 'test_token',
            'repo_owner': 'test_owner',
            'repo_name': 'test_repo'
        }
    
    @patch('ai_issue_implementer.requests.get')
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
        
        implementer = AIIssueImplementer(self.config)
        result = implementer.get_most_recent_issue()
        
        self.assertIsInstance(result, GitHubIssue)
        self.assertEqual(result.title, 'Add feature X')
        self.assertEqual(result.number, 123)
        self.assertEqual(result.body, 'Please implement feature X that does Y')
    
    @patch('subprocess.run')
    def test_create_branch_returns_branch_name(self, mock_run):
        implementer = AIIssueImplementer(self.config)
        result = implementer.create_branch(123)
        
        self.assertEqual(result, 'issue-123')
        mock_run.assert_called_once_with(['git', 'checkout', '-b', 'issue-123'], check=True)
    
    @patch('builtins.open')
    def test_make_placeholder_change_creates_file(self, mock_open):
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        implementer = AIIssueImplementer(self.config)
        implementer.make_placeholder_change('Fix bug X')
        
        mock_open.assert_called_once_with('placeholder_change.txt', 'w')
        mock_file.write.assert_called_once_with('Placeholder change for: Fix bug X')
    
    @patch('subprocess.run')
    def test_commit_changes_runs_git_commands(self, mock_run):
        implementer = AIIssueImplementer(self.config)
        implementer.commit_changes('Fix bug X')
        
        expected_calls = [
            mock.call(['git', 'add', '.'], check=True),
            mock.call(['git', 'commit', '-m', 'Fix bug X'], check=True)
        ]
        mock_run.assert_has_calls(expected_calls)
    
    @patch('subprocess.run')
    def test_push_branch_runs_git_push(self, mock_run):
        implementer = AIIssueImplementer(self.config)
        implementer.push_branch('issue-123')
        
        mock_run.assert_called_once_with(['git', 'push', 'origin', 'issue-123'], check=True)
    
    @patch('ai_issue_implementer.requests.post')
    def test_create_placeholder_pull_request_returns_github_pr_schema(self, mock_post):
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
        
        implementer = AIIssueImplementer(self.config)
        result = implementer.create_placeholder_pull_request('issue-123', 'AI Implementation: Fix bug X')
        
        self.assertIsInstance(result, GitHubPullRequest)
        self.assertEqual(result.html_url, 'https://github.com/test/repo/pull/1347')
        self.assertEqual(result.number, 1347)
        self.assertEqual(result.title, 'AI Implementation: Fix bug X')

if __name__ == '__main__':
    unittest.main()