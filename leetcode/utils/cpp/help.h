#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(vector<int> v) {
        // bfs 序构建整颗树
        assert(v.size() > 0);
        int son_idx = 1;
        queue<TreeNode *> Q;
        this->val = v[0];
        Q.push(this);
        while (!Q.empty()) {
            TreeNode *now = Q.front();
            Q.pop();
            int left_son_val = 0, right_son_val = 0;
            if (son_idx < v.size()) {
                left_son_val = v[son_idx];
            }
            if (son_idx + 1 < v.size()) {
                right_son_val = v[son_idx + 1];
            }

            son_idx += 2;
            if (left_son_val != 0) {
                TreeNode *tmp = new TreeNode(left_son_val);
                now->left = tmp;
                Q.push(tmp);
            }
            if (right_son_val != 0) {
                TreeNode *tmp = new TreeNode(right_son_val);
                now->right = tmp;
                Q.push(tmp);
            }
        }
    }
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}

    vector<int> bfs_order() {
        vector<int> res;
        res.push_back(this->val);
        queue<TreeNode *> Q;
        Q.push(this);
        while (!Q.empty()) {
            TreeNode *now = Q.front();
            Q.pop();
            // cout << now->val << endl;
            if (now->left != NULL) {
                Q.push(now->left);
                res.push_back(now->left->val);
            } else {
                res.push_back(0);
            }
            if (now->right != NULL) {
                Q.push(now->right);
                res.push_back(now->right->val);
            } else {
                res.push_back(0);
            }
        }
        // 去掉末尾 0
        int idx = res.size() - 1;
        while (idx >= 0 && res[idx] == 0) idx--;
        res.resize(idx + 1);
        return res;
    }
};

struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {}
};