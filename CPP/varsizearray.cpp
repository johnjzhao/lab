#include<iostream>
#include<vector>
#include<sstream>

using namespace std;

int main(){
    int x, y, s =0;
    cin >> x >> y;

    int* arr[x];
    while(x--){
        int num;
        cin >> num;

        arr[s] = new int[num];

        for(int i=0; i<num;i++)
            cin>>arr[s][i];

        s++;
    }

    while(y--){
        int a,q;
        cin>>a>>q;

        cout<<arr[a][q]<<endl;

    return 0;


int main(){
    int n, q;
    cin >> n >> q;
    cin.ignore();
    vector<vector<int>> a(n);

    for (int i = 0; i < n; i++){
        string line;
        getline(cin, line);
        istringstream ss(line);

        int k_size, k_item;
        ss >> k_size;
        vector<int> k(k_size, 0);

        for (int j = 0; j < k_size; j++){
            ss >> k_item;
            k[j] = k_item;
        }

        a[i] = k;
    }

    for (int i = 0; i < q; i++){
        string query;
        getline(cin, query);
        istringstream ss(query);

        int x, y;
        ss >> x >> y;
        cout << a[x][y] << endl;
    }

    return 0;
}


