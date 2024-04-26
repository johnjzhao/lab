#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <climits>

using namespace std;

int renameFile(string newName, string oldName) {
    int n = newName.length();
    int m = oldName.length();
    vector<int> dp(m + 1, 1);
    for (int i = 1; i <= n; i++) {
        vector<int> dpp(m + 1, 0);
        for (int j = i; j <= m; j++) {
            dpp[j] = dpp[j - 1];
            if (newName[i - 1] == oldName[j - 1]) {
                dpp[j] += dp[j - 1];
            }
        }
        dp = dpp;
    }
    return dp[m] % (int)(1e9 + 7);
}

int main() {

    string newName = "ccc";
    string oldName = "cccc";

    int result = renameFile(newName, oldName);

    cout << result << endl;

    return 0;
}
