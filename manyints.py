import sys; args = sys.argv[1:]
import time

startTime = time.time()

A = open(args[0]).read().split("\n")
B = open(args[1]).read().split("\n")
C = open(args[2]).read().split("\n")

A = list(map(int, A))
B = list(map(int, B))
C = list(map(int, C))

def find_unique_common_elements(listA, listB):
    setA = set(listA)
    setB = set(listB)
    common_elements = setA.intersection(setB)
    return list(common_elements)

def dist100th(lst):
    seen = set()
    noted_values = []

    for index, value in enumerate(lst):
        if value not in seen:
            seen.add(value)
            if len(seen) % 100 == 0:
                noted_values.append(value)

    return sum(noted_values)

def sumCommon(A, B, C):
    AC = find_unique_common_elements(C, A)
    BC = find_unique_common_elements(C, B)
    s = 0
    
    for i in AC:
        s += A.count(i)
    
    for i in BC:
        s += B.count(i)
        
    return s

def unique(A):
    unique_numbers = set(A)
    
    sorted_numbers = list(unique_numbers)
    sorted_numbers.sort(key = int)
    
    result = sorted_numbers[:10]
    return result
    
def dupl(arr):
    duplicates = [num for num in set(arr) if arr.count(num) >= 2]
    duplicates.sort(reverse=True)
    return duplicates[:10]
    
def seqSum(lst):
    smallest_unnoted = float('inf')
    total_sum = 0

    for num in lst:
        if num % 53 == 0:
            total_sum += smallest_unnoted
        elif num < smallest_unnoted:
            smallest_unnoted = num

    return total_sum

print("#1: " + str(len(find_unique_common_elements(A, B))))

print("#2: " + str(dist100th(A)))

print("#3: " + str(sumCommon(A, B, C)))

print("#4: " + str(unique(A)))

print("#5: " + str(dupl(B)))

print("#6: " + str(seqSum(A)))

print("Total time: ", str(round(time.time()-startTime, 3)) + "s")


# Medha Pappula, 6, 2026