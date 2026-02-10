def next_permutation(nums):
    n = len(nums)
    idx = -1
    for i in range(n-2, -1, -1):
        if nums[i] < nums[i+1]:
            idx = i
            break

    if idx == -1:
        nums[:] = nums[::-1]
        return nums

    for i in range(n-1, idx, -1):
        if nums[idx] < nums[i]:
            nums[idx], nums[i] = nums[i], nums[idx]
            break

    nums[:] = nums[:idx+1] + nums[idx+1:][::-1]
    return nums

if __name__ == "__main__":
    test_arr = [5, 4, 3, 2, 1]
    sol = next_permutation(test_arr)
    print(sol)
