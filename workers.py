
calendarDecember = [
        0,0,1,1,
        0,0,0,0,0,1,1,
        0,0,0,0,0,1,1,
        0,0,0,0,0,1,1,
        0,0,0,0,0,1
        ]




class Worker:
    def __init__(self, name, calendar=calendarDecember, workingDays=21, maxWorkingDaysInRow=5, shiftContinuity=5, independent=True):
        self.name = name
        self.independent = independent
        self.nameShort = self.name[0] + self.name[-1]
        self.workingDays = workingDays
        self.workedDay = 0
        self.restedDay = 0
        self.maxWorkingDaysInRow = maxWorkingDaysInRow
        self.shiftContinuity = shiftContinuity
        self.workingDayInRow = 0
        self.restingDayInRow = 0
        self.forceNextShift = 0
        self.wishesCalendar = [0 for day in calendar]
        self.calendar = [0 for day in calendar]
        self.prevWeek = []
        

        self.nextPrefferedShift = 0;

    def showStats(self):
        print(self.name)
        print("Working days: ", self.workingDays)
        print("Worked days: ", self.workedDay)
        print("Rested days: ", self.restedDay)
        print("Working day in row: ", self.workingDayInRow)
        print("Resting day in row: ", self.restingDayInRow)

    def clearStats(self):
        self.workedDay = self.restedDay = 0

    def clearCalendar(self):
        self.calendar = [0 for day in calendarDecember]

    def updateStats(self, shiftNum):
        if shiftNum > 0 and shiftNum < 4:
            self.workingDayInRow += 1
            self.workedDay += 1
            self.restingDayInRow = 0
        elif shiftNum == 4:
            self.restingDayInRow += 1
            self.restedDay += 1
            self.workingDayInRow = 0
        else:
            self.restingDayInRow = 0
            self.workingDayInRow = 0


    def calculateNextShift(self, prevShiftNum):
        if self.restingDayInRow == 1 or self.workedDay >= self.workingDays:
            self.forceNextShift = 4

        elif self.restingDayInRow > 1:
            self.forceNextShift = 0

        elif self.workingDayInRow > 0 and self.workingDayInRow < self.shiftContinuity:
            self.forceNextShift = prevShiftNum

        elif self.workingDayInRow >= self.maxWorkingDaysInRow:
            self.forceNextShift = 4

        else:
            self.forceNextShift = 0
        


    def calculatePrevWeek(self, prevWeek):
        self.prevWeek = prevWeek

        for shiftNum in self.prevWeek:
            self.updateStats(shiftNum)

        self.calculateNextShift(self.prevWeek[-1])
        
        self.clearStats()


    def makeWish(self, fromDay, toDay, shiftNumber):
        for dayNumber in range(fromDay, toDay):
            self.wishesCalendar[dayNumber] = shiftNumber



    def __str__(self):
        return self.name


staff = [
Worker("Krzysztof K", workingDays=20),
Worker("Roman P"),
Worker("Robert N"),
Worker("Roberto B"),
Worker("David M"),
Worker("Quentin T"),
Worker("Sergio L"),
Worker("Vincent G"),
Worker("David L"),
Worker("Alan P"),
Worker("Steven S", independent=False)
]



#starter pack
staff[0].calculatePrevWeek([4,4,4,3,3,3,3])
staff[1].calculatePrevWeek([4,4,4,4,1,1,4])
staff[2].calculatePrevWeek([1,1,1,4,2,2,2])
staff[3].calculatePrevWeek([4,4,2,2,2,2,2])
staff[4].calculatePrevWeek([3,3,4,1,1,1,1])
staff[5].calculatePrevWeek([2,2,4,4,4,4,4])
staff[6].calculatePrevWeek([2,2,4,4,3,3,3])
staff[7].calculatePrevWeek([1,1,4,4,4,4,4])
staff[8].calculatePrevWeek([3,3,3,4,4,4,4])
staff[9].calculatePrevWeek([1,1,4,4,1,1,1])
staff[10].calculatePrevWeek([2,2,4,4,1,1,1])

staff[0].makeWish(25,30,4)
staff[1].makeWish(6,23,4)
staff[4].makeWish(0,6,4)
staff[8].makeWish(24,30,4)
