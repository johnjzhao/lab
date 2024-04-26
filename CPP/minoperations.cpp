#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <climits>

using namespace std;

int minOperations(vector<int>& arr, int threshold, int d) {
    unordered_map<int, pair<int, int>> dp;
    sort(arr.begin(), arr.end());
    int ans = INT_MAX;
    for (int x : arr) {
        int steps = 0;
        while (true) {
            dp[x].first += 1;
            dp[x].second += steps;
            if (dp[x].first >= threshold) {
                ans = min(ans, dp[x].second);
            }
            if (x == 0) {
                break;
            }
            x /= d;
            steps += 1;
        }
    }
    return ans;
}

int main() {


    int threshold = 2;
    int d = 2;
    vector<int> arr = {64, 30, 25, 33};

    int result = minOperations(arr, threshold, d);

    cout << result << endl;

    return 0;
}
