#include <bits/stdc++.h>
#include <iostream>
#include <vector>

using namespace std;

class Result {
public:
    static int getMaxValue(vector<int>& arr) {
        arr[0] -= 1;
        sort(arr.begin(), arr.end());

        for (int i = 1; i < arr.size(); i++) {
            if (arr[i] > arr[i - 1] + 1) {
                arr[i] = arr[i - 1] + 1;
            }
        }

        return *max_element(arr.begin(), arr.end());
    }
};

int main() {
    //int arr_count = 4;
    //cin >> arr_count;
    vector<int> arr = {3, 1, 3, 4};
    //vector<int> arr(arr_count);

   // for (int i = 0; i < arr_count; i++) {
   //     cin >> arr[i];
    //}

    int result = Result::getMaxValue(arr);

    cout << result << endl;

    return 0;
}
