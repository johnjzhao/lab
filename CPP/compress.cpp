#include<iostream>
#include<string>

using namespace std;

string compress(string str){
    size_t org_length = str.length();
    if (org_length < 2){
        return str;
    }
    string out{""};
    int count = 1;
    for (size_t i = 1; i < org_length; i++){
        if (str[i-1] == str[i]){
            ++count;
        } else {
            out += str[i-1];
            out += to_string(count);
            count = 1;
        }
        if (out.length() >= org_length){
            return str;
        }
    }
    out += str[org_length-1];
    out += to_string(count);
    if (out.length() >= org_length){
        return str;
    }
    return out;
}

int main(){
    string str, out;
    cout << "Enter a string:\n";
    cin >> str;
    out = compress(str);
    if (str.compare(out)) {
        cout << str << " can be compressed to " << out << endl;
    } else {
        cout << str << " can not be compressed\n";
    }
    return 0;
}
