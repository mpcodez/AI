def getNext(prev):
    if prev+1 == 4:
        return 0
    return prev + 1


with open("ACSL/test.txt", encoding = "utf-8") as f:
    thing = []
    count = 0
    discard = []
    
    for line in f:
        thing.append(line.replace("\n", ""))
        count += 1
		
        if count == 2:
            rows = [*thing[0]]
            tiles = thing[1].split(" ")
            indexes = [0, 1, 2, 3, 0, 1, 2, 3]
            thing = []
            count = 0
            index = 0

            special = False
            specNum = ""

            for tile in tiles:
                firstD = tile[0]
                lastD = tile[len(tile)-1]
                if special:
                     if firstD != specNum and lastD != specNum:
                         discard.append(tile)
                         continue
                     else:
                         special = False
                         pass
                         
                if (firstD == lastD) and not special:
                    special = True
                    specNum = firstD

                placed = False

                for tmp in indexes[index:index+4]:
                    if rows[tmp] == firstD:
                        rows[tmp] = lastD
                        placed = True
                        index = getNext(tmp)
                        break
                    if rows[tmp] == lastD:
                        rows[tmp] = firstD
                        placed = True
                        index = getNext(tmp)
                        break

                if placed == False:
                    special = False
                    discard.append(tile)
                

            sum = 0
            for i in discard:
                for x in i:
                    sum += int(x)
            discard = []

            print(sum)