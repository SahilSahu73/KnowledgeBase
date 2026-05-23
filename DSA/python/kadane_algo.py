def kadane_algo(nums: list):
    n = len(nums)
    maxi = float("-inf")
    curr_sum = 0
    for i in range(n):
        curr_sum += nums[i]
        if curr_sum > maxi:
            maxi = curr_sum
        if curr_sum < 0:
            curr_sum = 0
    return maxi


if __name__ == "__main__":
    test_arr = [1, 8, 4, -8, -5, -3, -2, -10, 4]
    max_sum_subarr = kadane_algo(test_arr)
    print(max_sum_subarr)
