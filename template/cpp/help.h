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
        this->left = this->right = NULL;
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
    ListNode(vector<int> x) {
        assert(x.size() > 0);
        this->next = NULL;
        this->val = x[0];
        ListNode *now = this;
        for (int i = 1; i < x.size(); i++) {
            int val = x[i];
            ListNode *nxt = new ListNode(val);
            now->next = nxt;
            now = nxt;
        }
    }
    vector<int> to_vector() {
        ListNode *now = this;
        vector<int> ans;
        while (now != NULL) {
            int val = now->val;
            ans.push_back(val);
            now = now->next;
        }
        return ans;
    }
};

/*
    调试输出
*/
template <typename A, typename B>
string to_string(pair<A, B> p);

template <typename A, typename B, typename C>
string to_string(tuple<A, B, C> p);

template <typename A, typename B, typename C, typename D>
string to_string(tuple<A, B, C, D> p);

string to_string(const string &s) {
    return '"' + s + '"';
}

string to_string(const char *s) {
    return to_string((string)s);
}

string to_string(bool b) {
    return (b ? "true" : "false");
}

string to_string(vector<bool> v) {
    bool first = true;
    string res = "{";
    for (int i = 0; i < static_cast<int>(v.size()); i++) {
        if (!first) {
            res += ", ";
        }
        first = false;
        res += to_string(v[i]);
    }
    res += "}";
    return res;
}

template <size_t N>
string to_string(bitset<N> v) {
    string res = "";
    for (size_t i = 0; i < N; i++) {
        res += static_cast<char>('0' + v[i]);
    }
    return res;
}

template <typename A>
string to_string(A v) {
    bool first = true;
    string res = "{";
    for (const auto &x : v) {
        if (!first) {
            res += ", ";
        }
        first = false;
        res += to_string(x);
    }
    res += "}";
    return res;
}

template <typename A, typename B>
string to_string(pair<A, B> p) {
    return "(" + to_string(p.first) + ", " + to_string(p.second) + ")";
}

template <typename A, typename B, typename C>
string to_string(tuple<A, B, C> p) {
    return "(" + to_string(get<0>(p)) + ", " + to_string(get<1>(p)) + ", " + to_string(get<2>(p)) + ")";
}

template <typename A, typename B, typename C, typename D>
string to_string(tuple<A, B, C, D> p) {
    return "(" + to_string(get<0>(p)) + ", " + to_string(get<1>(p)) + ", " + to_string(get<2>(p)) + ", " + to_string(get<3>(p)) + ")";
}

void debug_out() {
    cerr << endl;
}

template <typename Head, typename... Tail>
void debug_out(Head H, Tail... T) {
    cerr << " " << to_string(H);
    debug_out(T...);
}

#define debug(...) cerr << "[" << #__VA_ARGS__ << "]:", debug_out(__VA_ARGS__)

// compare_result 实现
template <typename T>
void compare_result(string sample_idx, T &my_ans, T &result) {
    bool equal = (my_ans == result);
    debug(my_ans);
    debug(result);
    if (!equal) {
        cerr << "[fail!] 样例 " << sample_idx << " 错误! 请勿提交!" << endl;
    } else {
        cerr << "样例 " << sample_idx << " 通过测试!" << endl;
    }
}

void compare_result(string sample_idx, TreeNode *my_ans, TreeNode *result) {
    vector<int> a = my_ans->bfs_order();
    vector<int> b = result->bfs_order();
    compare_result(sample_idx, a, b);
};

void compare_result(string sample_idx, ListNode *my_ans, ListNode *result) {
    vector<int> a = my_ans->to_vector();
    vector<int> b = result->to_vector();
    compare_result(sample_idx, a, b);
}