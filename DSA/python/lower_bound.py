# Lower Bound
def lower_bound(arr: list, target: int, n: int):
    low, high = 0, n-1
    ans = n
    while(low <= high):
        mid = (low+high)//2
        if arr[mid] >= target:
            ans = mid
            high = mid-1
        else:
            low = mid+1
    return ans


def upper_bound(arr, target, n):
    low, high = 0, n-1
    ans = n
    while(low <= high):
        mid = (low+high)//2
        if arr[mid] > target:
            ans = mid
            high = mid-1
        else:
            low = mid+1
    return ans


if __name__ == "__main__":
    test_arr = list(map(int, input("Enter a list of numbers (sorted): ").split()))
    target = int(input("x: "))
    n = len(test_arr)
    lb = lower_bound(test_arr, target, n)
    ub = upper_bound(test_arr, target, n) - 1
    print(f"First and Last occurence of x in this array: ({lb}, {ub}) ")
