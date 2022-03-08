#include "./solution.h"

int main() {
	Solution sol = Solution();
	TreeNode* res[2] = {{50,20,80,15,17,19}, {1,2,null,null,3,4}};
	vector<vector<int>> descriptions[2] = {{{20,15,1},{20,17,0},{50,20,1},{50,80,0},{80,19,1}}, {{1,2,1},{2,3,0},{3,4,1}}};
    for (int i = 0; i < 2; i++) {
		TreeNode* my_ans = sol.createBinaryTree(descriptions[i]);
		compare_result(my_ans, res[i]);
    }
    return 0;
}