// test
#if __has_include("../../utils/cpp/help.h")
#include "../../utils/cpp/help.h"
#endif

class TimeMap {
   public:
    unordered_map<string, vector<pair<int, string>>> m;
    TimeMap() {
    }

    void set(string key, string value, int timestamp) {
        m[key].emplace_back(timestamp, value);
    }

    string get(string key, int timestamp) {
        auto &pairs = m[key];
        // 使用一个大于所有 value 的字符串，以确保在 pairs 中含有 timestamp 的情况下也返回大于 timestamp 的位置
        pair<int, string> p = {timestamp, string({127})};
        auto i = upper_bound(pairs.begin(), pairs.end(), p);
        if (i != pairs.begin()) {
            return (i - 1)->second;
        }
        return "";
    }
};

/**
 * Your TimeMap object will be instantiated and called as such:
 * TimeMap* obj = new TimeMap();
 * obj->set(key,value,timestamp);
 * string param_2 = obj->get(key,timestamp);
 */