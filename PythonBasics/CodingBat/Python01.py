#Warmup
def sleep_in(weekday, vacation):
  return True if weekday == False or vacation == True else False

def monkey_trouble(a_smile, b_smile):
  return True if a_smile == b_smile else False

def sum_double(a, b):
  return (a+b)*2 if a == b else a+b

def diff21(n):
  return abs(n-21)*2 if n>21 else abs(n-21)

def parrot_trouble(talking, hour):
  return True if (talking == True and hour < 7) or (talking == True and hour > 20) else False

def makes10(a, b):
  return True if a == 10 or b == 10 or a+b == 10 else False

def near_hundred(n):
  return True if abs(100-n) <= 10 or abs(200-n) <= 10 else False

def pos_neg(a, b, negative):
  return True if (negative == True and a < 0 and b < 0) or (a < 0 and b > 0 and negative == False) or (a > 0 and b < 0 and negative == False) else False

#String
def hello_name(name):
  return "Hello " + name + "!"

def make_abba(a, b):
  return a + b + b + a

def make_tags(tag, word):
  return "<" + tag + ">" + word + "<" + "/" + tag + ">"

def make_out_word(out, word):
  return out[0:len(out)//2] + word + out[len(out)//2:len(out)]

def extra_end(str):
  return str[len(str)-2:len(str)] * 3

def first_two(str):
  return str if len(str) < 2 else str[0:2]

def first_half(str):
  return str[0:len(str)//2]

def without_end(str):
  return str[1:len(str)-1]

#List
def first_last6(nums):
  return True if nums[0] == 6 or nums[0] == "6" or nums[len(nums)-1] == 6 or nums[len(nums)-1] =="6" else False

def same_first_last(nums):
  return True if len(nums) >= 1 and nums[0] == nums[len(nums)-1] else False  

def make_pi(n):
   return [3,1,4,1,5,9,2,6,5,3,5,8,9,7][0:n]

def common_end(a, b):
  return True if (str(a[0]) == str(b[0])) or (str(a[len(a)-1]) == str(b[len(b)-1])) else False

def sum3(nums):
  return sum(nums)

def rotate_left3(nums):
  return nums if len(nums)<2 else nums[1:len(nums)] + nums[0:1]

def reverse3(nums):
  return nums[ : :-1]

def max_end3(nums):
  return nums if len(nums)==1 else [max(nums[0],nums[len(nums)-1])]*len(nums)


#Logic
def cigar_party(cigars, is_weekend):
  return True if (is_weekend == True and cigars >= 40) or (is_weekend == False and cigars >= 40 and cigars <= 60) else False

def date_fashion(you, date):
  return 2 if (you >=8 and date > 2) or (date >= 8 and you > 2) else 1 if you > 2 and date > 2 else 0
  
def squirrel_play(temp, is_summer):
  return True if (is_summer == True and temp > 59 and temp < 101) or (is_summer == False and temp > 59 and temp < 91) else False

def caught_speeding(speed, is_birthday):
  return caught_speeding(speed-5,False) if is_birthday == True else 0 if speed<=60 else 1 if speed < 81 and speed > 60 else 2 

def sorta_sum(a, b):
  return 20 if  a + b > 9 and a + b < 20 else a+b

def alarm_clock(day, vacation):
  return "7:00" if day > 0 and day < 6 and vacation == False else "10:00" if(day == 0 and vacation == False) or (day == 6 and vacation == False) or (day > 0 and day < 6 and vacation == True) else "off"

def love6(a, b):
  return True if (a == 6 or b == 6) or (a + b == 6) or (abs(a-b) == 6) else False

def in1to10(n, outside_mode):
  return True if (outside_mode == False and n >= 1 and n <= 10) or (outside_mode == True and (n <= 1 or n >= 10)) else False

