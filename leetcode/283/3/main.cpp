#include "./solution.h"

int main() {
	Solution sol = Solution();
	vector<int> res[2] = {{12,7,6}, {2,1,1,3}};
	vector<int> nums[2] = {{, {};
    for (int i = 0; i < 2; i++) {
		vector<int> my_ans = sol.replaceNonCoprimes(nums[i]);
		compare_result(i, my_ans, res[i]);
    }
    return 0;
}