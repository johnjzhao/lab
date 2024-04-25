#include <iostream>
#include <cstring>
#include <vector>

using namespace std;

long getWays(int n, vector<long>& c){
    vector<long> change(n+1, 0);
    change[0] = 1;
    for (int coin : c) {
        for (int i = coin; i <= n; i++) {
            change[i] += change[i - coin];
        }
    }
    return change[n];
}

int main()
{
	int n = 4;
	vector<long> c{ 1, 2, 3 };
	cout << getWays(n, c);
    cout << endl;
	return 0;
}

