#include<iostream>
#include<vector>
#include<sstream>
#include<algorithm>

using namespace std;

long countMax(vector<string> upRight) {
    int rows = 0, cols = 0;

    for (string coord : upRight) {
        istringstream iss(coord);
        int r, c;
        iss >> r >> c;
        rows = max(rows, r);
        cols = max(cols, c);
    }

    vector<vector<int>> grid(rows + 1, vector<int>(cols + 1, 0));

    for (string coord : upRight) {
        istringstream iss(coord);
        int r, c;
        iss >> r >> c;
        for (int i = 1; i <= r; i++) {
            for (int j = 1; j <= c; j++) {
                grid[i][j] += 1;
                //cout<<grid[i][j]<<"\t";
            }
            //cout<<endl;
        }
        //cout<<endl;
    }

    int max_elem = 0;
    int my_elem = 0;
    for (vector<int> row : grid) {
        my_elem = *max_element(row.begin(), row.end());
        if (my_elem > max_elem)
            max_elem = my_elem;
    }
    cout<<"Max Elements: "<<max_elem<<endl;

    int count_max = 0;
    for (vector<int> row : grid) {
        count_max += count(row.begin(), row.end(), max_elem);
    }


    return count_max;
}

int main() {
    vector<string> upRight = {"1 4", "2 3", "4 1"};
    int result = countMax(upRight);
    cout <<"Count Occurences: "<< result << endl;
    return 0;
}
