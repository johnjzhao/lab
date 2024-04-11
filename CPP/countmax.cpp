#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm>

using namespace std;

int countMax(vector<string> upRight) {
    int rows = 0, cols = 0;

    // Process each coordinate and determine the final size of the grid
    for (const auto& coord : upRight) {
        int r, c;
        stringstream ss(coord);
        ss >> r >> c;
        rows = max(rows, r);
        cols = max(cols, c);
    }

    // Create the grid and fill it with zeros
    vector<vector<int>> grid(rows + 1, vector<int>(cols + 1, 0));
    cout<<grid<<endl;

    // Update the grid based on the coordinates
    for (const auto& coord : upRight) {
        int r, c;
        stringstream ss(coord);
        ss >> r >> c;
        for (int i = 1; i <= r; i++) {
            for (int j = 1; j <= c; j++) {
                grid[i][j]++;
            }
        }
    }

    // Find the maximal element in the grid
    int max_ele = *max_element(grid[0].begin(), grid[0].end());
    int count_max = 0;
    for (const auto& row : grid) {
        count_max += count(row.begin(), row.end(), max_ele);
    }

    return count_max;
}

int main() {
    vector<string> upRight = {"1 4", "2 3", "4 1"};
    int result = countMax(upRight);
    cout << result << endl;
    return 0;
}

