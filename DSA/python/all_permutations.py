# Method 1
def permute(nums: list):
    ans = []
    ds = []
    freq: list[bool] = [False for _ in range(len(nums))]
    recurPermute(nums, ans, ds, freq)
    return ans

def recurPermute(nums, ans, ds, freq):
    if len(ds) == len(nums):
        ds_copy = ds.copy()
        ans.append(ds_copy)
        return

    for i in range(len(nums)):
        if not freq[i]:
            freq[i] = True
            ds.append(nums[i])
            recurPermute(nums, ans, ds, freq)
            ds.pop()
            freq[i] = False


# Method 2
def permute2(nums):
    ans = []
    recurPermute2(0, nums, ans)
    return ans

def recurPermute2(idx, nums, ans):
    if idx == len(nums):
        ans.append(nums.copy())
        return

    for i in range(idx, len(nums)):
        nums[idx], nums[i] = nums[i], nums[idx]
        recurPermute2(idx + 1, nums, ans)
        nums[idx], nums[i] = nums[i], nums[idx]


if __name__ == "__main__":
    test_arr = [1, 2, 3]
    sol = permute2(test_arr)
    print(sol)
