import re

PM = {}
BM = {}

def main():
    # initializing BM
    for i in range(1024):
        if(i == 0):
            BM[i] = 1
        else:
            BM[i] = 0
    # initializing PM
    for i in range(524288):
        PM[i] = 0
    readLine1(input())
    readLine2(input())
    vaInput(input())


# Initializing ST
def readLine1(input):
    sf = list()
    inputArray = re.split(' ', input)
    for s, f in zip(inputArray[::2], inputArray[1::2]):
        sf.append([s,f])
    for item in sf:
        PM[int(item[0])] = int(item[1])
        findSlots(int(item[1]))


# Initializing PT
def readLine2(input):
    global BM
    psf = list()
    inputArray = re.split(' ', input)
    for p, s, f in zip(inputArray[::3], inputArray[1::3], inputArray[2::3]):
        psf.append([p,s,f])
    for item in psf:
        PM[PM[int(item[1])] + int(item[0])] = int(item[2])


# VA input
def vaInput(input):
    # list of Virtual Addresses
    va = list()
    inputArray = re.split(' ', input)
    for r, spw in zip(inputArray[::2], inputArray[1::2]):
        va.append([r,spw])

    for item in va:
        if(int(item[0]) == 0): #read
            spw = vaTranslate(int(item[1]))
            try:
                if(PM[spw[0]] == -1 or PM[spw[1]] == -1):
                    raise Exception('pf')
                elif(PM[spw[0]] == 0):
                    raise Exception('err')
                else:
                    print(PM[PM[spw[0]]+spw[1]]+spw[2], end=" ")
            except Exception as e:
                print(str(e), end=" ")

        elif(int(item[0]) == 1): #write
            spw = vaTranslate(int(item[1]))
            try:
                if (PM[spw[0]] == -1 or PM[spw[1]] == -1):
                    raise Exception('pf')
                elif (PM[spw[0]] == 0):
                    PM[spw[0]] = findSlots()
                elif(PM[PM[spw[0]]+spw[1]] == 0):
                    PM[PM[spw[0]]+spw[1]] = findSlots()
                else:
                    if(PM[PM[spw[0]] + spw[1]] + spw[2] == -1):
                        raise Exception('pf')
                    else:
                        print(PM[PM[spw[0]] + spw[1]] + spw[2], end=" ")
            except Exception as e:
                print(str(e), end=" ")

# VA Translate
def vaTranslate(spw):
    s = (spw >> 19) & 511
    p = (spw >> 9) & 1023
    w = spw & 511
    return [s,p,w]

# find 2 Empty Slots on BM
def findSlots(address = None):
    if address:
        BM[address/512] = 1
        BM[address/512 + 1] = 1
        print(BM)
    else:
        for i in BM:
            print(i)


# def findSlots(address = None, slots = 1):
#     if address:
#         if(slots == 2):
#             if(BM[address/512] == 0 and BM[address/512 +1] == 0):
#                 BM[address/512] = 1
#                 BM[address/512 + 1] = 1
#                 return BM[address/512] * 512
#         else:
#             return BM[address/512] * 512
#
#     for i in BM:
#         if(slots == 1):
#             if(BM[i] == 0):
#                 BM[i] = 1
#                 return BM[i]*512
#         elif(slots == 2):
#             if(BM[i] == 0 and BM[i+1] == 0):
#                 BM[i] = 1
#                 BM[i+1] = 1
#                 return BM[i]*512


class Bm:
    def __init__(self):
        self.bitmap = list()
        # initializing BIT-MAP
        for i in range(1024):
            self.bitmap[i] = 0

    def findSlots(self, address=None, slots=1):
        if(address):
            if(slots == 2):
                if(self.bitmap[address/512] == 0 and self.bitmap[address/512 +1] == 0):
                    self.bitmap[address/512] = 1
                    self.bitmap[address / 512 + 1] = 1
                    return self.bitmap[address/512]
                return -1
            else:
                if(self.bitmap[address/512] == 0):
                    self.bitmap[address / 512] = 1
                    return self.bitmap[address/512]
                return -1
        else:
            if (slots == 2):
                for i in self.bitmap:
                    if (self.bitmap[i] == 0 and self.bitmap[i + 1] == 0):
                        self.bitmap[i] = 1
                        self.bitmap[i+1] = 1
                        return self.bitmap[i]*512
                return -1
            else:
                for i in self.bitmap:
                    if (self.bitmap[i] == 0):
                        self.bitmap[i] = 1
                        return self.bitmap[i]*512
                return -1

    def getSlot(self, address):
        return self.bitmap[address/512]

main()