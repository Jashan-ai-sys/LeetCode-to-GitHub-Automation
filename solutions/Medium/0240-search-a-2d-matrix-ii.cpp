/*
 * Problem: 240. Search a 2D Matrix II
 * Difficulty: Medium
 * URL: https://leetcode.com/problems/search-a-2d-matrix-ii/
 * Topics: Array, Binary Search, Divide and Conquer, Matrix
 * Runtime: 55 ms
 * Memory: 18.6 MB
 * Date: 2026-02-07
*/
class Solution {
public:
    
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int n=matrix.size();
        int m=matrix[0].size();
        int row=0;
        int col=m-1;
        while(row<n&&col>=0){
            if(matrix[row][col]==target)
            return true;
            else if(matrix[row][col]>target)
            col--;
            else{
                row++;
            }
        }
        return false;
    }
};
