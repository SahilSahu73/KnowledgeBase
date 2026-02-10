def sort_array_of_012(nums: list):
    low = mid = 0
    high = len(nums)-1
    while(mid<high):
        if nums[mid] == 0:
            nums[mid], nums[low] = nums[low], nums[mid]
            mid += 1
            low += 1
        elif nums[mid] == 1:
            mid += 1
        elif nums[mid] == 2:
            nums[mid], nums[high] = nums[high], nums[mid]
            mid += 1
            high -= 1

nums = [1, 2, 0, 0, 2, 1]
sort_array_of_012(nums)
print(nums)
