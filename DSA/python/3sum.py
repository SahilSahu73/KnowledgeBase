def three_sum(nums: list):
    n = len(nums)
    i = 0
    sol = []
    nums.sort()

    while i < n - 1:
        ele = 0
        if i >= 1 and nums[i] == nums[i - 1]:
            i += 1
            continue
        else:
            ele = nums[i]

        j = i + 1
        k = n - 1
        curr_sum = 0
        while j < k:
            curr_sum = ele + nums[j] + nums[k]
            if curr_sum > 0:
                k -= 1
            elif curr_sum < 0:
                j += 1
            elif curr_sum == 0:
                sol.append([ele, nums[j], nums[k]])
                j += 1
                k -= 1
                while j < k and nums[j] == nums[j - 1]:
                    j += 1
                while j < k and nums[k] == nums[k + 1]:
                    k -= 1
        i += 1
    return sol


if __name__ == "__main__":
    test_arr = [2, -2, 0, 3, -3, 5]
    test_arr2 = [-3, 0, 0, 0, 3, 3, 3]
    print(three_sum(test_arr))
    print(three_sum(test_arr2))
