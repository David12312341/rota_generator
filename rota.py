from random import randint, choice
from collections import deque

from workers import *



class Shift:
    def __init__(self, name, minNumOfWorkers=1, maxNumOfWorkers=10, optimalNumOfWorkers=3, manned=False, number=0):
        self.name = name
        self.minNumOfWorkers = minNumOfWorkers
        self.maxNumOfWorkers = maxNumOfWorkers
        self.optimalNumOfWorkers = optimalNumOfWorkers
        self.manned = manned
        self.queue = deque()
        self.workers = []
        self.number = number

    def __str__(self):
        return self.name + ": " + str([worker.name for worker in self.workers])

    def checkIfManned(self, optimal=False):
        if optimal:
            return len([worker for worker in self.workers if worker.independent==True]) >= self.optimalNumOfWorkers
        else:
            return len([worker for worker in self.workers if worker.independent==True]) >= self.minNumOfWorkers

    def checkIfNotCollide(self, prevShift, nextShift):
        return prevShift <= nextShift or prevShift == 4





class Rota:
    def __init__(self, name, emptyCalendar, staff):
        self.name = name
        self.calendar = []
        self.emptyCalendar = emptyCalendar
        self.staff = staff
        self.collisions = 0
        self.collisionsOptimal = 0

        for dayNum in range(len(emptyCalendar)):
            day = emptyCalendar[dayNum]
            if day == 0:
                morningShift = Shift(name="MorningS", minNumOfWorkers=2, maxNumOfWorkers=10, optimalNumOfWorkers=3, manned=False, number=1)
                afternoonShift = Shift(name="AfternoonS", minNumOfWorkers=2, maxNumOfWorkers=10, optimalNumOfWorkers=3, manned=False, number=2)
                nightShift = Shift(name="NightS", minNumOfWorkers=2, maxNumOfWorkers=10, optimalNumOfWorkers=2, manned=False, number=3)
                dayOff = Shift(name="DayOff", minNumOfWorkers=0, maxNumOfWorkers=10, optimalNumOfWorkers=0, manned=True, number=4)
            else:
                morningShift = Shift(name="MorningS", minNumOfWorkers=1, maxNumOfWorkers=10, optimalNumOfWorkers=1, manned=False, number=1)
                afternoonShift = Shift(name="AfternoonS", minNumOfWorkers=1, maxNumOfWorkers=10, optimalNumOfWorkers=1, manned=False, number=2)
                nightShift = Shift(name="NightS", minNumOfWorkers=1, maxNumOfWorkers=10, optimalNumOfWorkers=1, manned=False, number=3)
                dayOff = Shift(name="DayOff", minNumOfWorkers=0, maxNumOfWorkers=10, optimalNumOfWorkers=0, manned=True, number=4)

            self.calendar.append([morningShift, afternoonShift, nightShift, dayOff])

    def reset(self):
        for worker in self.staff:
            worker.clearCalendar()

        self.calendar = []


    def show(self, dayFrom, dayTo):
        for i in range(dayFrom, dayTo):
            print("\n*** DAY " + str(i) + " ***")
            day = self.calendar[i]
            if day:
                for shift in day:
                    print(shift)

    def show2(self):
        daynumber = "**| "
        for day in range(len(self.emptyCalendar)):
            daynumber += str(day) + " "
            if day < 10:
                daynumber += " "

        weekends = "**|"
        weekends += str([day for day in self.emptyCalendar])
        underscore = "**|*********************************************************************************************"
        print(daynumber)
        print(weekends)
        print(underscore)
        for worker in self.staff:
            row = worker.nameShort

            for dayNum in range(1):
                row += "|" + str(worker.calendar)

            print(row)

        print(underscore)

        mannedMin = "**| "
        for day in self.calendar:
            result = "   "
            for shift in day:
                if shift.checkIfManned(optimal=False) == False:
                    result = "X  "

            mannedMin += result
        print(mannedMin)


        mannedOptimal = "**| "
        for day in self.calendar:
            result = "   "
            for shift in day:
                if shift.checkIfManned(optimal=True) == False:
                    result = "X  "

            mannedOptimal += result
        print(mannedOptimal)



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
                    if day[forcedShift-1].checkIfManned() == False or forcedShift == 4:
                        self.addEntry(worker, dayNum, forcedShift)
                    else:
                        q.append(worker)

                else:
                    q.append(worker)

            #print("waiting for assignment: ", [worker.name for worker in q])

            for shift in day:
                while q and shift.checkIfManned() == False:
                    randomWorker = choice(q)
                    prevShift = randomWorker.calendar[dayNum-1]
                    if dayNum == 0:
                        prevShift = randomWorker.prevWeek[-1]
                    currentShift = shift.number

                    if shift.checkIfNotCollide(prevShift, currentShift):
                        q.remove(randomWorker)
                        self.addEntry(randomWorker, dayNum, shift.number)

                    else:
                        qCollision.append(randomWorker)
                        q.remove(randomWorker)

                q += qCollision
                qCollision = []

            for shift in day:
                while q and shift.checkIfManned(optimal=True) == False:
                    randomWorker = choice(q)
                    prevShift = randomWorker.calendar[dayNum-1]
                    if dayNum == 0:
                        prevShift = randomWorker.prevWeek[-1]
                    currentShift = shift.number

                    if shift.checkIfNotCollide(prevShift, currentShift):
                        q.remove(randomWorker)
                        self.addEntry(randomWorker, dayNum, shift.number)

                    else:
                        qCollision.append(randomWorker)
                        q.remove(randomWorker)

                q += qCollision
                qCollision = []

            while q:
                randomWorker = choice(q)
                q.remove(randomWorker)
                self.addEntry(randomWorker, dayNum, 4)

            #count collisions:
            for shift in day:
                if shift.checkIfManned(optimal=False) == False:
                    self.collisions += 1
                if shift.checkIfManned(optimal=True) == False:
                    self.collisionsOptimal += 1



def generateRota(numOfSimulations):
    bag = []
    for num in range(numOfSimulations):
        bag.append(Rota(name="December", emptyCalendar=calendarDecember, staff=staff))
        for worker in staff:
            worker.clearCalendar()
            worker.clearStats()
        
    bag.sort(key=lambda x:x.collisions, reverse=True)
    for rota in bag:
        rota.makeRota()
        rota.show2()
        for worker in staff:
            worker.clearCalendar()
            worker.clearStats()




rotaDecember = Rota(name="December", emptyCalendar=calendarDecember, staff=staff)

generateRota(4)



