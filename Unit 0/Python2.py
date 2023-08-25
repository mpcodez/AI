## Warmup - 2 ##

def string_times(str, n):
  return str*n

def front_times(str, n):
  return str[:3]*n

def string_bits(str):
  return str[::2]

def string_splosion(str):
  return "".join([str[:x] for x in range(len(str)+1)])

def last2(str):
  return 0 if (len(str) < 2) else sum(1 for i in range(len(str)-2) if str[i:i+2] == str[len(str)-2:])

def array_count9(nums):
  return nums.count(9)

def array_front9(nums):
  return 9 in nums[:4]

def array123(nums):
  return sum(1 for i in range(len(nums) - 2) if nums[i] == 1 and nums[i+1] == 2 and nums[i+2] == 3) > 0
  
def string_match(a, b):
  return sum(1 for i in range(min(len(a), len(b)) - 1) if a[i:i+2] == b[i:i+2])

## Logic - 2 ##

def make_bricks(small, big, goal):
  return True if ((big*5 + small) >= goal) and (goal - (goal//5)*5 <= small) else False

def lone_sum(a, b, c):
  return 0 if a == b == c else a if b == c else b if a == c else c if a == b else a + b + c

def lucky_sum(a, b, c):
  return 0 if a == 13 else a if b == 13 else a + b if c == 13 else a + b + c

def no_teen_sum(a, b, c):
  return (0 if(a in range(13, 30) and a not in [15, 16]) else a) + (0 if(b in range(13, 30) and b not in [15, 16]) else b) + (0 if(c in range(13, 30) and c not in [15, 16]) else c)
  
def round_sum(a, b, c):
  return ((a//10)*10 if a%10 < 5 else (a//10 + 1)*10) + ((b//10)*10 if b%10 < 5 else (b//10 + 1)*10) + ((c//10)*10 if c%10 < 5 else (c//10 + 1)*10)

def close_far(a, b, c):
  return ((abs(a - b) <= 1 and abs(a - c) >= 2 and abs(b - c) >= 2) != (abs(a - c) <= 1 and abs(a - b) >= 2 and abs(b - c) >= 2))

def make_chocolate(small, big, goal):
  return (goal - (goal//5 if big*5 > goal else big)*5) if ((big*5 + small) >= goal) and (goal - (goal//5)*5 <= small) else -1

## String - 2 ##

def double_char(str):
  return "".join([str[i:i+1]*2 for i in range(len(str))])

def count_hi(str):
  return str.count("hi")

def cat_dog(str):
  return str.count("cat") == str.count("dog")

def count_code(str):
  return sum(1 for i in range(len(str) - 3) if str[i:i+2] == 'co' and str[i+3] == 'e')

def end_other(a, b):
  return a.lower() == b[len(b) - len(a):].lower() or b.lower() == a[len(a) - len(b):].lower()

def xyz_there(str):
  return str[:3] == "xyz" or sum(1 for i in range(len(str) - 3) if str[i:i+1] != '.' and str[i+1:i+4] == 'xyz') > 0

## List - 2 ##

def count_evens(nums):
  return sum(1 for n in nums if n%2 == 0)

def big_diff(nums):
  return max(nums) - min(nums)

def centered_average(nums):
  return int((sum(nums) - max(nums) - min(nums)) / (len(nums) - 2))

#SUM-13
def sum13(nums):
  i=0
  while i < len(nums):
    if(nums[i])==13:
      nums[i]=0
      if i<len(nums)-1:
        nums[i+1]=0
    i+=1
  return sum(nums)

#SUM-67
def sum67(nums):
  nums=nums[:]
  while 6 in nums:
    i=nums.index(6)
    j=nums.index(7,i)
    del nums[i:j+1]
  return sum(nums)


def has22(nums):
  return sum(1 for n in range(len(nums)-1) if nums[n] == 2 and nums[n] == nums[n+1]) > 0

#Medha Pappula, 6, 2026