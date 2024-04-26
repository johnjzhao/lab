#include <bits/stdc++.h>
#include <iostream>
#include <vector>

using namespace std;

int maxPairs(vector<int>& skillLevel, int minDiff) {
    sort(skillLevel.begin(), skillLevel.end());
    int n = skillLevel.size();
    int i = 0;
    vector<int> x;
    for (int j = 0; j < n / 2; j++) {
        while (i < n && skillLevel[i] - skillLevel[j] < minDiff) {
            i++;
        }
        if (i >= n) {
            break;
        }
        x.push_back(i);
    }
    x.resize(n / 2);
    int ans = 0;
    int k = n - 1;
    for (int y = x.size() - 1; y >= 0; y--) {
        if (x[y] <= k) {
            ans++;
            k--;
        }
    }
    return ans;
}

int main() {

    vector<int> skillLevel = {3, 4, 5, 2, 1, 1};
    int minDiff = 3;

    int result = maxPairs(skillLevel, minDiff);

    cout << result << endl;

    return 0;
}
