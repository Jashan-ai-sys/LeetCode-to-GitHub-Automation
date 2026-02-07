/*
 * Problem: 392. Is Subsequence
 * Difficulty: Easy
 * URL: https://leetcode.com/problems/is-subsequence/
 * Topics: Two Pointers, String, Dynamic Programming
 * Runtime: 0 ms
 * Memory: 8.7 MB
 * Date: 2026-02-07
*/
class Solution {
public:
    bool isSubsequence(string s, string t) {
        int p1=0;
        int p2=0;
        int c=0;
        while(p1<s.length()&& p2<t.length()){
            if(s[p1]==t[p2]){
                p1++;
                p2++;
               
            }
            else{
                p2++;
            }
        }
        if(p1==s.length())
        return true;
        else
        return false;
        
    }
};
