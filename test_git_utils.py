#!/usr/bin/env python3
import unittest
from unittest.mock import patch
import subprocess
from git_utils import GitUtils

class TestGitUtils(unittest.TestCase):
    
    @patch('git_utils.subprocess.run')
    def test_checkout_main(self, mock_run):
        GitUtils.checkout_main()
        mock_run.assert_called_once_with(['git', 'checkout', 'main'], check=True)
    
    @patch('git_utils.subprocess.run')
    def test_create_branch(self, mock_run):
        GitUtils.create_branch('feature-branch')
        mock_run.assert_called_once_with(['git', 'checkout', '-b', 'feature-branch'], check=True)
    
    @patch('git_utils.subprocess.run')
    def test_add_all(self, mock_run):
        GitUtils.add_all()
        mock_run.assert_called_once_with(['git', 'add', '.'], check=True)
    
    @patch('git_utils.subprocess.run')
    def test_commit(self, mock_run):
        GitUtils.commit('test commit message')
        mock_run.assert_called_once_with(['git', 'commit', '-m', 'test commit message'], check=True)
    
    @patch('git_utils.subprocess.run')
    def test_push_branch(self, mock_run):
        GitUtils.push_branch('feature-branch')
        mock_run.assert_called_once_with(['git', 'push', 'origin', 'feature-branch'], check=True)
    
    @patch.object(GitUtils, 'create_branch')
    @patch.object(GitUtils, 'checkout_main')
    def test_create_unique_branch_first_try_succeeds(self, mock_checkout, mock_create):
        result = GitUtils.create_unique_branch('issue-123')
        
        mock_checkout.assert_called_once()
        mock_create.assert_called_once_with('issue-123')
        self.assertEqual(result, 'issue-123')
    
    @patch.object(GitUtils, 'create_branch')
    @patch.object(GitUtils, 'checkout_main')
    def test_create_unique_branch_handles_conflicts(self, mock_checkout, mock_create):
        # Simulate first two attempts failing, third succeeds
        mock_create.side_effect = [
            subprocess.CalledProcessError(1, 'git'),  # issue-123 exists
            subprocess.CalledProcessError(1, 'git'),  # issue-123-1 exists  
            None  # issue-123-2 succeeds
        ]
        
        result = GitUtils.create_unique_branch('issue-123')
        
        mock_checkout.assert_called_once()
        self.assertEqual(mock_create.call_count, 3)
        mock_create.assert_any_call('issue-123')
        mock_create.assert_any_call('issue-123-1') 
        mock_create.assert_any_call('issue-123-2')
        self.assertEqual(result, 'issue-123-2')

if __name__ == '__main__':
    unittest.main()