import re
def get_data(day,part):
    """Get input data from file"""
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
    print(f"day{day} part{part}:")
    file = open(f"inputs/Day{day}part{part}.txt", "r")
    """create variable"""
    total = 0
    """for every number add or subtract it from total ( numerical data might be - )"""
    for line in file:
        total += int(line)
    file.close()
    """print total"""
    print(f"Resulting frequency is {total}")
def repFrequency(day, part):
    """create 2 lists and total
    Should do this again using sets. List iteration takes way too long"""
    total = 0
    pastfrequencies = []
    pastfrequencies.append(total)
    """populate frequencies"""
    frequency = get_data(day,part)
    """go through frequencies and add then to past frequencies list for compare"""
    i = 0
    while 1:
        if i == len(frequency):
            i = 0
        total += int(frequency[i])
        """check if past frequencies contains the frequency all ready and stop"""
        if total in pastfrequencies:
            break;
        """save frequency to past frequencies and move to next iteration"""
        pastfrequencies.append(total)
        i += 1
    print(f"First frequency the device reaches twice is :{total}")
def letterMultible(day,part):
    """create lists and variables"""
    boxArt = get_data(day,part)
    threeDigs = twoDigs = 0
    """go through all values in data"""
    for box in boxArt:
        """set  two found and three found flags as false"""
        two = False
        three = False
        """go through each string set"""
        for char in set(box):
            """set flag as true if 2 and/or 3 is found"""
            char = box.count(char)
            if char == 2:
                two = True
            elif char == 3:
                three = True
            if two and three:
                break;
        """ 
        since there are 3 different possibilities
        1 or 2 set of 2 letters ( gives 1 set of 2 anyway )
        1 or 2 set of 3 letters ( gives 1 set of 3 anyway )
        1 set of 2 and 1 set of 3 letters ( gives 1 set of each )
        so you can only get 1 of each any ways, we can use the flags to to
        add the given sets per iteration
        """
        twoDigs +=1 if two else 0
        threeDigs +=1 if three else 0

    return print(f" found threeDigs: {threeDigs} and twoDigs: {twoDigs} checksum is: {threeDigs * twoDigs}")
def letterDifference(day, part):
    """create lists and variables"""
    boxart = get_data(day, part)
    """Same as previous take one from the list and go through the string in it"""
    for checkThis in boxart:
        for box in boxart:
            """stript the line change just because"""
            box = box.strip()
            checkThis = checkThis.strip()
            """
            zip(): it pairs one letter for each box 
            what line 93 does it checks if any of the letters are different and 
            gives True then othewise it gives False I can sum them and when it gives 
            exacly 1 it means it has only 1 letter difference.
            """
            if (sum(inst1 != inst2 for inst1, inst2 in zip(box,checkThis) )) == 1:
                """Stupid way to manipulate set&lists to string"""
                remove = ''.join(set(checkThis) ^ set(box))
                correct = box.replace(""+remove, "")
                return print(f"Common letters between two corresponding box ID:s are:{correct}")
def calculateOverlap(info1, info2,counted):
    """
    sw = start width
    asw = another start width
    sh = start height
    ash another start width
    wl = width length
    awl = another width length
    hl =height length
    ahl = another height length
    Extract values to individual variables
    """
    id,sw,sh,wl,hl = info1
    aid, asw,ash,awl,ahl = info2
    """calculate if given measures overlap result in these are - if they don't and + if they do"""
    overlapW = min(sw+wl,asw+awl) - max(sw,asw)
    overlapH = min(sh+hl,ash+ahl) - max(sh,ash)
    if overlapW > 0 and overlapH > 0:
        """when there is overlap calculate the starting point and add resulting values to list
        for later use"""
        overlapstartW = max(sw,asw)
        overlapstartH = max(sh,ash)
        for i in range(overlapstartW,overlapstartW + overlapW):
            for j in range(overlapstartH,overlapstartH + overlapH):
                counted.append((i,j))
    else:
        return
def fabricCut(day,part):
    """populate...create variables..."""
    claimList = get_data(day, part)
    CountedPositions = []
    """
    This extracts values from string 
    if input data has many lines that contain values in same spots
    """
    postitionInfo = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
    """TODO: Create way to go through without 2 loops for efficiency"""
    """Go through the list 2 times to get 2 value sets to compare"""
    for i in range(len(claimList)):
        positions = tuple(map(int,postitionInfo.match(claimList[i]).groups()))
        for j in range(i+1,len(claimList)):
            otherPositions = tuple(map(int,postitionInfo.match(claimList[j]).groups()))
            """Check the funciton for info"""
            calculateOverlap(positions, otherPositions,CountedPositions)
    """Create 2 sets to populate for seen once and seen more than once"""
    Dublicates = set()
    Seen = set()
    """
    This list has been populated in function
    It contains every used inch in every claim
    when iterating it the ones that are all ready seen will be put in
    duplicates and the ones that are seen first time are put to seen
    """
    for count in CountedPositions:
        if count not in Seen:
            Seen.add(count)
        else:
            Dublicates.add(count)
    """Length of the sets reveal how many square inches are claimed more than once"""
    overlapCount = len(Dublicates)
    firstCount = len(Seen)
    print(f"overlap count: {overlapCount} once seen count: {firstCount}")
    return
def checkNoOverlap(setOfElves):
    """
    Using the knowledge from previous puzzle we go
    through the set two times to compare sets
    """
    for elves in setOfElves:
        checkThis = elves
        """Flag for the one ID that doesn't have any overlap"""
        noConflict = True
        for measures in setOfElves:
            if checkThis == measures:
                continue
            """calculate if given measures overlap result in these are - if they don't and + if they do"""
            id, sw, sh, wl, hl = checkThis
            aid, asw, ash, awl, ahl = measures
            overlapW = min(sw + wl, asw + awl) - max(sw, asw)
            overlapH = min(sh + hl, ash + ahl) - max(sh, ash)
            if overlapW > 0 and overlapH > 0:
                """when there is overlap we can set the flag as False"""
                noConflict = False
                break
        if noConflict:
            """When there is no conflict return the id and stop going through since there was only one"""
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
"""Map days and parts to functions"""
actions = {
    (1,1): frequency,
    (1,2): repFrequency,
    (2,1): letterMultible,
    (2,2): letterDifference,
    (3,1): fabricCut,
    (3,2): noOverlap,
}

def main():
    """Which part are you doing?"""
    day  = 1
    part = 1
    """go through the days after previously set"""
    while day <= 25:
        """Get the day from dict"""
        func = actions.get((day,part))
        """if found run it"""
        if func:
            func(day, part)
        """switch between 1 and 2"""
        part = 2 if part == 1 else 1
        if part == 1:
            day += 1


main()