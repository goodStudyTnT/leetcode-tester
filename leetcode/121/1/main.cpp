#include "./solution.h"

void test0() {
    string key[2] = {"foo", "foo"};
    string value[2] = {"bar", "bar2"};
    int timestamp[2] = {1, 4};
    string key0[4] = {"foo", "foo", "foo", "foo"};
    int timestamp0[4] = {1, 3, 4, 5};
    TimeMap *obj = new TimeMap();
    obj->set(key[0], value[0], timestamp[0]);
    compare_result(0, obj->get(key0[0], timestamp0[0]), string("bar"));
    compare_result(0, obj->get(key0[1], timestamp0[1]), string("bar"));
    obj->set(key[1], value[1], timestamp[1]);
    compare_result(0, obj->get(key0[2], timestamp0[2]), string("bar2"));
    compare_result(0, obj->get(key0[3], timestamp0[3]), string("bar2"));
}

int main() {
    test0();
    return 0;
}
