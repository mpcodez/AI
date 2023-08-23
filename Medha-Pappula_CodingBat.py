## Warmup - 1 ##

def sleep_in(weekday, vacation):
    """
    The parameter weekday is True if it is a weekday, and the parameter vacation is True if we are on vacation. We sleep in if it is not a weekday or we're on vacation. Return True if we sleep in.

    sleep_in(False, False) → True
    sleep_in(True, False) → False
    sleep_in(False, True) → True
    """
    return True if(not weekday or vacation) else False

def monkey_trouble(a_smile, b_smile):
    """We have two monkeys, a and b, and the parameters a_smile and b_smile indicate if each is smiling. We are in trouble if they are both smiling or if neither of them is smiling. Return True if we are in trouble.

    monkey_trouble(True, True) → True
    monkey_trouble(False, False) → True
    monkey_trouble(True, False) → False
    """
    return True if a_smile is b_smile else False

def sum_double(a, b):
    """
    Given two int values, return their sum. Unless the two values are the same, then return double their sum.

    sum_double(1, 2) → 3
    sum_double(3, 2) → 5
    sum_double(2, 2) → 8
    """
    return 2*(a+b) if a is b else a + b

def diff21(n):
    """
    Given an int n, return the absolute difference between n and 21, except return double the absolute difference if n is over 21.

    diff21(19) → 2
    diff21(10) → 11
    diff21(21) → 0
    """
    return 2*(n-21) if n > 21 else abs(n-21)

def parrot_trouble(talking, hour):
    """
    We have a loud talking parrot. The "hour" parameter is the current hour time in the range 0..23. We are in trouble if the parrot is talking and the hour is before 7 or after 20. Return True if we are in trouble.

    parrot_trouble(True, 6) → True
    parrot_trouble(True, 7) → False
    parrot_trouble(False, 6) → False
    """
    if(talking):
        if(hour >= 7 and hour <= 20):
            return False
        return True
    return False

def makes10(a, b):
    """
    Given 2 ints, a and b, return True if one if them is 10 or if their sum is 10.

    makes10(9, 10) → True
    makes10(9, 9) → False
    makes10(1, 9) → True
    """
    return True if a == 10 or b == 10 or a + b == 10 else False

def near_hundred(n):
    """
    Given an int n, return True if it is within 10 of 100 or 200. Note: abs(num) computes the absolute value of a number.

    near_hundred(93) → True
    near_hundred(90) → True
    near_hundred(89) → False
    """
    return True if (abs(n-100) <= 10) or (abs(n-200) <= 10) else False

def pos_neg(a, b, negative):
    """
    Given 2 int values, return True if one is negative and one is positive. Except if the parameter "negative" is True, then return True only if both are negative.

    pos_neg(1, -1, False) → True
    pos_neg(-1, 1, False) → True
    pos_neg(-4, -5, True) → True
    """
    return True if (a*b != abs(a*b) and not negative) or (negative and a != abs(a) and b != abs(b)) else False


## String - 1 ##

def hello_name(name):
    """
    Given a string name, e.g. "Bob", return a greeting of the form "Hello Bob!".

    hello_name('Bob') → 'Hello Bob!'
    hello_name('Alice') → 'Hello Alice!'
    hello_name('X') → 'Hello X!'
    """
    return "Hello " + name + "!"

def make_abba(a, b):
    """
    Given two strings, a and b, return the result of putting them together in the order abba, e.g. "Hi" and "Bye" returns "HiByeByeHi".

    make_abba('Hi', 'Bye') → 'HiByeByeHi'
    make_abba('Yo', 'Alice') → 'YoAliceAliceYo'
    make_abba('What', 'Up') → 'WhatUpUpWhat'
    """
    return a+b+b+a

def make_tags(tag, word):
    """
    The web is built with HTML strings like "<i>Yay</i>" which draws Yay as italic text. In this example, the "i" tag makes <i> and </i> which surround the word "Yay". Given tag and word strings, create the HTML string with tags around the word, e.g. "<i>Yay</i>".

    make_tags('i', 'Yay') → '<i>Yay</i>'
    make_tags('i', 'Hello') → '<i>Hello</i>'
    make_tags('cite', 'Yay') → '<cite>Yay</cite>'
    """
    return "<" + tag + ">" + word + "</" + tag + ">"

def make_out_word(out, word):
    return out[:len(out)//2] + word + out[len(out)//2:]

def extra_end(str):
    """
    Given a string, return a new string made of 3 copies of the last 2 chars of the original string. The string length will be at least 2.

    extra_end('Hello') → 'lololo'
    extra_end('ab') → 'ababab'
    extra_end('Hi') → 'HiHiHi'
    """
    return str[len(str)-2:len(str)]*3

def first_two(str):
    """
    Given a string, return the string made of its first two chars, so the String "Hello" yields "He". If the string is shorter than length 2, return whatever there is, so "X" yields "X", and the empty string "" yields the empty string "".
    
    first_two('Hello') → 'He'
    first_two('abcdefg') → 'ab'
    first_two('ab') → 'ab'
    """
    if len(str) < 2:
        return str
    return str[0:2]

def first_half(str):
    """
    Given a string of even length, return the first half. So the string "WooHoo" yields "Woo".
    
    first_half('WooHoo') → 'Woo'
    first_half('HelloThere') → 'Hello'
    first_half('abcdef') → 'abc'
    """
    return str[0:int(len(str)/2.0)]

def without_end(str):
    """Given a string, return a version without the first and last char, so "Hello" yields "ell". The string length will be at least 2.

    without_end('Hello') → 'ell'
    without_end('java') → 'av'
    without_end('coding') → 'odin'
    """
    return str[1:len(str)-1]



## List - 1 ##

def first_last6(nums):
    """
    Given an array of ints, return True if 6 appears as either the first or last element in the array. The array will be length 1 or more.

    first_last6([1, 2, 6]) → True
    first_last6([6, 1, 2, 3]) → True
    first_last6([13, 6, 1, 2, 3]) → False
    """
    return True if (str(nums[0]) == "6" or str(nums[len(nums)-1]) == "6") else False

def same_first_last(nums):
    """
    Given an array of ints, return True if the array is length 1 or more, and the first element and the last element are equal.

    same_first_last([1, 2, 3]) → False
    same_first_last([1, 2, 3, 1]) → True
    same_first_last([1, 2, 1]) → True
    """
    return True if len(nums) >= 1 and str(nums[0]) == str(nums[len(nums)-1]) else False

def make_pi(n):
    """
    Return an int array length 3 containing the first 3 digits of pi, {3, 1, 4}.

    make_pi() → [3, 1, 4]
    """
    
    return [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7][:n]

def common_end(a, b):
    """
    Given 2 arrays of ints, a and b, return True if they have the same first element or they have the same last element. Both arrays will be length 1 or more.

    common_end([1, 2, 3], [7, 3]) → True
    common_end([1, 2, 3], [7, 3, 2]) → False
    common_end([1, 2, 3], [1, 3]) → True
    """
    return True if (a[0] == b[0]) or (a[len(a)-1] == b[len(b)-1]) else False

def sum3(nums):
    """
    Given an array of ints length 3, return the sum of all the elements.

    sum3([1, 2, 3]) → 6
    sum3([5, 11, 2]) → 18
    sum3([7, 0, 0]) → 7
    """
    return sum(nums)

def rotate_left3(nums):
    """
    Given an array of ints length 3, return an array with the elements "rotated left" so {1, 2, 3} yields {2, 3, 1}.

    rotate_left3([1, 2, 3]) → [2, 3, 1]
    rotate_left3([5, 11, 9]) → [11, 9, 5]
    rotate_left3([7, 0, 0]) → [0, 0, 7]
    """
    return nums[1:] + [nums[0]] if len(nums) >= 2 else nums

def reverse3(nums):
    """
    Given an array of ints length 3, return a new array with the elements in reverse order, so {1, 2, 3} becomes {3, 2, 1}.

    reverse3([1, 2, 3]) → [3, 2, 1]
    reverse3([5, 11, 9]) → [9, 11, 5]
    reverse3([7, 0, 0]) → [0, 0, 7]
    """
    return nums[::-1]

def max_end3(nums):
    """
    Given an array of ints length 3, figure out which is larger, the first or last element in the array, and set all the other elements to be that value. Return the changed array.

    max_end3([1, 2, 3]) → [3, 3, 3]
    max_end3([11, 5, 9]) → [11, 11, 11]
    max_end3([2, 11, 3]) → [3, 3, 3]
    """
    return [nums[0]]*len(nums) if nums[0] > nums[len(nums)-1] else [nums[len(nums)-1]]*len(nums)


## Logic - 1 ##

def cigar_party(cigars, is_weekend):
    """
    When squirrels get together for a party, they like to have cigars. A squirrel party is successful when the number of cigars is between 40 and 60, inclusive. Unless it is the weekend, in which case there is no upper bound on the number of cigars. Return True if the party with the given values is successful, or False otherwise.

    cigar_party(30, False) → False
    cigar_party(50, False) → True
    cigar_party(70, True) → True
    """
    return True if(cigars >= 40) and (is_weekend or (is_weekend == False and cigars <= 60)) else False

def date_fashion(you, date):
    """
    You and your date are trying to get a table at a restaurant. The parameter "you" is the stylishness of your clothes, in the range 0..10, and "date" is the stylishness of your date's clothes. The result getting the table is encoded as an int value with 0=no, 1=maybe, 2=yes. If either of you is very stylish, 8 or more, then the result is 2 (yes). With the exception that if either of you has style of 2 or less, then the result is 0 (no). Otherwise the result is 1 (maybe).

    date_fashion(5, 10) → 2
    date_fashion(5, 2) → 0
    date_fashion(5, 5) → 1
    """
    if(you <= 2 or date <= 2):
        return 0
    elif(you >= 8 or date >= 8):
        return 2
    return 1

def squirrel_play(temp, is_summer):
    """
    The squirrels in Palo Alto spend most of the day playing. In particular, they play if the temperature is between 60 and 90 (inclusive). Unless it is summer, then the upper limit is 100 instead of 90. Given an int temperature and a boolean is_summer, return True if the squirrels play and False otherwise.

    squirrel_play(70, False) → True
    squirrel_play(95, False) → False
    squirrel_play(95, True) → True
    """
    return True if ((temp >= 60) and ((is_summer and temp <= 100) or (not is_summer and temp <= 90))) else False


def caught_speeding(speed, is_birthday):
    """
    You are driving a little too fast, and a police officer stops you. Write code to compute the result, encoded as an int value: 0=no ticket, 1=small ticket, 2=big ticket. If speed is 60 or less, the result is 0. If speed is between 61 and 80 inclusive, the result is 1. If speed is 81 or more, the result is 2. Unless it is your birthday -- on that day, your speed can be 5 higher in all cases.

    caught_speeding(60, False) → 0
    caught_speeding(65, False) → 1
    caught_speeding(65, True) → 0
    """
    addition = 5 if is_birthday else 0
    if(speed <= 60 + addition):
        return 0
    elif(speed >= 61 + addition and speed <= 80 + addition):
        return 1
    else:
        return 2

def sorta_sum(a, b):
    """
    Given 2 ints, a and b, return their sum. However, sums in the range 10..19 inclusive, are forbidden, so in that case just return 20.

    sorta_sum(3, 4) → 7
    sorta_sum(9, 4) → 20
    sorta_sum(10, 11) → 21
    """
    return 20 if (a+b >= 10 and a+b <= 19) else a + b

def alarm_clock(day, vacation):
    """
    Given a day of the week encoded as 0=Sun, 1=Mon, 2=Tue, ...6=Sat, and a boolean indicating if we are on vacation, return a string of the form "7:00" indicating when the alarm clock should ring. Weekdays, the alarm should be "7:00" and on the weekend it should be "10:00". Unless we are on vacation -- then on weekdays it should be "10:00" and weekends it should be "off".

    alarm_clock(1, False) → '7:00'
    alarm_clock(5, False) → '7:00'
    alarm_clock(0, False) → '10:00'
    """
    if(day == 0 or day == 6):
        return "off" if vacation else "10:00"
    else:
        return "10:00" if vacation else "7:00"
    
def love6(a, b):
    """
    The number 6 is a truly great number. Given two int values, a and b, return True if either one is 6. Or if their sum or difference is 6. Note: the function abs(num) computes the absolute value of a number.

    love6(6, 4) → True
    love6(4, 5) → False
    love6(1, 5) → True
    """
    return True if a == 6 or b == 6 or a+b == 6 or abs(a-b) == 6 or abs(b-a) == 6 else False

def in1to10(n, outside_mode):
    """
    Given a number n, return True if n is in the range 1..10, inclusive. Unless outside_mode is True, in which case return True if the number is less or equal to 1, or greater or equal to 10.

    in1to10(5, False) → True
    in1to10(11, False) → False
    in1to10(11, True) → True
    """
    return (n <= 1 or n >= 10) if outside_mode else (n >= 1 and n <= 10) 