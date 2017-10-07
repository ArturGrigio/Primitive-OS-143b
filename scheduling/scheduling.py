##############################################
#
# ARTUR GRIGORYAN
# UCI ID: 62661627
#
#
#
#
# run: truncate -s 0 output.txt && for i in {0..9}; do python3 scheduling.py $i.txt >> output.txt; done
#
#
#
##############################################

import copy
import sys
from decimal import Decimal

TIMEINTERVAL = 1
CURRTIME = 0
PROCESSES = []
CURRPROCESS = None

def main():
    original = []
    command = input()
    it = iter(command.split(' '))
    i = 0
    for x, y in zip(it, it):
        original.append(Process(i, int(x), int(y)))
        i += 1
    runSchedulers(original)


def inputFile(command):
    original = []
    it = iter(command.split(' '))
    i = 0
    for x, y in zip(it, it):
        original.append(Process(i, int(x), int(y)))
        i += 1
    runSchedulers(original)


def runSchedulers(original):
    global PROCESSES
    global CURRTIME
    CURRTIME = 0
    PROCESSES = copy.deepcopy(original)
    displayStats(FIFO())

    CURRTIME = 0
    PROCESSES = copy.deepcopy(original)
    displayStats(SJF())

    CURRTIME = 0
    PROCESSES = copy.deepcopy(original)
    displayStats(SRT())

    CURRTIME = 0
    PROCESSES = copy.deepcopy(original)
    displayStats(MLF())


def FIFO():
    global PROCESSES
    global CURRPROCESS
    global CURRTIME
    retVal = []
    dummy = Process(sys.maxsize, sys.maxsize, sys.maxsize, 1, True)
    CURRPROCESS = dummy
    while PROCESSES:
        for p in PROCESSES:
            if p.start < CURRPROCESS.start and p.start <= CURRTIME:
                CURRPROCESS = p
            if p.start == CURRPROCESS.start and p.start <= CURRTIME:
                CURRPROCESS = p if p.id < CURRPROCESS.id else CURRPROCESS
        while CURRPROCESS.time:
            CURRPROCESS.time -= clock()
            if CURRPROCESS.dummy:
                break
        if not CURRPROCESS.dummy:
            CURRPROCESS.completed = CURRTIME
            retVal.append(CURRPROCESS)
            PROCESSES.remove(CURRPROCESS)
            CURRPROCESS = dummy
    return retVal


def SJF():
    global CURRPROCESS
    global CURRTIME
    global PROCESSES
    retVal = []
    dummy = Process(sys.maxsize, sys.maxsize, sys.maxsize, 1, True)
    CURRPROCESS = dummy
    while PROCESSES:
        for p in PROCESSES:
            if p.time < CURRPROCESS.time and p.start <= CURRTIME:
                CURRPROCESS = p
            if p.time == CURRPROCESS.time and p.start <= CURRTIME:
                CURRPROCESS = p if p.id < CURRPROCESS.id else CURRPROCESS
        while(CURRPROCESS.time):
            CURRPROCESS.time -= clock()
            if CURRPROCESS.dummy:
                break
        if not CURRPROCESS.dummy:
            CURRPROCESS.completed = CURRTIME
            retVal.append(CURRPROCESS)
            PROCESSES.remove(CURRPROCESS)
            CURRPROCESS = dummy
    return retVal


def SRT():
    global CURRPROCESS
    global CURRTIME
    global PROCESSES
    retVal = []
    dummy = Process(sys.maxsize, sys.maxsize, sys.maxsize, 1, True)
    CURRPROCESS = dummy
    while PROCESSES:
        while CURRPROCESS.time:
            srtPreempt()
            CURRPROCESS.time -= clock()
        CURRPROCESS.completed = CURRTIME
        retVal.append(CURRPROCESS)
        PROCESSES.remove(CURRPROCESS)
        CURRPROCESS = dummy
    return retVal


def MLF():
    global CURRPROCESS
    global CURRTIME
    global PROCESSES
    retVal = []
    dummy = Process(sys.maxsize, sys.maxsize, sys.maxsize, 1, True)
    CURRPROCESS = dummy
    while PROCESSES:
        mlfCleanup(retVal)
        mlfPreempt()
        for i in range(CURRPROCESS.originalMLFblocks):
            if(CURRPROCESS.time > 0 and CURRPROCESS.MLFblocks > 0):
                CURRPROCESS.time -= clock()
                CURRPROCESS.MLFblocks -= 1
            flag = False
            for p in PROCESSES:
                if(p.start == CURRTIME):
                    flag = True
            if flag:
                break
        if CURRPROCESS.MLFblocks == 0:
            CURRPROCESS.decreasePriority()
    return retVal


def displayStats(processes):
    processes = sorted(processes, key=lambda x: x.id)
    total = 0
    for p in processes:
        total += (p.completed - p.start)
    print(round(Decimal(total/len(processes)), 2), end=" ")
    for p in processes:
        print(p.completed-p.start, end=" ")
    print("")


def srtPreempt():
    global PROCESSES
    global CURRPROCESS
    global CURRTIME
    for p in PROCESSES:
        if(p.start <= CURRTIME and p.time < CURRPROCESS.time):
            CURRPROCESS = p


def mlfPreempt():
    global PROCESSES
    global CURRPROCESS
    global CURRTIME
    for p in PROCESSES:
        if (p.priority > CURRPROCESS.priority and p.start <= CURRTIME):
            CURRPROCESS = p
        elif (p.priority == CURRPROCESS.priority and p.start <= CURRTIME and p.id < CURRPROCESS.id):
            CURRPROCESS = p


def mlfCleanup(retVal):
    global PROCESSES
    global CURRPROCESS
    dummy = Process(sys.maxsize, sys.maxsize, sys.maxsize, 1, True)
    for p in PROCESSES:
        if (p.time == 0 and CURRPROCESS.dummy != True):
            CURRPROCESS.completed = CURRTIME
            retVal.append(CURRPROCESS)
            PROCESSES.remove(CURRPROCESS)
            CURRPROCESS = dummy


def clock():
    global CURRPROCESS
    global PROCESSES
    global CURRTIME
    global TIMEINTERVAL
    for p in PROCESSES:
        if(p != CURRPROCESS and p.start <= CURRTIME and CURRPROCESS.dummy != True):
            p.wait += TIMEINTERVAL
    CURRTIME += TIMEINTERVAL
    return TIMEINTERVAL



## PROCESS CLASS
class Process:
    def __init__(self, id, start, time, priority = 5, dummy = False):
        self.id = id
        self.start = start
        self.time = time
        self.wait = 0
        self.completed = 0
        self.priority = priority
        self.MLFblocks = 1
        self.originalMLFblocks = 1
        self.dummy = dummy

    def decreasePriority(self):
        self.priority = self.priority-1 if self.priority >= 1 else 1
        self.MLFblocks = 2 * self.originalMLFblocks
        self.originalMLFblocks *= 2

    def print(self):
        print("id:",self.id," start:",self.start," time:",self.time," wait:",self.wait," completed:",self.completed)


# main()

with open(sys.argv[1], 'r') as file:
    content = file.readlines()
inputFile(content[0])
