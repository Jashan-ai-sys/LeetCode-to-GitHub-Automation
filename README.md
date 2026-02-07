# LeetCode to GitHub Automation

Automatically sync your LeetCode submissions to GitHub! 🚀

## Features

- ✅ Fetches your accepted LeetCode submissions
- ✅ Organizes solutions by difficulty (Easy/Medium/Hard)
- ✅ Adds problem metadata as comments in each file
- ✅ Automatic git commit and push
- ✅ Supports multiple programming languages
- ✅ Avoids duplicates - only syncs new solutions

## Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your LeetCode Session Cookie

1. Go to [leetcode.com](https://leetcode.com) and **log in**
2. Open **Developer Tools** (Press `F12`)
3. Go to **Application** → **Cookies** → `leetcode.com`
4. Find and copy the value of `LEETCODE_SESSION`
5. (Optional) Also copy `csrftoken` for better reliability

### 3. Configure

Edit `config.json`:

```json
{
    "leetcode_session": "PASTE_YOUR_SESSION_COOKIE_HERE",
    "csrf_token": "PASTE_YOUR_CSRF_TOKEN_HERE",
    "github_repo_path": "./solutions",
    "organize_by": "difficulty",
    "include_problem_description": true,
    "auto_push": true
}
```

### 4. Run the Sync

```bash
# Sync your latest 100 submissions
python leetcode_sync.py

# Sync more submissions
python leetcode_sync.py --max 500

# Test connection first
python leetcode_sync.py --test

# Preview without making changes
python leetcode_sync.py --dry-run
```

## CLI Options

| Option | Description |
|--------|-------------|
| `--test, -t` | Test LeetCode connection only |
| `--dry-run, -d` | Preview what would be synced |
| `--max N, -m N` | Maximum submissions to sync (default: 100) |
| `--force, -f` | Overwrite existing solutions |
| `--config FILE` | Use custom config file |

## Folder Structure

After syncing, your solutions will be organized like this:

```
solutions/
├── Easy/
│   ├── 0001-two-sum.py
│   ├── 0009-palindrome-number.py
│   └── ...
├── Medium/
│   ├── 0002-add-two-numbers.py
│   └── ...
└── Hard/
    ├── 0004-median-of-two-sorted-arrays.py
    └── ...
```

## Solution File Format

Each solution file includes helpful metadata:

```python
"""
Problem: 1. Two Sum
Difficulty: Easy
URL: https://leetcode.com/problems/two-sum/
Topics: Array, Hash Table
Runtime: 40 ms
Memory: 14.2 MB
Date: 2026-02-07
"""

class Solution:
    def twoSum(self, nums, target):
        # Your solution code
        ...
```

## Automation (Optional)

### Windows Task Scheduler

To run automatically every day:

1. Open **Task Scheduler**
2. Create a new task
3. Set trigger: Daily at your preferred time
4. Action: Start a program
   - Program: `python`
   - Arguments: `C:\Users\WIN11\githubautomate\leetcode_sync.py`
   - Start in: `C:\Users\WIN11\githubautomate`

### Using a Batch Script

Create `sync.bat`:

```batch
@echo off
cd /d C:\Users\WIN11\githubautomate
python leetcode_sync.py
pause
```

Double-click to run manually anytime!

## Troubleshooting

### "Not authenticated" Error

Your session cookie may have expired. Get a fresh one from LeetCode:
1. Log out and log back in
2. Get the new `LEETCODE_SESSION` cookie
3. Update `config.json`

### "Failed to push" Error

Make sure:
1. Git is configured with your GitHub credentials
2. The remote repository exists
3. You have push access to the repository

Run these commands if needed:

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

## License

MIT License - Feel free to modify and share!

---

Made with ❤️ for LeetCode grinders
