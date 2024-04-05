#include<iostream>
#include<cstring>

using namespace std;

void urlify(char *str, int len){
    int numSpaces = 0;
    int i = 0, j = 0;
    for (i = 0; i < len; i++){
        if (str[i] == ' ')
            numSpaces++;
    }

    int extLen = len + 2 * numSpaces;
    i = extLen - 1;
    for (j = len - 1; j >= 0; j--){
        if (str[j] != ' '){
            str[i--] = str[j];
        } else {
            str[i--] = '0';
            str[i--] = '2';
            str[i--] = '%';
        }
    }
}

int main()
{
    char str[] = "Mr John Zhao      ";                       //String with extended length ( true length + 2* spaces)
    cout << "Actual string   : " << str << std::endl;
    urlify(str, 12);                                        //Length of "Mr John Zhao" = 12
    cout << "URLified string : " << str << std::endl;
    return 0;
}
