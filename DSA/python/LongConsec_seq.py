def longestConsecutiveSequence(nums: list):
    n = len(nums)
    nums_set = set()

    for i in range(n):
        nums_set.add(nums[i])

    seq_count = 0
    longest = -1

    for ele in nums_set:
        seq_count = 1
        if ele - 1 not in nums_set:
            x = ele
            while x + 1 in nums_set:
                x += 1
                seq_count += 1

            longest = max(seq_count, longest)

    return longest


if __name__ == "__main__":
    test_arr = [1, 3, 4, 6, 2, 5, 100, 102, 4, 101]
    longest_seq = longestConsecutiveSequence(test_arr)
    print(longest_seq)
