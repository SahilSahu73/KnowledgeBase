# Brute Force Approach apparently
def rotate_k_left(arr: list, k: int):
    n = len(arr)
    k = k%n
    temp_nums = arr[:k]
    for i in range(k, n):
        arr[i-k] = arr[i]
    arr[n-k:] = temp_nums

def rotate_k_right(arr: list, k: int):
    n = len(arr)
    k = k%n
    temp_nums = arr[n-k:]
    for i in range(n-1, k-1, -1):
        arr[i] = arr[i-k]
    arr[:k] = temp_nums


# Another way of doing is to reverse the array
# This approach has slightly higher TC but is done in constant SC.
def reversal(arr: list): 
    start = 0
    end = len(arr)-1
    while(start<=end):
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1

def rotate_k_left_2(nums: list, k: int):
    # reversal(arr[:k])
    # reversal(arr[k:])
    # reversal(arr)
    k = k%len(nums)
    nums[:] = nums[-k::] + nums[:-k]

def unionn(arr1: list, arr2: list):
    set1 = set(arr1)
    set2 = set(arr2)
    return set1.union(set2)

def list_union(arr1: list, arr2: list):
    i, j = 0, 0
    arr1_len = len(arr1)
    arr2_len = len(arr2)
    temp = []
    while(i<arr1_len and j<arr2_len):
        if arr1[i] <= arr2[j]:
            if len(temp) == 0 or temp[-1] != arr1[i]:
                temp.append(arr1[i])
            i += 1
        else:
            if len(temp) == 0 or temp[-1] != arr2[j]:
                temp.append(arr2[j])
            j += 1

    while(j<arr2_len):
        if len(temp)==0 or temp[-1] != arr2[j]:
            temp.append(arr2[j])
        j += 1

    while(i<arr1_len):
        if len(temp) == 0 or temp[-1] != arr1[i]:
            temp.append(arr1[i])
        i += 1

    return temp

def intersection(arr1: list, arr2: list):
    i, j = 0, 0
    n1 = len(arr1)
    n2 = len(arr2)
    intersec = []
    while(i<n1 and j<n2):
        if arr1[i] == arr2[j]:
            intersec.append(arr1[i])
            i += 1
            j += 1
        elif arr1[i] < arr2[j]:
            i += 1
        elif arr1[i] > arr2[j]:
            j += 1
    return intersec


if __name__ == "__main__":
    # k = int(input("Enter the # of rotations (k): "))
    test_arr = list(map(int, input("Enter the values: ").split()))
    test_arr2 = list(map(int, input("Enter the values: ").split()))

    # rotate_k_left(test_arr, k)
    # rotate_k_left_2(test_arr, k)
    
    print(intersection(test_arr, test_arr2))
