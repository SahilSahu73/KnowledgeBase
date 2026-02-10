#include<bits/stdc++.h>
using namespace std;

// simple method
bool palindrome(string s){
    int i=0, j=s.length()-1;
    while(i<j){
        if (!isalnum(s[i]))
            i++;
        else if (!isalnum(s[j]))
            j--;
        else if (tolower(s[i]) != tolower(s[j]))
            return false;
        else{
            i++;
            j--;
        }
    }
    return true;
}

// Recursion method
bool isPalindrome(int i, string& s){
    if (i>=s.size()/2) return true;
    if (s[i] != s[s.size()-i-1]) return false;
    return isPalindrome(i+1, s);
}

// clean unncessary characters and then compare.
bool clean_palindrome(string& s){
    string cleaned;
    for(char ch : s){
        if (isalnum(ch))
            cleaned += tolower(ch);
    }
    int i=0, j=cleaned.length()-1;
    while(i<j){
        if (cleaned[i] != cleaned[j])
            return false;
        i++;
        j--;
    }
    return true;
}


int main(){
    string str = "ABCDCBA";
    bool ans = isPalindrome(0, str);
    bool ans2 = palindrome(str);

    if (ans == true and ans2==true) {
        cout << "Palindrome"<<endl;
    } 
    else {
        cout << "Not Palindrome"<<endl;
    }
    return 0;
}
