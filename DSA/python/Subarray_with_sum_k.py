def sum_k_subarray_count(nums: list, k: int):
    prefix_sum = 0
    mpp = {0:1}
    count = 0
    for i in range(len(nums)):
        prefix_sum += nums[i]

        rem = prefix_sum - k
        if rem in mpp:
            count += mpp[rem]

        if prefix_sum not in mpp:
            mpp[prefix_sum] = 1
        else:
            mpp[prefix_sum] += 1


def max_xor_sum(nums: list, k: int):
    n = len(nums)
    max_sum = 0
    for i in range(k+1):
        temp_sum = 0
        for j in range(n):
            temp_sum += i ^ nums[j]
            max_sum = max(max_sum, temp_sum)
    return max_sum


if __name__ == "__main__":
    nums = list(map(int, input()))

