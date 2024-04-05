#include<string>
#include<iostream>
#include<algorithm>

using namespace std;

bool arePermutation(string str1, string str2){
    int n1 = str1.length();
    int n2 = str2.length();

    if (n1 != n2)
        return false;
    sort(str1.begin(), str1.end());
    sort(str2.begin(), str2.end());
    for (int i = 0; i < str1.length(); i++)
        if (str1[i] != str2[i])
            return false;
    return true;
}



int main() {
// Using sort Method
    cout << "Using sort method:" << endl;
    string str1 = "testest";
    string str2 = "estxest";
    if(arePermutation(str1, str2))
      cout << str1 <<" and " << str2 << " are permutation of each other" << endl;
    else
      cout << str1 <<" and " << str2 << " are not permutation of each other" << endl;
    str1 = "hello";
    str2 = "oellh";
    if(arePermutation(str1, str2))
      cout << str1 <<" and " << str2 << " are permutation of each other" << endl;
    else
      cout << str1 <<" and " << str2 << " are not permutation of each other" << endl;
}

