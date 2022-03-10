#include "./solution.h"

int main() {
	Solution sol = Solution();
	string res[2] = {"abb", "aabaa"};
	int a[2] = {1, 4};
	int b[2] = {2, 1};
    for (int i = 0; i < 2; i++) {
		string my_ans = sol.strWithout3a3b(a[i], b[i]);
		compare_result(i, my_ans, res[i]);
    }
    return 0;
}