cowCount = int(input(""))
cows = input("")

clusters = cows.split("0")
while "" in clusters:
    clusters.remove("")

if cows == "1" or cows == "11":
    print(1)
elif "1" not in cows or clusters == []:
    print(0)
elif "010" in cows or "0110" in cows:
    print(cows.count("1"))
else:
    backup = clusters[:]
    clusters[0] = "1"*(len(clusters[0])*2 - 1)
    clusters[len(clusters)-1] = "1"*(len(clusters[len(clusters)-1])*2 - 1)
    group = 0
    val = len(min(clusters))
    if (val%2 == 0):
        group = val - 1
    else:
        group = val
    
    s = 0
    for i in range(len(backup)):
        if i == 0 or i == len(backup)-1:
            bLen = len(backup[i])
            if len(clusters[i]) == group:
                s += 1
            elif bLen%group == 0:
                s += bLen/group
            else:
                s += bLen//group + 1
        else:
            c = backup[i]
            if len(c)%group == 0:
                s += len(c)/group
            else:
                s += (len(c)//group + 1)
    
    print(int(s))