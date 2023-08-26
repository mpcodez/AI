## Warmup - 2 ##

def string_times(str, n):
  return str*n

def front_times(str, n):
  return str[:3]*n

def string_bits(str):
  return str[::2]

def string_splosion(s):
  return ''.join(s[:i+1] for i in range(len(s)))

def last2(str):
  return sum(1 for i in range(len(str)-2) if str[i:i+2] == str[-2:])

def array_count9(nums):
  return nums.count(9)

def array_front9(nums):
  return 9 in nums[:4]

def array123(nums):
  return any(nums[i:i+3] == [1, 2, 3] for i in range(len(nums) - 2))

def string_match(a, b):
  return sum(1 for i in range(len(a)-1) if a[i:i+2] == b[i:i+2])

## Logic - 2 ##

def make_bricks(small, big, goal):
  return goal <= small + big * 5 and goal % 5 <= small

def lone_sum(a, b, c):
  return 0 if a == b == c else a if b == c else b if a == c else c if a == b else a + b + c

def lucky_sum(a, b, c):
  return 0 if a == 13 else a if b == 13 else a + b if c == 13 else a + b + c

def no_teen_sum(a, b, c):
  return sum(x if x not in [13, 14, 17, 18, 19] else 0 for x in [a, b, c])

def round_sum(a, b, c):
  return sum((num // 10 + 1)*10 if num%10 >= 5 else (num // 10)*10 for num in [a, b, c])

def close_far(a, b, c):
  return (abs(b - a) <= 1 and abs(c - a) >= 2 and abs(c - b) >= 2) or (abs(c - a) <= 1 and abs(b - a) >= 2 and abs(b - c) >= 2)

def make_chocolate(small, big, goal):
  return goal - 5 * min(big, goal // 5) if goal - 5 * min(big, goal // 5) <= small else -1

## String - 2 ##

def double_char(str):
  return ''.join([i*2 for i in str])

def count_hi(str):
  return str.count("hi")

def cat_dog(str):
  return str.count('cat') == str.count('dog')

def count_code(str):
  return sum(1 for i in range(len(str)-3) if str[i:i+2]=='co' and str[i+3]=='e')

def end_other(a, b):
  return a.lower().endswith(b.lower()) or b.lower().endswith(a.lower())

def xyz_there(str):
  return True in ('xyz' in str[i:i+3] and (i == 0 or str[i-1] != '.') for i in range(len(str) - 2))

## List - 2 ##

def count_evens(nums):
  return sum(1 for num in nums if num % 2 == 0)

def big_diff(nums):
  return max(nums) - min(nums)

def centered_average(nums):
  return (sum(nums) - max(nums) - min(nums)) // (len(nums) - 2)

def sum13(nums):
  return sum(nums[i] for i in range(len(nums)) if nums[i] != 13 and (i == 0 or nums[i - 1] != 13))

def sum67(nums):
  return sum([x for index, x in enumerate(nums) if (((nums[(index - nums[index::-1].index(6)):].index(7) + (index - nums[index::-1].index(6))) < index) if (6 in nums[:index+1]) else True)])

def has22(nums):
  return sum(1 for n in range(len(nums)-1) if nums[n] == 2 and nums[n] == nums[n+1]) > 0

#Medha Pappula, 6, 2026