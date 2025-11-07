import os
import re
import numpy as np
from classes.coordinates import *
from collections import defaultdict, deque
from datetime import datetime


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
            Guard_Id, sw, sh, wl, hl = checkThis
            aid, asw, ash, awl, ahl = measures
            overlapW = min(sw + wl, asw + awl) - max(sw, asw)
            overlapH = min(sh + hl, ash + ahl) - max(sh, ash)
            if overlapW > 0 and overlapH > 0:
                """when there is overlap we can set the flag as False"""
                noConflict = False
                break
        if noConflict:
            """When there is no conflict return the id and stop going through since there was only one"""
            return Guard_Id

    return 0

def calculateManhattanDistance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def collectRelevantData(listing):
    sleepStarts = datetime.now()
    guard_id = 0
    SleepingGuard = defaultdict(lambda: {"sleeptime": 0, "minutesInSleep": defaultdict(int)})
    lineInfo = re.compile(r'^\[(?P<ts>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\]\s*(?P<event>.+)$')
    for line in listing:
        event = lineInfo.match(line).groups()
        timestamp = datetime.strptime(event[0], "%Y-%m-%d %H:%M")
        minute = timestamp.minute
        if event:
            if re.search(r"\d+", event[1]):
                guard_id  = int(re.search(r"\d+", event[1]).group())
            # when falling a sleep next has to be wake up so save minutes when sleeping: (wake-up time -1) - fall asleep
            elif event[1] == "falls asleep":
                sleepStarts = timestamp.minute
            else:
                Wakeup = int(minute)
                sleepStartsminute = int(sleepStarts)
                sleeptime = int(Wakeup) - sleepStartsminute
                guard = SleepingGuard[guard_id]
                for minute in range(sleepStartsminute, Wakeup):
                    guard["minutesInSleep"][minute] += 1
                guard["sleeptime"] += sleeptime
    return [{"id": gid, **data} for gid, data in SleepingGuard.items()]

def calculateOverlap(info1, info2, counted):
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
    id, sw, sh, wl, hl = info1
    aid, asw, ash, awl, ahl = info2
    """calculate if given measures overlap result in these are - if they don't and + if they do"""
    overlapW = min(sw + wl, asw + awl) - max(sw, asw)
    overlapH = min(sh + hl, ash + ahl) - max(sh, ash)
    if overlapW > 0 and overlapH > 0:
        """when there is overlap calculate the starting point and add resulting values to list
        for later use"""
        overlapstartW = max(sw, asw)
        overlapstartH = max(sh, ash)
        for i in range(overlapstartW, overlapstartW + overlapW):
            for j in range(overlapstartH, overlapstartH + overlapH):
                counted.append((i, j))
    else:
        return

def get_data(day, part):
    """Get input data from file"""
    path = f"inputs/Day{day}part{part}.txt"
    print(f"day {day} part {part} :\n")
    size = os.path.getsize(path)
    print(f"Converting inputs from file. File size: {size} bytes")
    if not os.path.exists(path):
        print(f" File not found: {path}")
        return None
    data = []


    file = open(f"inputs/Day{day}part{part}.txt", "r", encoding="utf-8")
    if size < 100000:
        for line in file:
            line = line.strip()
            if line.isdigit():
                data.append(int(line))
            else:
                data.append(line)
        file.close()
    else:
        """NEed to figure this out later"""
        print("File Size is", file.tell(), "bytes returning it in parts")

    return data

def prosessingString(data):
    RemoveDud = deque(data)
    CorrectOnes = deque()
    i = 0
    for dublic in RemoveDud:
        if CorrectOnes and CorrectOnes[-1].lower() == dublic.lower() and CorrectOnes[-1] != dublic:
            CorrectOnes.pop()
        else:
            CorrectOnes.append(dublic)
    return CorrectOnes