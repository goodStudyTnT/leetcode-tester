#include "./solution.h"

int main() {
	Solution sol = Solution();
	long long res[2] = {5, 25};
	vector<int> nums[2] = {{1,4,25,10,25}, {5,6}};
	int k[2] = {2, 6};
    for (int i = 0; i < 2; i++) {
		long long my_ans = sol.minimalKSum(nums[i], k[i]);
		compare_result(i, my_ans, res[i]);
    }
    return 0;
}