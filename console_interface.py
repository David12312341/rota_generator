


def printRota(rota):

    print("")

    dayNumberBar = "**| "
    for day in range(len(rota.emptyCalendar)):
        dayNumberBar += str(day) + " "
        if day < 10:
            dayNumberBar += " "
    dayNumberBar += "  DAY NUMBER"

    shiftTypeBar = "**|"
    shiftTypeBar += str([day for day in rota.emptyCalendar])
    shiftTypeBar += "   SHIFT GROUP NUMBER"

    underscore = "**|*********************************************************************************************"

    print(dayNumberBar)
    print(shiftTypeBar)
    print(underscore)

    for worker in rota.staff:
        row = worker.nameShort
        for dayNum in range(1):
            row += "|" + str(worker.calendar)

        stats = "   " + "worked=" + str(worker.workedDay) + ", rested=" + str(worker.restedDay)
        row += stats


        print(row)
    

    print(underscore)

    mannedMin = "**| "
    for day in rota.calendar:
        result = "   "
        for shift in day:
            if shift.checkIfManned(optimal=False) == False:
                result = "X  "

        mannedMin += result
    mannedMin += "  MANNED MIN - " + str(rota.collisions)
    print(mannedMin)


    mannedOptimal = "**| "
    for day in rota.calendar:
        result = "   "
        for shift in day:
            if shift.checkIfManned(optimal=True) == False:
                result = "X  "

        mannedOptimal += result
    mannedOptimal += "  MANNED OPTIMAL"
    print(mannedOptimal)



