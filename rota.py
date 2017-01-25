from random import randint, choice

from workers import *
from console_interface import *



class Shift:
    def __init__(self, name, minNumOfWorkers=1, maxNumOfWorkers=10, optimalNumOfWorkers=3, manned=False, number=0):
        self.name = name
        self.minNumOfWorkers = minNumOfWorkers
        self.maxNumOfWorkers = maxNumOfWorkers
        self.optimalNumOfWorkers = optimalNumOfWorkers
        self.manned = manned
        self.workers = []
        self.number = number

    def __str__(self):
        return self.name + ": " + str([worker.name for worker in self.workers])

    def checkIfManned(self, optimal=False):
        if len(self.workers) == 1 and self.workers[0].independent == False:
            return False
        if optimal:
            return len([worker for worker in self.workers]) >= self.optimalNumOfWorkers
        else:
            return len([worker for worker in self.workers]) >= self.minNumOfWorkers



class Rota:
    def __init__(self, name, emptyCalendar, staff):
        self.name = name
        self.calendar = []
        self.emptyCalendar = emptyCalendar
        self.staff = staff
        self.collisions = 0
        self.collisionsOptimal = 0

        # fill in rota calendar with empty shift objects for each day, each shift object is a separate instance
        for dayNum in range(len(emptyCalendar)):
            day = emptyCalendar[dayNum]
            shifts = []
            shiftGroup = shiftDefinition[day]

            shiftID = 0
            for shiftType in shiftGroup:
                shiftID += 1
                shifts.append(Shift(name=shiftType[0], minNumOfWorkers=shiftType[1], maxNumOfWorkers=shiftType[2], optimalNumOfWorkers=shiftType[3], manned=shiftType[4], number=shiftID))



            self.calendar.append(shifts)



    def reset(self):
        for worker in self.staff:
            worker.clearCalendar()

        self.calendar = []



    def addEntry(self, worker, dayNum, shiftNum):
        shift = self.calendar[dayNum][shiftNum-1]
        shift.workers.append(worker)

        worker.calendar[dayNum] = shiftNum
        worker.updateStats(shiftNum)

        worker.calculateNextShift(shiftNum)


    def makeRota(self):
        for dayNum in range(len(self.calendar)):
            q = []
            qCollision = []
            day = self.calendar[dayNum]

            for worker in self.staff:
                if worker.wishesCalendar[dayNum]:
                    worker.forceNextShift = worker.wishesCalendar[dayNum]
                forcedShift = worker.forceNextShift

                if forcedShift:
                    if day[forcedShift-1].checkIfManned() == False or forcedShift == dayOffShiftNumber:
                        self.addEntry(worker, dayNum, forcedShift)
                    else:
                        q.append(worker)

                else:
                    q.append(worker)


            #assign workers to shifts till their minium amount for given shift is enough
            for shift in day:
                while q and shift.checkIfManned() == False:
                    randomWorker = choice(q)
                    prevShift = randomWorker.calendar[dayNum-1]
                    if dayNum == 0:
                        if randomWorker.prevWeek:
                            prevShift = randomWorker.prevWeek[-1]
                        else:
                            prevShift = 0

                    currentShift = shift.number

                    if shiftRulesCheck(prevShift, currentShift):
                        q.remove(randomWorker)
                        self.addEntry(randomWorker, dayNum, shift.number)

                    else:
                        qCollision.append(randomWorker)
                        q.remove(randomWorker)

                q += qCollision
                qCollision = []

            #assign workers to shifts till their optimal amount for given shift is enough
            for shift in day:
                while q and shift.checkIfManned(optimal=True) == False:
                    randomWorker = choice(q)
                    prevShift = randomWorker.calendar[dayNum-1]
                    if dayNum == 0:
                        if randomWorker.prevWeek:
                            prevShift = randomWorker.prevWeek[-1]
                        else:
                            prevShift = 0

                    currentShift = shift.number

                    if shiftRulesCheck(prevShift, currentShift):
                        q.remove(randomWorker)
                        self.addEntry(randomWorker, dayNum, shift.number)

                    else:
                        qCollision.append(randomWorker)
                        q.remove(randomWorker)

                q += qCollision
                qCollision = []

            #if there are still workers available, give them a day-off
            while q:
                randomWorker = choice(q)
                q.remove(randomWorker)
                self.addEntry(randomWorker, dayNum, dayOffShiftNumber)

            #count collisions:
            for shift in day:
                if shift.checkIfManned(optimal=False) == False:
                    self.collisions += 10
                if shift.checkIfManned(optimal=True) == False:
                    self.collisions += 1

def generateRota(numOfSimulations):
    bag = []
    for num in range(numOfSimulations):
        for worker in staff:
            worker.mamboJambo()
        thisRota = Rota(name="December", emptyCalendar=calendarDefinition, staff=staff)
        thisRota.makeRota()
        bag.append(thisRota)

        
    bag.sort(key=lambda x:x.collisions, reverse=False)
    printRota(bag[0])



#rotaDecember = Rota(name="December", emptyCalendar=calendarDefinition, staff=staff)

generateRota(30)


