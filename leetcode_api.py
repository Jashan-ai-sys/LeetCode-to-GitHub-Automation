"""
LeetCode API Handler
Fetches submissions and problem details using LeetCode's GraphQL API
"""

import requests
import json
import time
from typing import Optional, Dict, List, Any


class LeetCodeAPI:
    """Handles all LeetCode API interactions"""
    
    BASE_URL = "https://leetcode.com"
    GRAPHQL_URL = "https://leetcode.com/graphql"
    
    # Language extension mapping
    LANGUAGE_EXTENSIONS = {
        "python": ".py",
        "python3": ".py",
        "java": ".java",
        "cpp": ".cpp",
        "c": ".c",
        "csharp": ".cs",
        "javascript": ".js",
        "typescript": ".ts",
        "go": ".go",
        "ruby": ".rb",
        "swift": ".swift",
        "kotlin": ".kt",
        "rust": ".rs",
        "scala": ".scala",
        "php": ".php",
        "mysql": ".sql",
        "postgresql": ".sql",
        "mssql": ".sql",
        "oraclesql": ".sql",
    }
    
    def __init__(self, session_cookie: str, csrf_token: str = ""):
        """Initialize with LeetCode session cookie"""
        self.session = requests.Session()
        self.session.cookies.set("LEETCODE_SESSION", session_cookie, domain=".leetcode.com")
        if csrf_token:
            self.session.cookies.set("csrftoken", csrf_token, domain=".leetcode.com")
        
        self.session.headers.update({
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            "Origin": "https://leetcode.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        
        if csrf_token:
            self.session.headers["x-csrftoken"] = csrf_token
    
    def get_user_profile(self) -> Optional[Dict]:
        """Get current user's profile to verify authentication"""
        query = """
        query globalData {
            userStatus {
                username
                isSignedIn
                avatar
            }
        }
        """
        
        try:
            response = self.session.post(
                self.GRAPHQL_URL,
                json={"query": query}
            )
            data = response.json()
            return data.get("data", {}).get("userStatus")
        except Exception as e:
            print(f"Error fetching profile: {e}")
            return None
    
    def get_all_submissions(self, limit: int = 20, offset: int = 0) -> List[Dict]:
        """Fetch user's submission history"""
        query = """
        query submissionList($offset: Int!, $limit: Int!, $lastKey: String, $questionSlug: String, $lang: Int, $status: Int) {
            submissionList(offset: $offset, limit: $limit, lastKey: $lastKey, questionSlug: $questionSlug, lang: $lang, status: $status) {
                lastKey
                hasNext
                submissions {
                    id
                    title
                    titleSlug
                    status
                    statusDisplay
                    lang
                    langName
                    runtime
                    timestamp
                    memory
                }
            }
        }
        """
        
        try:
            response = self.session.post(
                self.GRAPHQL_URL,
                json={
                    "query": query,
                    "variables": {
                        "offset": offset,
                        "limit": limit,
                        "status": 10  # 10 = Accepted submissions only
                    }
                }
            )
            data = response.json()
            submission_list = data.get("data", {}).get("submissionList", {})
            return submission_list.get("submissions", [])
        except Exception as e:
            print(f"Error fetching submissions: {e}")
            return []
    
    def get_todays_submissions(self) -> List[Dict]:
        """Fetch only today's accepted submissions"""
        from datetime import datetime, timezone
        
        # Get today's date at midnight (UTC)
        today = datetime.now(timezone.utc).date()
        
        print(f"Fetching today's submissions ({today})...")
        
        # Fetch recent submissions
        submissions = self.get_all_submissions(limit=50, offset=0)
        
        todays_subs = []
        for sub in submissions:
            # Convert timestamp to date
            timestamp = int(sub.get("timestamp", 0))
            sub_date = datetime.fromtimestamp(timestamp, timezone.utc).date()
            
            if sub_date == today:
                todays_subs.append(sub)
            elif sub_date < today:
                # Stop if we've gone past today (submissions are ordered by time)
                break
        
        print(f"  Found {len(todays_subs)} submissions from today")
        return todays_subs
    
    def get_all_accepted_submissions(self, max_submissions: int = 500, today_only: bool = False) -> List[Dict]:
        """Fetch accepted submissions with pagination"""
        if today_only:
            return self.get_todays_submissions()
        
        all_submissions = []
        offset = 0
        limit = 20
        
        print("Fetching your accepted submissions...")
        
        while len(all_submissions) < max_submissions:
            submissions = self.get_all_submissions(limit=limit, offset=offset)
            
            if not submissions:
                break
                
            all_submissions.extend(submissions)
            print(f"  Fetched {len(all_submissions)} submissions...")
            
            if len(submissions) < limit:
                break
                
            offset += limit
            time.sleep(0.5)  # Rate limiting
        
        return all_submissions[:max_submissions]
    
    def get_submission_code(self, submission_id: str) -> Optional[str]:
        """Get the actual code from a submission"""
        query = """
        query submissionDetails($submissionId: Int!) {
            submissionDetails(submissionId: $submissionId) {
                code
                timestamp
                statusDisplay
                lang {
                    name
                    verboseName
                }
                question {
                    questionId
                    title
                    titleSlug
                    difficulty
                    topicTags {
                        name
                    }
                }
            }
        }
        """
        
        try:
            response = self.session.post(
                self.GRAPHQL_URL,
                json={
                    "query": query,
                    "variables": {"submissionId": int(submission_id)}
                }
            )
            data = response.json()
            return data.get("data", {}).get("submissionDetails")
        except Exception as e:
            print(f"Error fetching submission code: {e}")
            return None
    
    def get_problem_details(self, title_slug: str) -> Optional[Dict]:
        """Get problem description and metadata"""
        query = """
        query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                title
                titleSlug
                difficulty
                content
                topicTags {
                    name
                    slug
                }
                codeSnippets {
                    lang
                    langSlug
                    code
                }
            }
        }
        """
        
        try:
            response = self.session.post(
                self.GRAPHQL_URL,
                json={
                    "query": query,
                    "variables": {"titleSlug": title_slug}
                }
            )
            data = response.json()
            return data.get("data", {}).get("question")
        except Exception as e:
            print(f"Error fetching problem details: {e}")
            return None
    
    def get_extension(self, language: str) -> str:
        """Get file extension for a language"""
        return self.LANGUAGE_EXTENSIONS.get(language.lower(), ".txt")


def test_connection():
    """Test the API connection"""
    import json
    
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found!")
        return
    
    if not config.get("leetcode_session"):
        print("Error: leetcode_session not set in config.json")
        return
    
    api = LeetCodeAPI(
        config["leetcode_session"],
        config.get("csrf_token", "")
    )
    
    print("Testing LeetCode API connection...")
    profile = api.get_user_profile()
    
    if profile and profile.get("isSignedIn"):
        print(f"✓ Connected as: {profile.get('username')}")
        
        # Fetch a few submissions
        submissions = api.get_all_submissions(limit=5)
        if submissions:
            print(f"✓ Found {len(submissions)} recent accepted submissions")
            for sub in submissions[:3]:
                print(f"  - {sub['title']} ({sub['langName']})")
        else:
            print("! No accepted submissions found")
    else:
        print("✗ Not authenticated. Please check your session cookie.")


if __name__ == "__main__":
    test_connection()
