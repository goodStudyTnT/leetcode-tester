#include "./solution.h"

int main() {
	Solution sol = Solution();
	int res[2] = {11, 17};
	vector<int> days[2] = {{1,4,6,7,8,20}, {1,2,3,4,5,6,7,8,9,10,30,31}};
	vector<int> costs[2] = {{2,7,15}, {2,7,15}};
    for (int i = 0; i < 2; i++) {
		int my_ans = sol.mincostTickets(days[i], costs[i]);
		compare_result(i, my_ans, res[i]);
    }
    return 0;
}