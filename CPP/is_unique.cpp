#include<string>
#include<vector>
#include<iostream>
#include<bitset>
#include<algorithm>

using namespace std;

bool isUniqueChars(const string &str){
    if ( str.length() > 128){
	return false;
    }
    vector <bool> charset(128);
    for (int i=0; i<str.length(); i++){
	int val = str[i];
	if (charset[val]){
	    return false;
	}
	charset[val] = true;
    }
    return true;
}

int main(){
    vector<string> words = {"abcde", "hello", "apple", "kite", "padle", "johnz", "rubber"};
    for (auto word : words)
    {
        cout << word << string(" :") << boolalpha << isUniqueChars(word) << endl;
    }
    return 0;
}

