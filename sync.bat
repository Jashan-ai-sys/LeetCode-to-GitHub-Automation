@echo off
echo ====================================
echo LeetCode to GitHub Sync
echo ====================================
echo.

cd /d "%~dp0"
python leetcode_sync.py %*

echo.
pause
