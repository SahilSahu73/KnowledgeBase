def two_sum(nums: list, target: int):
    mpp = {}
    for i in range(len(nums)):
        k = target - nums[i]
        if k in mpp:
            return [mpp[k], i]
        else:
            mpp[nums[i]] = i


if __name__ == "__main__":
    test_arr = [2, 6, 1, 8, 5, 11]
    print(two_sum(test_arr, 16))
