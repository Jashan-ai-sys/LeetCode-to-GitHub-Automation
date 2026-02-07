"""
Git Handler
Manages Git operations for committing and pushing solutions
"""

import os
import subprocess
from typing import Optional, Tuple
from datetime import datetime


class GitHandler:
    """Handles all Git operations"""
    
    def __init__(self, repo_path: str):
        """Initialize with repository path"""
        self.repo_path = os.path.abspath(repo_path)
    
    def run_git_command(self, args: list, cwd: str = None) -> Tuple[bool, str]:
        """Run a git command and return success status and output"""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=cwd or self.repo_path,
                capture_output=True,
                text=True
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)
    
    def is_git_repo(self) -> bool:
        """Check if the path is a git repository"""
        git_dir = os.path.join(self.repo_path, ".git")
        return os.path.isdir(git_dir)
    
    def init_repo(self) -> bool:
        """Initialize a new git repository"""
        if self.is_git_repo():
            print(f"Repository already exists at {self.repo_path}")
            return True
        
        os.makedirs(self.repo_path, exist_ok=True)
        success, output = self.run_git_command(["init"])
        
        if success:
            print(f"✓ Initialized git repository at {self.repo_path}")
            
            # Create initial README
            readme_path = os.path.join(self.repo_path, "README.md")
            if not os.path.exists(readme_path):
                with open(readme_path, "w") as f:
                    f.write("# LeetCode Solutions\n\n")
                    f.write("My solutions to LeetCode problems, automatically synced.\n\n")
                    f.write("## Structure\n\n")
                    f.write("Solutions are organized by difficulty:\n")
                    f.write("- `Easy/` - Easy problems\n")
                    f.write("- `Medium/` - Medium problems\n")
                    f.write("- `Hard/` - Hard problems\n")
                
                self.run_git_command(["add", "README.md"])
                self.run_git_command(["commit", "-m", "Initial commit: Add README"])
        else:
            print(f"✗ Failed to initialize repository: {output}")
        
        return success
    
    def add_remote(self, remote_url: str, remote_name: str = "origin") -> bool:
        """Add a remote repository"""
        # Check if remote already exists
        success, output = self.run_git_command(["remote", "get-url", remote_name])
        
        if success:
            print(f"Remote '{remote_name}' already exists: {output.strip()}")
            return True
        
        success, output = self.run_git_command(["remote", "add", remote_name, remote_url])
        
        if success:
            print(f"✓ Added remote '{remote_name}': {remote_url}")
        else:
            print(f"✗ Failed to add remote: {output}")
        
        return success
    
    def commit_file(self, file_path: str, message: str) -> bool:
        """Stage and commit a single file"""
        # Get relative path from repo root
        rel_path = os.path.relpath(file_path, self.repo_path)
        
        # Stage the file
        success, output = self.run_git_command(["add", rel_path])
        if not success:
            print(f"✗ Failed to stage {rel_path}: {output}")
            return False
        
        # Check if there are changes to commit
        success, output = self.run_git_command(["diff", "--cached", "--quiet"])
        if success:
            # No changes to commit
            return True
        
        # Commit
        success, output = self.run_git_command(["commit", "-m", message])
        if success:
            print(f"✓ Committed: {message}")
        else:
            if "nothing to commit" in output:
                return True
            print(f"✗ Failed to commit: {output}")
        
        return success
    
    def commit_all(self, message: str) -> bool:
        """Stage and commit all changes"""
        # Stage all changes
        success, output = self.run_git_command(["add", "-A"])
        if not success:
            print(f"✗ Failed to stage changes: {output}")
            return False
        
        # Check if there are changes
        success, output = self.run_git_command(["diff", "--cached", "--quiet"])
        if success:
            print("No changes to commit")
            return True
        
        # Commit
        success, output = self.run_git_command(["commit", "-m", message])
        if success:
            print(f"✓ Committed: {message}")
        else:
            print(f"✗ Failed to commit: {output}")
        
        return success
    
    def push(self, remote: str = "origin", branch: str = "main") -> bool:
        """Push commits to remote"""
        # First, ensure we have the branch set up
        success, output = self.run_git_command(["branch", "-M", branch])
        
        # Push to remote
        success, output = self.run_git_command(["push", "-u", remote, branch])
        
        if success:
            print(f"✓ Pushed to {remote}/{branch}")
        else:
            # Try force push if first time
            if "failed to push" in output.lower() or "rejected" in output.lower():
                print("Attempting to set upstream and push...")
                success, output = self.run_git_command(["push", "--set-upstream", remote, branch])
                if success:
                    print(f"✓ Pushed to {remote}/{branch}")
                else:
                    print(f"✗ Failed to push: {output}")
            else:
                print(f"✗ Failed to push: {output}")
        
        return success
    
    def get_status(self) -> str:
        """Get current git status"""
        success, output = self.run_git_command(["status", "--short"])
        return output if success else "Unable to get status"


if __name__ == "__main__":
    # Test the git handler
    handler = GitHandler("./solutions")
    
    if not handler.is_git_repo():
        handler.init_repo()
    
    print("\nGit Status:")
    print(handler.get_status())
