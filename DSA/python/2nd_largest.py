def second_largest(arr: list) -> int:
    largest = arr[0]
    second_largest = -999999999
    for i in range(len(arr)):
        if arr[i]>largest:
            second_largest = largest
            largest = arr[i]
        elif second_largest < arr[i] and arr[i] < largest:
            second_largest = arr[i]
    return second_largest

def second_smallest(arr: list) -> int:
    smallest = arr[0]
    second_smallest = 999999999
    for i in range(len(arr)):
        if arr[i] < smallest:
            second_smallest = smallest
            smallest = arr[i]
        elif second_smallest > arr[i] and arr[i] > smallest:
            second_smallest = arr[i]
    return second_smallest

def check_if_sorted(arr: list) -> bool:
    for i in range(1, len(arr)):
        if not (arr[i] >= arr[i-1]):
            return False
    return True

def remove_duplicates(arr: list):
# one way of doing it in python    
    # return set(arr)
    i = 0
    j = i+1
    while(j<len(arr)):
        if arr[j] == arr[i]:
            j += 1
        else:
            arr[i+1] = arr[j]
            i += 1
    return arr[:i+1]
        
if __name__  == "__main__":
    n = int(input("Enter the length of the array: "))
    test_arr = list(map(int, input("Enter the values: ").split()))

    # find the 2nd largest
    num1 = second_largest(test_arr)
    num2 = second_smallest(test_arr)
    sorted = check_if_sorted(test_arr)
    if sorted:
        print("The array is sorted.")
    else:
        print("The array is not sorted.")
 
    print(remove_duplicates(test_arr))
    print(f"The 2nd largest number is: {num1}")
    print(f"The 2nd smallest number is: {num2}")
