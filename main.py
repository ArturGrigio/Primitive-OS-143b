##############################################
#
# ARTUR GRIGORYAN
# UCI ID: 62661627
#
#
#
#
# run: python3 vm.py input.txt >> output.txt
#
#
#
##############################################

import re
import sys
import collections

currProcess = None
resources = None
RL = None
processes = {}
errored = False

def newStartup():
    global currProcess
    global resources
    global RL
    global processes
    global errored
    errored = False
    processes = {}
    RL = {2: [], 1: [], 0: []}
    currProcess = Process('init', 0)
    currProcess.status = 'running'
    RL[0].append(currProcess)
    resources = {'R1': Resource(1), 'R2': Resource(2), 'R3': Resource(3), 'R4': Resource(4)}
    print(currProcess.PID, end="")

def main():
    newStartup()
    while(True):
        command = input()
        execCommand(re.split(' |, |,', command))

def execCommand(params):
    global RL
    global currProcess
    global resources
    global processes
    global errored
    try:
        if(params[0] == 'init'):
            newStartup()
        elif (params[0] == 'cr'):
            if params[1] in processes:
                raise Exception('Tried to create process with same name.')
            priority = int(params[2])
            if(priority < 1):
                raise Exception('Tried to create priority 0 process.')
            processes[params[1]] = currProcess.create(params[1], priority)
            scheduler()
        elif (params[0] == 'de'):
            if (currProcess.PID == 'init'):
                raise Exception('Tried to Destroy init.')
            if(currProcess.checkTree(params[1])):
                processes[params[1]].destroy()
                del processes[params[1]]
            else:
                raise Exception('Tried to destroy non-relative process')
            scheduler()
        elif (params[0] == 'req'):
            if(currProcess.PID == 'init'):
                raise Exception('\'init\' tried to request a Resource.')
            currProcess.request(params[1], int(params[2]))
            scheduler()
        elif (params[0] == 'rel'):
            if (currProcess.PID == 'init'):
                raise Exception('\'init\' tried to release a Resource.')
            currProcess.release(params[1], int(params[2]))
            scheduler()
        elif (params[0] == 'to'):
            currProcess.timeout()
            scheduler()
        elif(params[0] == 'open'):
            with open(params[1]) as f:
                content = f.readlines()
            content = [x.strip() for x in content]
            for each in content:
                execCommand(re.split(' |, |,', each))
        elif(params[0] == 'CP'):
            print('Current Process: %s, Priority: %s' % (currProcess.PID, currProcess.priority))
        elif(params[0] == 'RL'):
            print(RL)
        elif(params[0] == 'RE'):
            for res in resources:
                print(res+": "+str(resources[res].instances)+" waitlist: "+str(resources[res].waitlist))
        elif(params[0] == "" or params[0] == ""):
            print("")
        else:
            raise Exception('Bad Command')
    except:
        print(" error", end="")
        errored = True

###########
# Scheduler
###########
def scheduler():
    global currProcess
    notFinished = True
    i = 2
    while(notFinished and i>=0):
        list = RL[i]
        for process in list:
            if(currProcess == None or currProcess.priority < process.priority or currProcess.status != "running"):
                if(currProcess and currProcess.status != 'blocked'):
                    currProcess.status = "ready"
                    temp = currProcess
                    del RL[currProcess.priority][0]
                    RL[temp.priority].append(temp)
                process.status = "running"
                currProcess = process
                notFinished = False
        i -= 1
    if not errored:
        print(" "+currProcess.PID, end="")




###############
# Process Class
###############
class Process:
    def __init__(self, PID, priority):
        self.PID = PID
        self.priority = priority
        self.otherResources = {}
        self.status = "ready"
        self.child = []
        self.parent = None

    def create(self, PID, priority):
        childProcess = Process(PID, priority)
        childProcess.parent = self
        self.child.append(childProcess)
        RL[priority].append(childProcess)
        return childProcess

    def checkTree(self, PID):
        retVal = False
        if self.PID == PID:
            return True
        else:
            for child in self.child:
                retVal = child.checkTree(PID)
                if retVal:
                    return True
        return False

    def destroy(self):
        global currProcess
        self.status = None
        for child in self.child.copy():
            child.destroy()
        if self in RL[self.priority]:
            RL[self.priority].remove(self)
        self.parent.child.remove(self)
        self.parent = None
        for res in self.otherResources:
            res.increment(self.otherResources[res])
            res.resourceReallocate()
        if(currProcess == self):
            currProcess = None
        temp = self
        del self
        return temp

    def request(self, resource, count):
        r = resources[resource]
        if(r.instances-count >= 0):
            r.instances -= count
            if r in self.otherResources:
                self.otherResources[r] += count
            else:
                self.otherResources[r] = count
        elif(r.initialInstances-count < 0 or (r in self.otherResources and self.otherResources[r]+count > r.initialInstances)):
            raise Exception("Requested more than Possible")
        else:
            self.status = "blocked"
            if self in r.waitlist:
                r.waitlist[self] += count
                if(r.waitlist[self] > r.initialInstances):
                    raise Exception("Requested more than Possible")
            else:
                r.waitlist[self] = count
            RL[self.priority].remove(self)
        return self


    def release(self, resource, count):
        r = resources[resource]
        # Checkingthe resource count
        if(self.otherResources[r] - count < 0):
            raise Exception('Releasing more than Have')
        elif(self.otherResources[r] - count == 0):
            del self.otherResources[r]
            r.increment(count)
            if(self.status == "blocked"):
                self.status = "ready"
                RL[self.priority].append(self)
        else:
            self.otherResources[r] -= count
            r.increment(count)
        r.resourceReallocate()
        return self


    def timeout(self):
        global currProcess
        temp = currProcess
        del RL[currProcess.priority][0]
        RL[temp.priority].append(temp)
        currProcess = None
        temp.status = "ready"


################
# Resource Class
################
class Resource:
    def __init__(self, instances):
        self.initialInstances = instances
        self.instances = self.initialInstances
        self.waitlist = collections.OrderedDict()

    def increment(self, count):
        if(count + self.instances > self.initialInstances):
            raise Exception('Release more than the Resource originally had')
        else:
            self.instances += count
            return self

    def resourceReallocate(self):
        noStarvation = True
        for process in self.waitlist:
            if(noStarvation):
                if(self.waitlist[process] == self.instances):
                    if self in process.otherResources:
                        process.otherResources[self] += self.waitlist[process]
                    else:
                        process.otherResources[self] = self.waitlist[process]
                    self.instances = 0
                    del self.waitlist[process]
                    RL[process.priority].append(process)
                elif(self.waitlist[process] < self.instances):
                    if self in process.otherResources:
                        process.otherResources[self] += self.waitlist[process]
                    else:
                        process.otherResources[self] = self.waitlist[process]
                    self.instances -= self.waitlist[process]
                    del self.waitlist[process]
                    RL[process.priority].append(process)
                noStarvation = False



main()

# with open(sys.argv[1], 'r') as file:
#     content = file.readlines()
# content = [x.strip() for x in content]
# newStartup()
# for each in content:
#     execCommand(re.split(' |, |,', each))