// test
#if __has_include("../../utils/cpp/help.h")
#include "../../utils/cpp/help.h"
#endif

/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
   public:
    TreeNode* createBinaryTree(vector<vector<int>>& descriptions) {
        map<int, TreeNode*> M;

        int n = descriptions.size();

        set<int> have_fa;
        for (int i = 0; i < n; i++) {
            int p = descriptions[i][0], c = descriptions[i][1], is_left = descriptions[i][2];
            have_fa.insert(c);
            TreeNode *par, *chi;
            if (M.count(p)) {
                par = M[p];
            } else {
                par = new TreeNode(p);
                M[p] = par;
            }

            if (M.count(c)) {
                chi = M[c];
            } else {
                chi = new TreeNode(c);
                M[c] = chi;
            }
            if (is_left) {
                par->left = chi;
            } else {
                par->right = chi;
            }
        }

        for (int i = 0; i < n; i++) {
            int p = descriptions[i][0];
            if (have_fa.count(p)) continue;
            cout << p << endl;
            return M[p];
        }
        return NULL;
    }
};