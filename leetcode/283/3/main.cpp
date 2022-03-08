#include "./solution.h"


int main() {

    Solution sol = Solution();
vector<int>& nums[2]=6,4,3,2,7,6,2,2,2,1,1,3,3,3
    for (int i = 0; i < 2; i++) {
        vector<int> res = sol.replaceNonCoprimes(nums[i]);
cout << (res == [['[12,7,6]'], ['[2,1,1,3]']][i]) << endl;
    }
}