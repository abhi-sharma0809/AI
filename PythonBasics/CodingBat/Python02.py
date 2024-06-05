#Warmup
def string_times(str, n):
  return str*n

def front_times(str, n):
  return str[:3] * n

def string_bits(str):
  return str[ : :2]

def string_splosion(str):
  return "".join(str[:i+1] for i in range(len(str)))

def last2(str):
  return sum(str[i:i+2] == str[-2:] for i in range(len(str)-2))

def array_count9(nums):
  return nums.count(9)

def array_front9(nums):
  return 9 in nums[:4]

def array123(nums):
  return any([1,2,3] == nums[i:i+3] for i in range(len(nums)))

def string_match(a, b):
  return sum(a[i:i+2] == b[i:i+2] for i in range(min(len(a), len(b))-1))


#Logic
def make_bricks(small, big, goal):
  return goal-(5*min(big,goal//5))-small < 1

def lone_sum(a, b, c):
  return sum(i for i in [a,b,c] if [a,b,c].count(i) < 2)

def lucky_sum(a, b, c):
    return ((a==13) or a + lucky_sum(b,c,13)+1)-1

def no_teen_sum(a, b, c):
  return sum(i for i in [a,b,c] if i not in [13,14,17,18,19])

def round_sum(a, b, c):
  return sum(((i+5)//10)*10 for i in[a,b,c])

def close_far(a, b, c):
    return (abs(a - b) < 2 and (abs(a - c) > 1 < abs(b - c))) ^ (abs(a - c) < 2 and (abs(a - b) > 1 < abs(b - c)))

def make_chocolate(small, big, goal):
    return [goal-min(goal // 5, big) * 5, -1][small<goal-min(goal // 5, big) * 5]

#String
def double_char(str):
  return "".join(i+i for i in str)

def count_hi(str):
  return str.count("hi")

def cat_dog(str):
  return str.count('cat') == str.count('dog')

def count_code(str):
  return sum(str[i:i+2] == 'co' and str[i+3] == 'e' for i in range(len(str)-3))
  

def end_other(a, b):
  return b.lower().endswith(a.lower()) or a.lower().endswith(b.lower())

def xyz_there(str):
  return str[:3] == 'xyz' or any((str[i] != '.' and str[i+1:i+4]) == 'xyz' for i in range(len(str)))

#List
def count_evens(nums):
  return sum(1-n%2 for n in nums)

def big_diff(nums):
    return max(nums) - min(nums)

def centered_average(nums):
  return sum(sorted(nums)[1:-1]) // (len(nums) - 2)

def sum13(nums):
   return sum(nums[n] for n in range(len(nums)) if nums[n] != 13 and (n==0 or nums[n-1] !=13))

def sum67(nums):
  while 6 in nums: del nums[nums.index(6):nums.index(7,nums.index(6))+1]
  return sum(nums)

def has22(nums):
  return any(nums[i:i+2] == [2,2] for i in range(len(nums)-1))

#Abhisheik Sharma 7 2024


