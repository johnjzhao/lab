#include<iostream>
#include<vector>

using namespace std;

int getCharIndex(char c){
    int idx = -1;
    if (c >= 'a' && c <= 'z'){
        idx = c - 'a';
    } else if (c >= 'A' && c <= 'Z'){
        idx = c - 'A';
    }
    return idx;
}

void countFrequency(const string & str, int *frequency){
    int idx;
    for (const char & c : str){
        idx = getCharIndex(c);
        if (idx != -1)
            ++frequency[idx];
    }
}

bool isPermutationOfPallindrome(const string & str){
    int frequency[26] = { 0 };
    countFrequency(str, frequency);

    bool oddAppeared = false;
    for (int i = 0; i < 26; i++){
        if ( frequency[i] % 2 && oddAppeared) {
            return false;
        } else if (frequency[i] % 2 && !oddAppeared){
            oddAppeared = true;
        }
    }
    return true;
}

int main()
{
    vector<string> patterns{
        "",
        "a",
        "ab",
        "Tact Coa",
        "A big Cat",
        "Aba cbc",
        "Rats live on no evil st",
        "Rats live on no evil star"
        };
    for (auto& pattern : patterns)
    {
        cout<<"[Sample:]"<<pattern<<endl;
        cout<<isPermutationOfPallindrome(pattern)<<endl;
    }
    return 0;
}
