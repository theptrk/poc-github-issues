#!/usr/bin/env python3
import unittest
from unittest.mock import Mock, patch
from schemas import GitHubIssue, GitHubPullRequest
from ai_issue_implementer import AIIssueImplementer
from git_utils import GitUtils
from github_utils import GitHubUtils

class TestAIIssueImplementer(unittest.TestCase):
    
    def setUp(self):
        self.config = {
            'github_token': 'test_token',
            'repo_owner': 'test_owner',
            'repo_name': 'test_repo'
        }
    
    @patch.object(GitUtils, 'create_unique_branch')
    def test_create_branch_returns_branch_name(self, mock_create_unique):
        mock_create_unique.return_value = 'issue-123'
        
        implementer = AIIssueImplementer(self.config)
        result = implementer.create_branch(123)
        
        self.assertEqual(result, 'issue-123')
        mock_create_unique.assert_called_once_with('issue-123')
    
    @patch('builtins.open')
    def test_make_placeholder_change_creates_file(self, mock_open):
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        implementer = AIIssueImplementer(self.config)
        implementer.make_placeholder_change('Fix bug X')
        
        mock_open.assert_called_once_with('placeholder_change.txt', 'w')
        mock_file.write.assert_called_once_with('Placeholder change for: Fix bug X')
    
    @patch.object(GitUtils, 'checkout_main')
    @patch.object(GitUtils, 'push_branch')
    @patch.object(GitUtils, 'commit_all_changes')
    @patch.object(GitUtils, 'create_unique_branch')
    @patch('builtins.open')
    def test_create_full_pull_request_workflow_success(self, mock_open, mock_create_branch, 
                                                       mock_commit, mock_push, mock_checkout):
        # Mock GitUtils static methods
        mock_create_branch.return_value = 'issue-123'
        
        # Mock GitHubUtils instance
        mock_github_utils = Mock()
        mock_pr = Mock()
        mock_pr.html_url = 'https://github.com/test/repo/pull/1347'
        mock_github_utils.create_pull_request.return_value = mock_pr
        
        implementer = AIIssueImplementer(self.config)
        implementer.github_utils = mock_github_utils  # Replace with mock
        
        result = implementer.create_full_pull_request_workflow(123, 'Fix bug X')
        
        # Verify the workflow called the right methods
        mock_create_branch.assert_called_once_with('issue-123')
        mock_commit.assert_called_once_with('AI Implementation: Fix bug X')
        mock_push.assert_called_once_with('issue-123')
        mock_github_utils.create_pull_request.assert_called_once_with('issue-123', 'AI Implementation: Fix bug X')
        mock_checkout.assert_called_once()
        
        self.assertEqual(result, 'https://github.com/test/repo/pull/1347')

if __name__ == '__main__':
    unittest.main()