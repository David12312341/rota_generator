# DEFINE CALENDAR
# number of days in given month equals number of elements in the list
# for each day specify corresponding group of shifts using integer number
# e.g. for weekends the group may be different than for normal working days (shifts may require less workers to attend)
calendarDefinition = [
        0,0,1,1,
        0,0,0,0,0,1,1,
        0,0,0,0,0,1,1,
        0,0,0,0,0,1,1,
        0,0,0,0,0,1
        ]


# DEFINE SHIFTS
# each group of shifts (list-object element within the following major list identified by integer number starting from 0) corresponds
# to number in the month calendar defined above
#
# template: 
# ["Name of the shift", minimum number of workers, maximum number of workers, optimal number of workers, is Manned? True/False, id number]
shiftDefinition = [
        [
            ["Morning Standard Shift", 2, 10, 3, False],
            ["Afternoon Standard Shift", 2, 10, 3, False],
            ["Night Standard Shift", 2, 10, 2, False]
        ],
        [
            ["Morning Weekend Shift", 1, 10, 1, False],
            ["Afternoon Weekend Shift", 1, 10, 1, False],
            ["Night Weekend Shift", 1, 10, 1, False]
        ]
]

# DEFINE SHIFT-RELATIONS CONDITION
# choose: True/False if the worker must have at least 24h break between shifts:
oneDayBreakRule = True

minRestingDaysInRow = 2

for shiftGroup in shiftDefinition:
    shiftGroup.append(["Day Off", 0, 10, 0, True])

def shiftRulesCheck(prevShift, nextShift):
    if oneDayBreakRule:
        return prevShift <= nextShift or prevShift == dayOffShiftNumber
    else:
        return True

dayOffShiftNumber = len(shiftDefinition[0])

class Worker:
    def __init__(self, name, calendar=calendarDefinition, workingDays=21, maxWorkingDaysInRow=5, shiftContinuity=5, independent=True, prevWeek=False):
        self.name = name
        self.independent = independent #if able to take care of all shift responsibilities by himself
        self.nameShort = self.name[0] + self.name[-1]
        self.workingDays = workingDays
        self.workedDay = 0
        self.restedDay = 0
        self.maxWorkingDaysInRow = maxWorkingDaysInRow
        self.shiftContinuity = shiftContinuity #how many days in row must he work on the same shift, excluding day-off shift
        self.workingDayInRow = 0
        self.restingDayInRow = 0
        self.forceNextShift = 0
        self.wishesCalendar = [0 for day in calendar]
        self.calendar = [0 for day in calendar]
        self.prevWeek = prevWeek


        #if you specify shifts that the worker attended last week of the previous month, it will calculate how many days the worker has been working/resting, for now it works with the following format --> [X, X, X, X, X, X, X], where X is an integer number identyfying type of shift
        if prevWeek:
            self.calculatePrevWeek()


    def clearStats(self):
        self.workedDay = self.restedDay = 0

    def clearCalendar(self):
        self.calendar = [0 for day in calendarDefinition]

    def updateStats(self, shiftNum):
        if shiftNum > 0 and shiftNum < dayOffShiftNumber:
            self.workingDayInRow += 1
            self.workedDay += 1
            self.restingDayInRow = 0
        elif shiftNum == dayOffShiftNumber:
            self.restingDayInRow += 1
            self.restedDay += 1
            self.workingDayInRow = 0
        else:
            self.restingDayInRow = 0
            self.workingDayInRow = 0


    def calculateNextShift(self, prevShiftNum):
        if self.restingDayInRow == (minRestingDaysInRow - 1) or self.workedDay >= self.workingDays:
            self.forceNextShift = dayOffShiftNumber

        elif self.restingDayInRow >= minRestingDaysInRow:
            self.forceNextShift = 0

        elif self.workingDayInRow > 0 and self.workingDayInRow < self.shiftContinuity:
            self.forceNextShift = prevShiftNum

        elif self.workingDayInRow >= self.maxWorkingDaysInRow:
            self.forceNextShift = dayOffShiftNumber

        else:
            self.forceNextShift = 0
        


    def calculatePrevWeek(self):
        
        for shiftNum in self.prevWeek:
            self.updateStats(shiftNum)

        self.calculateNextShift(self.prevWeek[-1])
        
        self.clearStats()


    def makeWish(self, fromDay, toDay, shiftNumber):
        for dayNumber in range(fromDay, toDay):
            self.wishesCalendar[dayNumber] = shiftNumber


    def mamboJambo(self):
        self.clearStats()
        self.clearCalendar()
        self.calculatePrevWeek()




    def __str__(self):
        return self.name

staff = [
Worker("Krzysztof K", workingDays=20, prevWeek=[4,4,4,3,3,3,3]),
Worker("Roman P", prevWeek=[4,4,4,4,1,1,4]),
Worker("Robert N", prevWeek=[1,1,1,4,2,2,2]),
Worker("Roberto B", prevWeek=[4,4,2,2,2,2,2]),
Worker("David M", prevWeek=[3,3,4,1,1,1,1]),
Worker("Quentin T", prevWeek=[2,2,4,4,4,4,4]),
Worker("Sergio L", prevWeek=[2,2,4,4,3,3,3]),
Worker("Vincent G", prevWeek=[1,1,4,4,4,4,4]),
Worker("David L", prevWeek=[3,3,3,4,4,4,4]),
Worker("Alan P", prevWeek=[1,1,4,4,1,1,1]),
Worker("Steven S", independent=False, prevWeek=[2,2,4,4,1,1,1])
]

"""
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
"""

staff[0].makeWish(25,30,dayOffShiftNumber)
staff[1].makeWish(6,23,dayOffShiftNumber)
staff[4].makeWish(0,6,dayOffShiftNumber)
staff[8].makeWish(24,30,dayOffShiftNumber)
