import re
def get_data(day,part):
    print(f"day{day} part{part}:")
    data = []
    file = open(f"inputs/Day{day}part{part}.txt", "r")
    for line in file:
        if type(line) is int:
            data.append(int(line))
        else:
            data.append(line)
    file.close()
    return data
def frequency(day, part):
    file = open(f"inputs/Day{day}part{part}.txt", "r")
    #create variable
    total = 0
    # for every number add or subtract it from total
    for line in file:
        total += int(line)
    file.close()
    #print total
    print(total)
def repFrequency(day, part):
    # create 2 lists and total
    total = 0
    pastfrequencies = []
    pastfrequencies.append(total)
    # populate frequencies
    frequency = get_data(day,part)
    # go through frequencies and add then to past frequencies list for compare
    i = 0
    while 1:
        if i == len(frequency):
            i = 0
        total += int(frequency[i])
        # check if past frequencies contains the frequency all ready and stop
        if total in pastfrequencies:
            break;
        # save frequency to past frequencies and move to next iteration
        pastfrequencies.append(total)
        i += 1
    print(total)
def letterMultible(day,part):
    #create lists and variables to compare and populate them
    boxart = get_data(day,part)
    threeDigs = twoDigs = 0

    for box in boxart:
        two = False
        three = False
        for char in set(box):
            char = box.count(char)
            if char == 2:
                two = True
            elif char == 3:
                three = True
            if two and three:
                break;
        twoDigs +=1 if two else 0
        threeDigs +=1 if three else 0

    return print(f" found threeDigs: {threeDigs} and twoDigs: {twoDigs} checksum is: {threeDigs * twoDigs}")
def letterDifference(day, part):
    # create lists and variables to compare and populate them
    boxart = get_data(day, part)
    box1 = box2 = ""
    correctDigs = []
    i = 0
    while i < len(boxart):
        box1 = boxart[i]
        for box in boxart:
            box = box.strip()
            box1 = box1.strip()

            if (sum(inst1 != inst2 for inst1, inst2 in zip(box,box1) )) == 1:
                remove = ''.join(set(box1) ^ set(box))
                correct = box.replace(""+remove, "")
                return print(correct)
        i +=1
def calculateOverlap(info1, info2,counted):
    """
    sw = start width
    asw = another start width
    sh = start height
    ash another startwidt
    wl = widht lenght
    awl = another width lenght
    hl =height lenght
    ahl = another heihght lenght
    """
    id,sw,sh,wl,hl = info1
    aid, asw,ash,awl,ahl = info2
    overlapW = min(sw+wl,asw+awl) - max(sw,asw)
    overlapH = min(sh+hl,ash+ahl) - max(sh,ash)
    if overlapW > 0 and overlapH > 0:
        overlapstartW = max(sw,asw)
        overlapstartH = max(sh,ash)
        for i in range(overlapstartW,overlapstartW + overlapW):
            for j in range(overlapstartH,overlapstartH + overlapH):
                counted.append((i,j))
    else:
        return
def fabricCut(day,part):
    claimList = get_data(day, part)
    CountedPositions = []
    postitionInfo = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
    for i in range(len(claimList)):
        positions = tuple(map(int,postitionInfo.match(claimList[i]).groups()))
        for j in range(i+1,len(claimList)):
            otherPositions = tuple(map(int,postitionInfo.match(claimList[j]).groups()))
            calculateOverlap(positions, otherPositions,CountedPositions)
    Dublicates = set()
    Seen = set()
    for count in CountedPositions:
        if count not in Seen:
            Seen.add(count)
        else:
            Dublicates.add(count)
    overlapCount = len(Dublicates)
    firstCount = len(Seen)
    print(f"overlap count: {overlapCount} once seen count: {firstCount}")
    return
def checkNoOverlap(setOfElves):

    for elves in setOfElves:
        checkThis = elves
        noConflict = True
        for measures in setOfElves:
            if checkThis == measures:
                continue
            id, sw, sh, wl, hl = checkThis
            aid, asw, ash, awl, ahl = measures
            overlapW = min(sw + wl, asw + awl) - max(sw, asw)
            overlapH = min(sh + hl, ash + ahl) - max(sh, ash)
            if overlapW > 0 and overlapH > 0:
                noConflict = False
                break
        if noConflict:
            return id

    return 0
def noOverlap(day,part):
    List = get_data(day, part)
    Dataposition = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
    setOfElves = set()
    for i in range(len(List)):
        Data = tuple(map(int,Dataposition.match(List[i]).groups()))
        setOfElves.add(Data)
    id = checkNoOverlap(setOfElves)
    print(f"There is no conflict with elf id: {id}")

    return
# Map days and parts to functions
actions = {
    (1,1): frequency,
    (1,2): repFrequency,
    (2,1): letterMultible,
    (2,2): letterDifference,
    (3,1): fabricCut,
    (3,2): noOverlap,
}

def main():
    #Which part are you doing?
    day  = 3
    part = 2
    # read input
    while day <= 25:
        func = actions.get((day,part))
        if func:
            func(day, part)
        part = 2 if part == 1 else 1
        if part == 1:
            day += 1


main()