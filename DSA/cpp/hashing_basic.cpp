#include<bits/stdc++.h>
using namespace std;

void num_freq(){
    // When this function will be called it will ask for inputs and then calculate the frequnecies using map STL in C++.
    // can also use unordered_map instead map.
    map<int, int> mpp;
    int n;
    cout<<"Input the # inputs you want to give (size of arr): ";
    cin>>n;
    int arr[n];
    cout<<"Now enter all the entries:-"<<endl;
    for(int i=0; i<n; i++){
        cin >> arr[i];
        // pre-computing here itself, same thing
        mpp[arr[i]]++;
    }

    // can iterate through the map and view all the key value pairs.
    cout<<"Here is the frequency of all the values you input."<<endl;
    for(auto i: mpp){
        cout << i.first << " -> " << i.second << endl;
    }

    // number of queries
    int q;
    cout<<"Number of queries to search: ";
    cin >> q;
    while(q--){
        int num;
        cin>>num;
        cout<<mpp[num]<<endl;
    }
}

int main(){
    num_freq();
    string s;
    cout<<"Input string sequence: ";
    cin>>s;
    
    //pre-computation of making the hash
    int hash[26] = {0};
    // here we are considering only lower case characters, if we want to include all the ascii characters then use 256 size array and remove
    // subtracting char 'a' part. 
    for (int i=0; i<s.length(); i++){
        hash[s[i] - 'a']++;
    }

    // number of queries
    int q;
    cout<<"Number of queries to search: ";
    cin>>q;

    while(q--){
        char ch;
        cin >> ch;
        // fetch operation from hash
        cout << hash[ch - 'a'] << endl; 
    }
    return 0;
}
