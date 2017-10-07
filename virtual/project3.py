##############################################
# ARTUR GRIGORYAN
#
# NO-TLB:       python3 project3.py input1.txt input2.txt False > 62661627_NO_TLB.txt
# WITH_TLB:     python3 project3.py input1.txt input2.txt True > 62661627_WITH_TLB.txt
##############################################
import re
import sys

PM = {}
BM = {}
TLB = {}

def main(input1, input2, input3):
    # initializing TLB
    for i in range(4):
        item = {'LRU': i, 'sp': -2, 'f': -1}
        TLB[i] = item
    # initializing BM
    for i in range(1024):
        BM[i] = 0
    BM[0] = 1 # setting first for ST
    # initializing PM
    for i in range(524288):
        PM[i] = 0
    readLine1(input1)
    readLine2(input2)
    vaInput(input3)


# Initializing ST
def readLine1(input):
    sf = list()
    inputArray = re.split(' ', input)
    for s, f in zip(inputArray[::2], inputArray[1::2]):
        sf.append([s, f])
    for item in sf:
        s = int(item[0])
        f = int(item[1])
        PM[s] = f
        # setting BM
        BM[f/512] = 1
        BM[f/512 + 1] = 1


# Initializing PT
def readLine2(input):
    global BM
    psf = list()
    inputArray = re.split(' ', input)
    for p, s, f in zip(inputArray[::3], inputArray[1::3], inputArray[2::3]):
        psf.append([p, s, f])
    for item in psf:
        p = int(item[0])
        s = int(item[1])
        f = int(item[2])
        PM[PM[s]+p] = f
        # setting BM
        BM[f/512] = 1


def vaInput(input):
    # list of Virtual Addresses
    va = list()
    inputArray = re.split(' ', input)
    for r, spw in zip(inputArray[::2], inputArray[1::2]):
        va.append([r,spw])

    for item in va:
        spw = vaTranslate(int(item[1]))
        s = spw[0]
        p = spw[1]
        w = spw[2]

        # read
        if(int(item[0]) == 0):
            if enableTLB:
                tlb = checkTLB(s,p)
            else:
                tlb = ''
            try:
                if(PM[s] == -1):
                    raise Exception('pf')
                if(PM[s] == 0):
                    raise Exception('err')
                if(PM[PM[s] + p] == -1):
                    raise Exception('pf')
                if(PM[PM[s] + p] == 0):
                    raise Exception('err')
                if tlb != 'h ':
                    updateTLB(s,p)
                print(tlb + str(PM[PM[s] + p] + w), end=' ')
            except Exception as e:
                print(tlb + str(e), end=' ')

        # write
        elif(int(item[0]) == 1):
            if enableTLB:
                tlb = checkTLB(s, p)
            else:
                tlb = ''
            try:
                if(PM[s] == -1):
                    raise Exception('pf')
                if(PM[s] == 0):
                    PM[s] = find2Slot()
                if(PM[PM[s] + p] == -1):
                    raise Exception('pf')
                if(PM[PM[s] + p] == 0):
                    PM[PM[s] + p] = find1Slot()
                if tlb != 'h ':
                    updateTLB(s,p)
                print(tlb + str(PM[PM[s] + p] + w), end=' ')
            except Exception as e:
                print(tlb + str(e), end=' ')


def vaTranslate(spw):
    s = (spw >> 19) & 511
    p = (spw >> 9) & 1023
    w = spw & 511
    return [s,p,w]


def find1Slot():
    for i in BM:
        if(BM[i] == 0):
            BM[i] = 1
            return i*512


def find2Slot():
    for i in BM:
        if(BM[i] == 0 and BM[i+1] == 0):
            BM[i] = 1
            BM[i+1] = 1
            return i*512


def checkTLB(s, p):
    for i in TLB:
        item = TLB[i]
        if(item['sp'] == (s << 10) + p):
            return 'h '
    return 'm '


def updateTLB(s,p):
    global PM
    flag = False
    for i in TLB:
        if flag:
            continue
        item = TLB[i]
        if (item['LRU'] == 0):
            item['LRU'] = 3
            item['sp'] = (s << 10) + p
            item['f'] = PM[PM[s] + p]
            for j in TLB:
                item2 = TLB[j]
                if (item2 != item):
                    item2['LRU'] -= 1
                if (item2['LRU'] == -1):
                    item2['LRU'] = 0
            flag = True


with open(sys.argv[1], 'r') as file:
    content = file.readlines()
content = [x.strip() for x in content]
input1 = content[0]
input2 = content[1]

with open(sys.argv[2], 'r') as file:
    content = file.readlines()
content = [x.strip() for x in content]
input3 = content[0]

if(sys.argv[3] == 'True' or sys.argv[3] == 't' or sys.argv[3] == 1):
    enableTLB = True
else:
    enableTLB = False

main(input1, input2, input3)