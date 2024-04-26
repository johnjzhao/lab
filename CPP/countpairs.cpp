#include <bits/stdc++.h>
#include <iostream>
#include <vector>
#include <unordered_map>

using namespace std;

int countPairs(vector<int>& arr) {
    auto po2 = [](int x) { return x > 0 && !(x & (x - 1)); };
    unordered_map<int, int> d;
    for (int x : arr) {
        d[x]++;
    }
    vector<pair<int, int>> d_vec(d.begin(), d.end());
    int ans = 0;
    for (int i = 0; i < d_vec.size(); i++) {
        int a = d_vec[i].first;
        int a_cnt = d_vec[i].second;
        for (int j = i; j < d_vec.size(); j++) {
            int b = d_vec[j].first;
            int b_cnt = d_vec[j].second;
            if (po2(a & b)) {
                if (a == b) {
                    ans += (a_cnt * (a_cnt - 1)) / 2;
                } else {
                    ans += a_cnt * b_cnt;
                }
            }
        }
    }
    return ans;
}

int main() {

    vector<int> arr = {10, 7, 2, 8, 3};

    int result = countPairs(arr);

    cout << result << endl;

    return 0;
}
