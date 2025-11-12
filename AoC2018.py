import heapq
from classes.coordinates import *
from Functions.Helpers import *
from collections import defaultdict, deque
from datetime import datetime

"""Day 1 part 1 """
def frequency(day, part):
    print(f"day {day} part {part} :\n")
    file = open(f"inputs/Day{day}part{part}.txt", "r")
    """create variable"""
    total = 0
    """for every number add or subtract it from total ( numerical data might be - )"""
    for line in file:
        total += int(line)
    file.close()
    """print total"""
    print(f"Resulting frequency is {total}\n")

"""Day 1 part 2 """
def repFrequency(day, part):
    """create 2 lists and total
    Should do this again using sets. List iteration takes way too long"""
    total = 0
    pastfrequencies = []
    pastfrequencies.append(total)
    """populate frequencies"""
    frequency = get_data(day, part)
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
    print(f"First frequency the device reaches twice is :{total}\n")

"""Day 2 part 1 """
def letterMultible(day, part):
    """create lists and variables"""
    boxArt = get_data(day, part)
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
        twoDigs += 1 if two else 0
        threeDigs += 1 if three else 0

    return print(f" found threeDigs: {threeDigs} and twoDigs: {twoDigs} checksum is: {threeDigs * twoDigs}\n")

"""Day 2 part 2 """
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
            if (sum(inst1 != inst2 for inst1, inst2 in zip(box, checkThis))) == 1:
                """Stupid way to manipulate set&lists to string"""
                remove = ''.join(set(checkThis) ^ set(box))
                correct = box.replace("" + remove, "")
                return print(f"Common letters between two corresponding box ID:s are:{correct}\n")

"""Day 3 part 1"""
def fabricCut(day, part):
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
        positions = tuple(map(int, postitionInfo.match(claimList[i]).groups()))
        for j in range(i + 1, len(claimList)):
            otherPositions = tuple(map(int, postitionInfo.match(claimList[j]).groups()))
            """Check the funciton for info"""
            calculateOverlap(positions, otherPositions, CountedPositions)
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
    print(f"overlap count: {overlapCount} once seen count: {firstCount}\n")
    return

"""Day 3 part 2"""
def noOverlap(day, part):
    List = get_data(day, part)
    Dataposition = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
    setOfElves = set()
    for i in range(len(List)):
        Data = tuple(map(int, Dataposition.match(List[i]).groups()))
        setOfElves.add(Data)
    id = checkNoOverlap(setOfElves)
    print(f"There is no conflict with elf id: {id}\n")

    return

"""Day 4 part 1"""
def sleepingGuard(day, part):
    Guardlist = sorted(get_data(day, part))
    SleepingGuard = collectRelevantData(Guardlist)
    most_asleep = max(SleepingGuard, key = lambda e: e["sleeptime"])
    minute = max(most_asleep["minutesInSleep"],key=most_asleep["minutesInSleep"].get)
    checksum = int(most_asleep["id"]) * int(minute)

    print(f"most asleep was guard id {most_asleep['id']} "
          f"He slept for {most_asleep['sleeptime']} "
          f"most asleep on minute {minute} "
          f" Check sum should be: {checksum}\n")

"""Day 4 part 2"""
def WhenGuardSleeps(day, part):
    SleepingGuard = collectRelevantData(sorted(get_data(day, part)))
    most_asleep = None
    max_count = -1

    for guard in SleepingGuard:
        if not guard["minutesInSleep"]:
            continue  # skip guards who never slept
        minute = max(guard["minutesInSleep"], key=guard["minutesInSleep"].get)
        count = guard["minutesInSleep"][minute]

        if count > max_count:
            max_count = count
            most_asleep = {
                "Guard": guard["id"],
                "minute": minute,
                "howMany": count,
                "checksum": guard["id"] * minute,
            }
    print(f"of all guards, Guard Id {most_asleep['Guard']} slept most frequently on the same minute ({most_asleep['minute']}).\n"
          f"Counted {most_asleep['howMany']} times check sum should be: {most_asleep['checksum']}\n")

"""Day 5 part 1"""
def SuitPolymers(day, part):
    data = get_data(day, part)
    inputs = ""
    if len(data) == 1:
        inputs = data[0].strip()
    else:
        inputs = ''.join(line.strip() for line in data if line.strip())
    CorrectOnes = prosessingString(inputs)

    print(f"There are {len(CorrectOnes)} units of polymer left after scan.\n")
    return

"""Day 5 part 2"""
def MinimumPolymers(day, part):
    data = get_data(day, part)
    Letters = set()
    output = []
    if len(data) == 1:
        inputs = data[0].strip()
    else:
        inputs = ''.join(line.strip() for line in data if line.strip())
    Letters = set(inputs)
    for letter in Letters:
        test = inputs.replace(letter.upper(), "").replace(letter.lower(), "")
        CorrectOnes = prosessingString(test)
        output.append({
            "Letter" : letter,
            "Length" : len(CorrectOnes)
        })
    minimum = min(output, key=lambda e: e["Length"])
    print(f'removing letter {minimum["Letter"]} gives {minimum["Length"]} units of polymer left after scan.\n')



    return

"""Day 6 part 1"""
def ManhattanGeoLocation(day, part):
    # Get the puzzle input for the given day and part
    data = get_data(day, part)

    # Convert the input strings to a NumPy array of coordinates
    Locations = np.array([list(map(int, item.split(','))) for item in data])

    # Margin to extend the bounding box to handle edges
    margin = 1

    # Find the min and max coordinates for X and Y, with margin
    minX, maxX = Locations[:, 0].min() - margin, Locations[:, 0].max() + margin
    minY, maxY = Locations[:, 0].min() - margin, Locations[:, 0].max() + margin

    # Create a 2D grid of X and Y coordinates
    GridX, GridY = np.meshgrid(np.arange(minX, maxX + 1), np.arange(minY, maxY + 1))

    # Compute the Manhattan distance from each grid point to each location
    differences = (
            np.abs(GridX - Locations[:, 0][:, None, None]) +
            np.abs(GridY - Locations[:, 1][:, None, None])
    )

    # Find the minimum distance for each grid point
    min_dists = differences.min(axis=0)

    # Assign each grid point to the index of the closest location
    owner = np.argmin(differences, axis=0)

    # Identify grid points where there is a tie (multiple locations equally close)
    ties = (differences == min_dists)
    tieCount = np.sum(ties, axis=0)

    # Mark grid points with ties as -1 (no owner)
    owner[tieCount > 1] = -1

    # Collect the owners that appear on the edges of the grid
    edges = np.concatenate([
        owner[0, :],  # top edge
        owner[-1, :],  # bottom edge
        owner[:, 0],  # left edge
        owner[:, -1],  # right edge
    ])
    # Get unique edge owners (these locations have infinite area)
    infinitSrc = np.unique(edges[edges >= 0])

    # Count the area of each location by summing grid points owned
    Area = np.array([
        np.sum(owner == i) for i in range(Locations.shape[0])
    ], dtype=int)

    # Remove the areas of locations with infinite regions
    Area[infinitSrc] = 0

    # Find the largest finite area
    Result = np.max(Area)
    print(f"Largest area is {Result}")


def EvenMoreManhattanCrap(day,part):
    # Get the puzzle input for the given day and part
    data = get_data(day, part)

    # Convert the input strings to a NumPy array of coordinates
    Locations = np.array([list(map(int, item.split(','))) for item in data])

    # Margin to extend the bounding box to handle edges. Treshold for the area
    marginaali = 1
    treshold = 10000
    # Find the min and max coordinates for X and Y, with margin
    minX, maxX = Locations[:, 0].min() - marginaali, Locations[:, 0].max() + marginaali
    minY, maxY = Locations[:, 0].min() - marginaali, Locations[:, 0].max() + marginaali

    # Create a 2D grid of X and Y coordinates
    GridX, GridY = np.meshgrid(np.arange(minX, maxX + 1), np.arange(minY, maxY + 1))

    # Compute the Manhattan distance from each grid point to each location
    differences = (
            np.abs(GridX - Locations[:, 0][:, None, None]) +
            np.abs(GridY - Locations[:, 1][:, None, None])
    )
    dfferenceSum = differences.sum(axis=0)

    region = dfferenceSum < treshold

    Area = np.sum(region).astype(int)
    return print(f"Largest area is {Area}")


def sledgeBuildingInstructions(day,part):
    data = get_data(day, part)
    steps = defaultdict(set)
    pattern = re.compile(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin")

    for line in data:
        match = pattern.match(line.strip())
        if match:
            before, after = match.groups()
            steps[after].add(before)
            steps[before]

    Available = [letter for letter, deps in steps.items() if not deps]
    heapq.heapify(Available)
    word = ""
    while Available:
        letter = heapq.heappop(Available)
        word += letter

        for key in steps:
            if letter in steps[key]:
                steps[key].remove(letter)
                if not steps[key]:
                    heapq.heappush(Available, key)

    return print(word)

def moreElfs(day, part):
    data = get_data(day, part)
    time = 0
    word = ""
    workers = list()
    steps = defaultdict(set)
    pattern = re.compile(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin")

    for line in data:
        match = pattern.match(line.strip())
        if match:
            before, after = match.groups()
            steps[after].add(before)
            steps[before]

    Available = [letter for letter, deps in steps.items() if not deps]
    heapq.heapify(Available)
    while steps:
        if workers:
            heapq.heapify(workers)
            stepTime, letter = min(workers, key=lambda x: x[0])
            finishedWork = []
            newWork = []
            time += stepTime
            print(f" letter = {letter} stepTime = {stepTime}")

            for workertime, workerletter in workers:
                workertime -= stepTime
                if workertime == 0:
                    finishedWork.append(workerletter)
                else:
                    newWork.append((workertime, workerletter))
                print(workers)
            workers = newWork
            for letter in finishedWork:
                word += letter
                for key in list(steps.keys()):
                    if letter in steps[key]:
                        steps[key].remove(letter)
                        if not steps[key]:
                            heapq.heappush(Available, key)
                    if not steps[key] and key in word:
                        print("removing ", key)
                        del steps[key]
            newlyAssigned = []
            while len(workers) + len(newlyAssigned) < 5 and Available:
                letterPair = heapq.heappop(Available)
                duration = 60 + (ord(letterPair[0]) - 64)
                newlyAssigned.append((duration, letterPair))
            workers.extend(newlyAssigned)
        else:
            while len(workers) < 5 and Available:
                letterPair = heapq.heappop(Available)
                duration = 60 + ord(letterPair[0]) - 64
                workers.append((duration, letterPair))
    return print(f"Sledge building took {time} seconds.\n")
"""
Map days and parts to functions
Puzzle information and puzzle inputs can be found on inputs folder
"""
actions = {
    (1, 1): frequency,
    (1, 2): repFrequency,
    (2, 1): letterMultible,
    (2, 2): letterDifference,
    (3, 1): fabricCut,
    (3, 2): noOverlap,
    (4, 1): sleepingGuard,
    (4, 2): WhenGuardSleeps,
    (5, 1): SuitPolymers,
    (5, 2): MinimumPolymers,
    (6, 1): ManhattanGeoLocation,
    (6, 2): EvenMoreManhattanCrap,
    (7, 1): sledgeBuildingInstructions,
    (7, 2): moreElfs,
}


def main():
    """Which part are you doing?"""
    day = 7
    part = 2
    """go through the days after previously set"""
    while day <= 25:
        """Get the day from dict"""
        func = actions.get((day, part))
        """if found run it"""
        if func:
            func(day, part)
        """switch between 1 and 2"""
        part = 2 if part == 1 else 1
        if part == 1:
            day += 1


main()
