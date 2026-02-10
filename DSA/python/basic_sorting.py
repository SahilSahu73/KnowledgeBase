def selection(arr: list):
    n = len(arr)
    for i in range(n):
        minimum = i
        for j in range(i, n):
            if arr[j] < arr[minimum]:
                minimum = j
        arr[minimum], arr[i] = arr[i], arr[minimum]
    return arr


def bubble(arr: list):
    n = len(arr)
    for i in range(n):
        swap_bool: bool = False
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swap_bool = True
        print("Iteration number: ", i)
        if not swap_bool:
            break
    return arr


def insertion(arr: list):
    n = len(arr)
    for i in range(n):
        j = i
        while(j>0 and arr[j-1]>arr[j]):
            arr[j-1], arr[j] = arr[j], arr[j-1]
            j -= 1
    return arr


def merge_sort(arr, low, high):
    mid = (low+high)//2
    if low >= high:
        return
    
    merge_sort(arr, low, mid)
    merge_sort(arr, mid+1, high)
    merge(arr, low, mid, high)

def merge(arr: list, low: int, mid: int, high: int):
    temp_arr = []
    left = low
    right = mid+1
    
    while(left<=mid and right<=high):
        if arr[left] <= arr[right]:
            temp_arr.append(arr[left])
            left+=1
        else:
            temp_arr.append(arr[right])
            right+=1

    while(right<=high):
        temp_arr.append(arr[right])
        right+=1

    while(left<=mid):
        temp_arr.append(arr[left])
        left+=1

    for i in range(low, high+1):
        arr[i] = temp_arr[i-low]


def quick_sort(arr: list, low: int, high: int):
    if low<high:
        partition_idx = quick(arr, low, high)
        quick_sort(arr, low, partition_idx-1)
        quick_sort(arr, partition_idx+1, high)

def quick(arr: list, low: int, high: int):
    pivot = arr[low]
    i = low
    j = high
    while(j>i):
        while(arr[i]<=pivot and i<=high-1):
            i+=1
        while(arr[j]>pivot and j>=low+1):
            j-=1

        if i<j:
            arr[j], arr[i] = arr[i], arr[j]
    
    arr[low], arr[j] = arr[j], arr[low]
    return j


if __name__ == "__main__":
    n = int(input("Enter length of array: "))
    test_arr = list(map(int, input("Enter the array elements: ").split()))

    # function call
    # sol = insertion(test_arr)
    quick_sort(test_arr, 0, n-1)
    print("The sorted array is: ")
    # print(sol)
    print(test_arr)
