/*
 * Problem: 151. Reverse Words in a String
 * Difficulty: Medium
 * URL: https://leetcode.com/problems/reverse-words-in-a-string/
 * Topics: Two Pointers, String
 * Runtime: 3 ms
 * Memory: 10.2 MB
 * Date: 2026-02-07
*/
class Solution {
public:
    string reverseWords(string s) {
        int i = s.length() - 1;
        string ans = "";

        while (i >= 0) {
                while (i >= 0 && s[i] == ' ') {
                i--;
            }
            if (i < 0) break;

            int j = i;
            while (i >= 0 && s[i] != ' ') {
                i--;
            }           
            ans += s.substr(i + 1, j - i);
            ans += ' ';
        }
        if (!ans.empty()) ans.pop_back();

        return ans;
    }
};
