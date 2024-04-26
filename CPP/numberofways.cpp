#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

void dfs(int x, int d, vector<vector<int>>& adj, vector<int>& dist) {
    dist[x] = d;
    for (int y : adj[x]) {
        if (dist[y] == -1) {
            dfs(y, d + 1, adj, dist);
        }
    }
}

int numberOfWays(vector<vector<int>>& roads) {
    int n = roads.size() + 1;
    vector<vector<int>> adj(n);
    for (auto& road : roads) {
        adj[road[0] - 1].push_back(road[1] - 1);
        adj[road[1] - 1].push_back(road[0] - 1);
    }
    int ans = 0;

    for (int i = 0; i < n - 2; i++) {
        for (int j = i + 1; j < n - 1; j++) {
            for (int k = j + 1; k < n; k++) {
                vector<int> dist(n, -1);
                dfs(i, 0, adj, dist);
                if (dist[j] != dist[k]) {
                    continue;
                }
                dist.assign(n, -1);
                dfs(j, 0, adj, dist);
                if (dist[i] == dist[k]) {
                    ans++;
                }
            }
        }
    }
    return ans;
}

int main() {


    vector<vector<int>> roads = {{1, 2}, {2, 5}, {3, 4}, {4, 5}, {5, 6},{7, 6}};
    int result = numberOfWays(roads);

    cout << result << endl;

    return 0;
}
