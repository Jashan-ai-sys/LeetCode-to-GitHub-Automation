/*
 * Problem: 808. Number of Matching Subsequences
 * Difficulty: Medium
 * URL: https://leetcode.com/problems/number-of-matching-subsequences/
 * Topics: Array, Hash Table, String, Binary Search, Dynamic Programming, Trie, Sorting
 * Runtime: 275 ms
 * Memory: 340.9 MB
 * Date: 2026-02-07
*/
class Solution {
public:
    bool fun(string s , string words){
        int p1=0;
        int p2=0;

        while(p1<s.size() && p2<words.size()){
            if(s[p1]==words[p2]) {
                p1++,p2++;
            }
            else p1++;
        }
        if(p2==words.size()) return true;
        return false;
    }
    int numMatchingSubseq(string s, vector<string>& words) {
        int count =0;
        unordered_map<string, bool> mp;

        for (int i = 0; i < words.size(); i++) {
            if (mp.find(words[i]) != mp.end()) {
                if (mp[words[i]]) count++;
            } 
        else {
            bool ok = fun(s, words[i]);
            mp[words[i]] = ok;
            if (ok) count++;
        }
    }
    return count;

    }
};
