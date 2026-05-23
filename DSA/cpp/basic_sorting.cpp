#include<bits/stdc++.h>
using namespace std;

void selection_sort(int arr[], int n){
    for(int i=0; i<n-1; i++){
        int minimum = i;
        for(int j=i; j<n; j++){
            if (arr[j] < arr[minimum]){
                minimum = j;
            }
        }
        int temp = arr[minimum];
        arr[minimum] = arr[i];
        arr[i] = temp;
    }
}

void bubble_sort(int arr[], int n){
    for(int i=0; i<n; i++){
        int swap_bool = 0;
        for(int j=0; j<n-i-1; j++){
            if(arr[j] > arr[j+1]){
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
                swap_bool = 1;
            }
        }
        cout<<"Iteration of i: "<<i<<endl;
        if(swap_bool==0)
            break;
    }
}

void insertion_sort(int arr[], int n){
    for(int i=0; i<n; i++){
        int j = i;
        while(j>0 && arr[j-1]>arr[j]){
            int temp = arr[j];
            arr[j] = arr[j-1];
            arr[j-1] = temp;
            j--;
        }
    }
}

int main(){
    int n;
    cout<<"Enter length of array: ";
    cin>>n;
    int main_arr[n];
    cout<<"Enter the values: ";
    for(int i=0; i<n; i++){
        cin>>main_arr[i];
    }
    insertion_sort(main_arr, n);
    cout<<"The sorted array: ";
    for(int i=0; i<n; i++){
        cout<<main_arr[i]<<" ";
    }
    cout<<endl;
    return 0;
}
