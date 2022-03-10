#include "./solution.h"

int main() {
	Solution sol = Solution();
	int res[1] = {12};
	vector<int> nums[1] = {{2,1,3}};
    for (int i = 0; i < 1; i++) {
		int my_ans = sol.countTriplets(nums[i]);
		compare_result(i, my_ans, res[i]);
    }
    return 0;
}