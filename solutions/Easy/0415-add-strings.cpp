/*
 * Problem: 415. Add Strings
 * Difficulty: Easy
 * URL: https://leetcode.com/problems/add-strings/
 * Topics: Math, String, Simulation
 * Runtime: 27 ms
 * Memory: 58.7 MB
 * Date: 2026-02-07
*/
class Solution {
public:
    string addStrings(string num1, string num2) {
        int i=num1.length()-1;
        int j=num2.length()-1;
        int sum=0;
        string ans="";
       int carry=0;
        while((i>=0||j>=0)||carry)
{
            sum=carry;
            if(i>=0){
                sum+=num1[i]-'0';
                i--;
            }
            if(j>=0){
                sum+=num2[j]-'0';
                j--;
            }
            ans=char(sum%10+'0')+ans;
            carry=sum/10;
        }      
        return ans;
        
    }
};
