#include<bits/stdc++.h>
using namespace std;

void Merge(vector<int> &arr, int low, int mid, int high){
    vector<int> temp;
    int left = low;
    int right = mid+1;
    while(left<=mid && right<=high){
        if (arr[left]<=arr[right]){
            temp.push_back(arr[left]);
            left++;
        }
        else{
            temp.push_back(arr[right]);
            right++;
        }
    }
    while(left<=mid){
        temp.push_back(arr[left]);
        left++;
    }
    while(right<=high){
        temp.push_back(arr[right]);
        right++;
    }
    for(int i=low; i<=high; i++){
        arr[i] = temp[i-low];
    }
}

void MergeSort(vector<int> &arr, int low, int high){
    if(low >= high)
        return;
    int mid = (high + low)/2;
    MergeSort(arr, low, mid);
    MergeSort(arr, mid+1, high);
    Merge(arr, low, mid, high);
}

int main(){
    int n;
    cout<<"Enter length of array: ";
    cin>>n;
    vector<int> main_arr;
    cout<<"Enter the values: ";
    int num;
    for(int i=0; i<n; i++){
        // int num;
        cin>>num;
        main_arr.push_back(num);
    }
    MergeSort(main_arr, 0, n-1);
    cout<<"The sorted array using merge sort: ";
    for(int i=0; i<n; i++){
        cout<<main_arr[i]<<" ";
    }
    cout<<endl;
    return 0;
}
