"""
File Manager
Handles file organization and solution file creation
"""

import os
import re
import html
from typing import Dict, Optional
from datetime import datetime


class FileManager:
    """Manages solution file organization"""
    
    def __init__(self, base_path: str, organize_by: str = "difficulty"):
        """
        Initialize file manager
        
        Args:
            base_path: Root directory for solutions
            organize_by: Organization method ('difficulty' or 'topic')
        """
        self.base_path = os.path.abspath(base_path)
        self.organize_by = organize_by
        
        # Create base directories
        os.makedirs(self.base_path, exist_ok=True)
        if organize_by == "difficulty":
            for difficulty in ["Easy", "Medium", "Hard"]:
                os.makedirs(os.path.join(self.base_path, difficulty), exist_ok=True)
    
    def sanitize_filename(self, name: str) -> str:
        """Convert problem title to valid filename"""
        # Remove special characters
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        # Replace spaces with hyphens
        name = re.sub(r'\s+', '-', name)
        # Remove consecutive hyphens
        name = re.sub(r'-+', '-', name)
        # Convert to lowercase
        return name.lower().strip('-')
    
    def get_solution_path(
        self,
        problem_id: str,
        title: str,
        difficulty: str,
        extension: str
    ) -> str:
        """Get the full path for a solution file"""
        # Format: XXXX-problem-title.ext
        filename = f"{problem_id.zfill(4)}-{self.sanitize_filename(title)}{extension}"
        
        if self.organize_by == "difficulty":
            folder = difficulty.capitalize()
            return os.path.join(self.base_path, folder, filename)
        else:
            return os.path.join(self.base_path, filename)
    
    def clean_html_content(self, html_content: str) -> str:
        """Convert HTML to plain text for comments"""
        if not html_content:
            return ""
        
        # Unescape HTML entities
        text = html.unescape(html_content)
        
        # Remove HTML tags but keep content
        text = re.sub(r'<pre[^>]*>.*?</pre>', '', text, flags=re.DOTALL)  # Remove code blocks
        text = re.sub(r'<[^>]+>', '', text)  # Remove remaining tags
        
        # Clean up whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()
        
        return text
    
    def generate_header_comment(
        self,
        problem_id: str,
        title: str,
        difficulty: str,
        url: str,
        topics: list,
        language: str,
        runtime: str = "",
        memory: str = "",
        description: str = ""
    ) -> str:
        """Generate a header comment for the solution file"""
        
        # Determine comment style based on language
        if language.lower() in ["python", "python3", "ruby"]:
            comment_start = '"""'
            comment_end = '"""'
            line_prefix = ""
        elif language.lower() in ["java", "cpp", "c", "javascript", "typescript", "go", "kotlin", "scala", "rust", "swift", "csharp"]:
            comment_start = "/*"
            comment_end = "*/"
            line_prefix = " * "
        elif language.lower() in ["mysql", "postgresql", "mssql", "oraclesql"]:
            comment_start = "/*"
            comment_end = "*/"
            line_prefix = " * "
        else:
            comment_start = "/*"
            comment_end = "*/"
            line_prefix = " * "
        
        lines = [
            comment_start,
            f"{line_prefix}Problem: {problem_id}. {title}",
            f"{line_prefix}Difficulty: {difficulty}",
            f"{line_prefix}URL: {url}",
        ]
        
        if topics:
            lines.append(f"{line_prefix}Topics: {', '.join(topics)}")
        
        if runtime:
            lines.append(f"{line_prefix}Runtime: {runtime}")
        
        if memory:
            lines.append(f"{line_prefix}Memory: {memory}")
        
        lines.append(f"{line_prefix}Date: {datetime.now().strftime('%Y-%m-%d')}")
        lines.append(comment_end)
        lines.append("")  # Empty line after comment
        
        return "\n".join(lines)
    
    def save_solution(
        self,
        code: str,
        problem_id: str,
        title: str,
        title_slug: str,
        difficulty: str,
        extension: str,
        language: str,
        topics: list = None,
        runtime: str = "",
        memory: str = "",
        include_header: bool = True
    ) -> Optional[str]:
        """
        Save a solution to file
        
        Returns the file path if successful, None otherwise
        """
        try:
            file_path = self.get_solution_path(problem_id, title, difficulty, extension)
            
            # Check if file already exists (skip if exists)
            if os.path.exists(file_path):
                return None
            
            # Generate content
            content = ""
            if include_header:
                url = f"https://leetcode.com/problems/{title_slug}/"
                content = self.generate_header_comment(
                    problem_id=problem_id,
                    title=title,
                    difficulty=difficulty,
                    url=url,
                    topics=topics or [],
                    language=language,
                    runtime=runtime,
                    memory=memory
                )
            
            content += code
            
            # Ensure file ends with newline
            if not content.endswith("\n"):
                content += "\n"
            
            # Write file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            return file_path
            
        except Exception as e:
            print(f"Error saving solution: {e}")
            return None
    
    def get_existing_solutions(self) -> set:
        """Get set of existing solution filenames (without extension)"""
        existing = set()
        
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                # Extract problem ID from filename
                match = re.match(r'^(\d{4})-', file)
                if match:
                    existing.add(match.group(1))
        
        return existing


if __name__ == "__main__":
    # Test the file manager
    fm = FileManager("./test_solutions")
    
    test_code = """def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
    return []
"""
    
    path = fm.save_solution(
        code=test_code,
        problem_id="1",
        title="Two Sum",
        title_slug="two-sum",
        difficulty="Easy",
        extension=".py",
        language="python3",
        topics=["Array", "Hash Table"],
        runtime="40 ms",
        memory="14.2 MB"
    )
    
    if path:
        print(f"✓ Saved solution to: {path}")
    else:
        print("Solution already exists or error occurred")
