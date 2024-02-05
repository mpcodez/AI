inpL = list(map(int, input().split(" ")))
lines, start = int(inpL[0]), int(inpL[1])

nLine = {}

for i in range(lines):
    tmp = input()
    tmpL = tmp.split(" ")
    t, v = int(tmpL[0]), int(tmpL[1])
    nLine[i+1] = (True if t==1 else False, False, v)
    
curr = start
count = 0
direction = True
bPow = 1

step = bPow * (1 if direction else -1)
while 0 < curr <= lines:
    target, alrHit, power = nLine[curr]
    if alrHit:
        curr += step
        continue
    if target:
        if bPow >= power:
            count += 1
            nLine[curr] = (target, True, power)
        curr += step
    else:
        direction = not direction
        bPow += power
        step = bPow * (1 if direction else -1)
        curr += step

print(count)