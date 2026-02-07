"""
LeetCode to GitHub Sync
Main script to sync LeetCode submissions to your GitHub repository
"""

import json
import os
import sys
import argparse
import time
from datetime import datetime

from leetcode_api import LeetCodeAPI
from git_handler import GitHandler
from file_manager import FileManager


def load_config(config_path: str = "config.json") -> dict:
    """Load configuration from JSON file"""
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {config_path} not found!")
        print("Please create a config.json with your LeetCode session cookie.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing {config_path}: {e}")
        sys.exit(1)


def sync_submissions(
    config: dict,
    max_submissions: int = 100,
    dry_run: bool = False,
    force: bool = False,
    today_only: bool = False
):
    """
    Main sync function
    
    Args:
        config: Configuration dictionary
        max_submissions: Maximum number of submissions to sync
        dry_run: If True, don't actually save files or commit
        force: If True, overwrite existing files
    """
    # Validate config
    if not config.get("leetcode_session"):
        print("Error: leetcode_session not set in config.json")
        print("\nTo get your session cookie:")
        print("1. Go to leetcode.com and log in")
        print("2. Open Developer Tools (F12)")
        print("3. Go to Application > Cookies > leetcode.com")
        print("4. Copy the value of 'LEETCODE_SESSION'")
        return
    
    # Initialize components
    api = LeetCodeAPI(
        config["leetcode_session"],
        config.get("csrf_token", "")
    )
    
    repo_path = config.get("github_repo_path", "./solutions")
    
    file_manager = FileManager(
        repo_path,
        config.get("organize_by", "difficulty")
    )
    
    git_handler = GitHandler(repo_path)
    
    # Verify authentication
    print("=" * 50)
    print("LeetCode to GitHub Sync")
    print("=" * 50)
    print()
    
    profile = api.get_user_profile()
    if not profile or not profile.get("isSignedIn"):
        print("✗ Not authenticated. Please check your session cookie.")
        return
    
    print(f"✓ Logged in as: {profile.get('username')}")
    print()
    
    # Initialize git repo if needed
    if not dry_run:
        if not git_handler.is_git_repo():
            git_handler.init_repo()
    
    # Get existing solutions to avoid duplicates
    existing = file_manager.get_existing_solutions()
    print(f"Found {len(existing)} existing solutions in repository")
    print()
    
    # Fetch submissions
    submissions = api.get_all_accepted_submissions(max_submissions, today_only=today_only)
    
    if not submissions:
        print("No accepted submissions found.")
        return
    
    print(f"\nFound {len(submissions)} accepted submissions")
    print("-" * 50)
    print()
    
    # Track unique problems (avoid duplicate solutions for same problem)
    synced_problems = set()
    new_solutions = 0
    skipped = 0
    
    for i, submission in enumerate(submissions, 1):
        title_slug = submission.get("titleSlug")
        title = submission.get("title")
        
        # Skip if already processed this problem
        if title_slug in synced_problems:
            continue
        
        synced_problems.add(title_slug)
        
        print(f"[{i}/{len(submissions)}] Processing: {title}")
        
        # Get detailed submission info
        details = api.get_submission_code(submission["id"])
        
        if not details:
            print(f"  ✗ Could not fetch submission details")
            continue
        
        # Get problem info
        question = details.get("question", {})
        problem_id = question.get("questionId", "0")
        difficulty = question.get("difficulty", "Unknown")
        topics = [tag["name"] for tag in question.get("topicTags", [])]
        
        # Skip if already exists (unless force)
        if problem_id.zfill(4) in existing and not force:
            print(f"  → Skipping (already exists)")
            skipped += 1
            continue
        
        # Get language and extension
        lang_info = details.get("lang", {})
        language = lang_info.get("name", submission.get("lang", "unknown"))
        extension = api.get_extension(language)
        
        code = details.get("code", "")
        
        if dry_run:
            print(f"  [DRY RUN] Would save: {problem_id.zfill(4)}-{title_slug}{extension}")
            new_solutions += 1
            continue
        
        # Save solution
        file_path = file_manager.save_solution(
            code=code,
            problem_id=problem_id,
            title=title,
            title_slug=title_slug,
            difficulty=difficulty,
            extension=extension,
            language=language,
            topics=topics,
            runtime=submission.get("runtime", ""),
            memory=submission.get("memory", ""),
            include_header=config.get("include_problem_description", True)
        )
        
        if file_path:
            print(f"  ✓ Saved: {os.path.basename(file_path)}")
            new_solutions += 1
            
            # Commit each file
            commit_msg = config.get(
                "commit_message_template",
                "Add: {problem_id} - {problem_title} [{difficulty}]"
            ).format(
                problem_id=problem_id,
                problem_title=title,
                difficulty=difficulty
            )
            
            git_handler.commit_file(file_path, commit_msg)
        else:
            print(f"  → Skipping (already exists)")
            skipped += 1
        
        # Rate limiting
        time.sleep(0.3)
    
    # Summary
    print()
    print("=" * 50)
    print("Sync Complete!")
    print("=" * 50)
    print(f"  New solutions: {new_solutions}")
    print(f"  Skipped (existing): {skipped}")
    print()
    
    # Push to remote
    if not dry_run and new_solutions > 0 and config.get("auto_push", True):
        print("Pushing to GitHub...")
        git_handler.push()


def main():
    parser = argparse.ArgumentParser(
        description="Sync LeetCode submissions to GitHub"
    )
    
    parser.add_argument(
        "--config", "-c",
        default="config.json",
        help="Path to config file (default: config.json)"
    )
    
    parser.add_argument(
        "--max", "-m",
        type=int,
        default=100,
        help="Maximum submissions to sync (default: 100)"
    )
    
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Show what would be synced without making changes"
    )
    
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Overwrite existing solutions"
    )
    
    parser.add_argument(
        "--today",
        action="store_true",
        help="Sync only today's submissions"
    )
    
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Test LeetCode API connection only"
    )
    
    args = parser.parse_args()
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    config = load_config(args.config)
    
    if args.test:
        # Just test the connection
        from leetcode_api import test_connection
        test_connection()
    else:
        sync_submissions(
            config,
            max_submissions=args.max,
            dry_run=args.dry_run,
            force=args.force,
            today_only=args.today or config.get("today_only", False)
        )


if __name__ == "__main__":
    main()
