l1 = input("")
l2 = input("")
l3 = input("")

n, m = l1.split(" ")
cowN = int(n)
caneM = int(m)

cows = l2.split(" ")
canes = l3.split(" ")

for i in range(cowN):
    cows[i] = int(cows[i])
    
for i in range(caneM):
    canes[i] = int(canes[i])

for cane in canes:
    hRange = [0, cane]
    for i in range(cowN):
        cow = cows[i]
        if hRange[0] == hRange[1]:
            break
        elif cow > hRange[0] and cow <= hRange[1]:
            tmp = cow - hRange[0]
            hRange[0] += tmp
            cows[i] += tmp
        elif cow > hRange[1]:
            tmp = hRange[1] - hRange[0]
            hRange[0] = hRange[1]
            cows[i] += tmp

for cow in cows:
    print(cow)