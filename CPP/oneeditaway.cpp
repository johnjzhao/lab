#include<iostream>
#include<string>
#include<cmath>

using namespace std;

bool oneEditAway(const string & str1, const string & str2){
    if (abs(int(str1.length()) - int(str2.length())) > 1){
        return false;
    }

    int len1 = str1.length();
    int len2 = str2.length();
    string shorter = len1 < len2 ? str1 : str2;
    string longer = len1 < len2 ? str2 : str1;

    unsigned int i = 0, j = 0;
    bool mismatchFound = false;
    while ( i < shorter.length() && j < longer.length()){
        if (shorter[i] != longer[j]){
            if (mismatchFound){
                return false;
            }
            mismatchFound = true;
            if (len1 == len2){
                i++;
            }
        } else {
            ++i;
        }
        ++j;
    }
    return true;
}

void translate(bool result, const string str1, const string str2){
    if (result == true){
        cout << str1 << " and " << str2 << " are one edit away\n";
    } else {
        cout << str1 << " and " << str2 << " are not one edit away\n";
    }
}
       
int main(){
    translate ( oneEditAway("pale", "ple"), "pale", "ple" );
    translate ( oneEditAway("pales", "pale"), "pales", "pale" );
    translate ( oneEditAway("pale", "pales"), "pale", "pales" );
    translate ( oneEditAway("pale", "bale"), "pale", "bale" );
    translate ( oneEditAway("pale", "bake"), "pale", "bake" );
    return 0;
}
