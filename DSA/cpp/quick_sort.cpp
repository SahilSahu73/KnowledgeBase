#include<bits/stdc++.h>
using namespace std;

int quick(vector<int> &arr, int low, int high){
  int pivot = arr[low];
  int i = low;
  int j = high;
  while(i<j){
    while(arr[i]<=pivot && i<=high-1){
      i++;
    }
    while(arr[j]>pivot && j>=low+1){
      j--;
    }
    if (i<j){
      int temp = arr[i];
      arr[i] = arr[j];
      arr[j] = temp;
    }
  }
  int temp2 = arr[j];
  arr[j] = arr[low];
  arr[low] = temp2;
  return j;
}

void quick_sort(vector<int> &arr, int low, int high){
  if (low<high){
    int partition_idx = quick(arr, low, high);
    quick_sort(arr, low, partition_idx-1);
    quick_sort(arr, partition_idx+1, high);
  }
}


int merge_sort(vector<int> &arr, int low, int high){
  int mid = (low+high)/2;
  if (low<=high){
    merge_sort(arr, low, mid);
    merge_sort(arr, mid+1, high);
    merge(arr, low, mid, high);
  }
}


int main(){
  int n;
  cout<<"Enter array length: ";
  cin>>n;
  vector<int> test_arr;
  cout<<"Enter values: ";
  int num;
  for(int i=0; i<n; i++){
    cin>>num;
    test_arr.push_back(num);
  }
  
  // call quick sort
  quick_sort(test_arr, 0, n-1);
  cout<<"The sorted array: ";
  for(int i=0; i<n; i++){
    cout<<test_arr[i]<<" ";
  }
  cout<<endl;
  return 0;
}
