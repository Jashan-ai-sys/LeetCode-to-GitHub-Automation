/*
 * Problem: 680. Valid Palindrome II
 * Difficulty: Easy
 * URL: https://leetcode.com/problems/valid-palindrome-ii/
 * Topics: Two Pointers, String, Greedy
 * Runtime: 7 ms
 * Memory: 26.8 MB
 * Date: 2026-02-07
*/
class Solution {
public:
    bool ispalindrome(int left,int right,string s){
        while(left<=right){
            if(s[left]==s[right]){
            left++;
            right--;
            }
            else
            return false;
        }
        return true;
    }
    bool validPalindrome(string s) {
        int n=s.size();
        int low=0;
        int high=n-1;
        while(low<=high){
            if(s[low]==s[high]){
            low++;
            high--;
            }
            else{
                return (ispalindrome(low+1,high,s)||ispalindrome(low,high-1,s));
            }

        }
        return true;
        
    }
};
