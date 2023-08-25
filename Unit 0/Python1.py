def sleep_in(weekday, vacation):
    return True if(not weekday or vacation) else False

def monkey_trouble(a_smile, b_smile):
    return True if a_smile is b_smile else False

def sum_double(a, b):
    return 2*(a+b) if a is b else a + b

def diff21(n):
    return 2*(n-21) if n > 21 else abs(n-21)

def parrot_trouble(talking, hour):
    return True if (talking) and (hour < 7 or hour > 20) else False

def makes10(a, b):
    return True if a == 10 or b == 10 or a + b == 10 else False

def near_hundred(n):
    return True if (abs(n-100) <= 10) or (abs(n-200) <= 10) else False

def pos_neg(a, b, negative):
    return True if (a*b != abs(a*b) and not negative) or (negative and a != abs(a) and b != abs(b)) else False

def hello_name(name):
    return "Hello " + name + "!"

def make_abba(a, b):
    return a+b+b+a

def make_tags(tag, word):
    return "<" + tag + ">" + word + "</" + tag + ">"

def make_out_word(out, word):
    return out[:len(out)//2] + word + out[len(out)//2:]

def extra_end(str):
    return str[len(str)-2:len(str)]*3

def first_two(str):
    return str if len(str) < 2 else str[0:2]

def first_half(str):
    return str[0:int(len(str)/2.0)]

def without_end(str):
    return str[1:len(str)-1]

def first_last6(nums):
    return True if (str(nums[0]) == "6" or str(nums[len(nums)-1]) == "6") else False

def same_first_last(nums):
    return True if len(nums) >= 1 and str(nums[0]) == str(nums[len(nums)-1]) else False

def make_pi(n):
    return [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7][:n]

def common_end(a, b):
    return True if (a[0] == b[0]) or (a[len(a)-1] == b[len(b)-1]) else False

def sum3(nums):
    return sum(nums)

def rotate_left3(nums):
    return nums[1:] + [nums[0]] if len(nums) >= 2 else nums

def reverse3(nums):
    return nums[::-1]

def max_end3(nums):
    return [nums[0]]*len(nums) if nums[0] > nums[len(nums)-1] else [nums[len(nums)-1]]*len(nums)

def cigar_party(cigars, is_weekend):
    return True if(cigars >= 40) and (is_weekend or (is_weekend == False and cigars <= 60)) else False

def date_fashion(you, date):
    return 0 if(you <= 2 or date <= 2) else 2 if (you >= 8 or date >= 8) else 1

def squirrel_play(temp, is_summer):
    return True if ((temp >= 60) and ((is_summer and temp <= 100) or (not is_summer and temp <= 90))) else False

def caught_speeding(speed, is_birthday):
    return 0 if(speed <= 60 + (5 if is_birthday else 0)) else 1 if (speed >= 61 + (5 if is_birthday else 0) and speed <= 80 + (5 if is_birthday else 0)) else 2

def sorta_sum(a, b):
    return 20 if (a+b >= 10 and a+b <= 19) else a + b

def alarm_clock(day, vacation):
    return ("off" if vacation else "10:00") if(day == 0 or day == 6) else ("10:00" if vacation else "7:00")    

def love6(a, b):
    return True if a == 6 or b == 6 or a+b == 6 or abs(a-b) == 6 or abs(b-a) == 6 else False

def in1to10(n, outside_mode):
    return (n <= 1 or n >= 10) if outside_mode else (n >= 1 and n <= 10) 