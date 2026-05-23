COUNT = 0

def merge_sort_count(low, high, arr):
    if low >= high:
        return
    mid = (low+high)//2
    merge_sort_count(low, mid, arr)
    merge_sort_count(mid+1, high, arr)
    merge(low, mid, high, arr)


if __name__ == "__main__":
    n = int(input("Enter length of array: "))
    test_arr = list(map(int, input("Enter the array elements: ").split()))

    # function call
    merge_sort_count(0, n-1, test_arr)
    print(test_arr)
