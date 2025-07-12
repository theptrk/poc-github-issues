#!/usr/bin/env python3
import subprocess

class GitUtils:
    """Utility class for git operations"""
    
    @staticmethod
    def checkout_main() -> None:
        """Switch to main branch"""
        subprocess.run(['git', 'checkout', 'main'], check=True)
    
    @staticmethod
    def create_branch(branch_name: str) -> None:
        """Create and checkout a new branch"""
        subprocess.run(['git', 'checkout', '-b', branch_name], check=True)
    
    @staticmethod
    def add_all() -> None:
        """Stage all changes"""
        subprocess.run(['git', 'add', '.'], check=True)
    
    @staticmethod
    def commit(message: str) -> None:
        """Commit staged changes"""
        subprocess.run(['git', 'commit', '-m', message], check=True)
    
    @staticmethod
    def push_branch(branch_name: str) -> None:
        """Push branch to origin"""
        subprocess.run(['git', 'push', 'origin', branch_name], check=True)
    
    @staticmethod
    def commit_all_changes(message: str) -> None:
        """Stage all changes and commit"""
        GitUtils.add_all()
        GitUtils.commit(message)
    
    @staticmethod
    def create_unique_branch(base_name: str) -> str:
        """Create a branch with unique name, adding suffix if needed"""
        GitUtils.checkout_main()
        
        branch_name = base_name
        counter = 1
        
        while True:
            try:
                GitUtils.create_branch(branch_name)
                return branch_name
            except subprocess.CalledProcessError:
                # Branch already exists, try with suffix
                branch_name = f"{base_name}-{counter}"
                counter += 1