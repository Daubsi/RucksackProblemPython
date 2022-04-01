from main import Paket
from random import randint



# Modeling space with an array
# Size of space
lengthOfSpace = 30
widthOfSpace  = 30
Space = [widthOfSpace+2][lengthOfSpace+2]

# List of the given packages
packageList = Paket[100]

# testMode saves on some printStatements
testMode = False

placingPosition = [1, 1]

rotation = True

# General Information for later
global nPlacedPackages
global nSkippedPackages
global valueOfAllPackages
global areaOfAllPackages
global valueOfPlacedPackages
global areaOfPlacedPackages

# Creates random sample packages
def prepareSamples(packageList, min, max):
    for i in packageList.length:
        name = i + 1
        value  = randint(1,100)
        width  = randint(min, max)
        length = randint(min, max)
        packageList[i] = Paket(name, value, width, length)



# Fills the Array with 0's except the borders they get filled with 1's
def preapareSpace(space):
    for i in range(len(space)) :
        for j in range(len(space[i])) :
            # If at a border fill 1 else fill 0
            if ((i == space.length-1 or i == 0) or (j == space[i].length-1 or j == 0)):
                space[i][j] = 1

            else :
                space[i][j] = 0


# Prints the space array in the console
def printSpace(space, max):
    Spaces = 4
    if (max > 9):
        Spaces = 3
    if (max > 99):
        Spaces = 2
    if (max > 999):
        Spaces = 1

    for i in range(1, len(space)-1):
        for j in range(len(space[i])):
            spaceNeeded = Spaces
            printMessage = ""
            if (space[i][j] < 1000):
                spaceNeeded = Spaces - 2
            if (space[i][j] < 100 ):
                spaceNeeded = Spaces - 1
            if (space[i][j] < 10  ):
                spaceNeeded = Spaces - 0

            for nSpaces in range(spaceNeeded):
                printMessage += " "

            print(space[i][j] + printMessage + " ")

        print("\n")

    print("\n")


# Checks the amount of 1's surrounding a Cell
def checkSourroundings(space, xValue, yValue):
    nFreeCells = 0
    if (space[yValue+1][xValue] == 0): nFreeCells+=1
    if (space[yValue-1][xValue] == 0): nFreeCells+=1
    if (space[yValue][xValue+1] == 0): nFreeCells+=1
    if (space[yValue][xValue-1] == 0): nFreeCells+=1

    return nFreeCells


# Sorts the Packages according to the attribute ValuePerArea
def sortPackages(packages):
    for a in range(len(packages)):
        tallest = a
        b = a+1
        for i in range(b, len(packages)):
            if(packages[b].getValuePerArea() > packages[tallest].getValuePerArea()):
                tallest = b
        temp = packages[a]
        packages[a] = packages[tallest]
        packages[tallest] = temp


# Checks the amount of free cells around a package

def freeCellsAroundPackage(space, currentPaketLength, currentPaketWidth, startPoint):
    space.fillSpace(space, currentPaketLength, currentPaketWidth, startPoint, True)
    nAllAvailableCells = 0
    i = startPoint[0]
    j = startPoint[1]
    for i in range(i, i+currentPaketLength) and i < len(space)-1:
        for j in range(j, j+currentPaketWidth) and j < len(space[i])-1:
            nAllAvailableCells += space.checkSourroundings(space, j, i)


    space.fillSpace(space, currentPaketLength, currentPaketWidth, startPoint, False)
    return nAllAvailableCells


# Fills the area of a package with 0 or 1 in the array
def fillSpace(space, length, width, startPoint, fill):
    i = startPoint[0]
    j = startPoint[1]
    for i in range(i, i + length) and i < len(space) - 1:
        for j in range(j, j + width) and j < len(space[i]) - 1:

            if (fill):
                space[i][j] = 1
            else:
                space[i][j] = 0


# Checking if the package would fit in both orientations
def doesFit(space, Paket, currentPaket, startPoint):

    orientationA = True
    orientationB = True

    i = startPoint[0]
    j = startPoint[1]
    for i in range(i, i + currentPaket.length):
        for j in range(j, j + currentPaket.width):
            if i <= len(space) and j <= len(space[i]):
                if space[i][j] != 0:
                    orientationA = False
            else: orientationA = False


    for i in range(i, i + currentPaket.width):
        for j in range(j, j + currentPaket.length):
            if i <= len(space) and j <= len(space[i]):
                if space[i][j] != 0:
                    orientationB = False
            else: orientationB = False


    # Returning the orientations that would fit
    return [orientationA, orientationB]


# Prints a package in the space Array
def printPackage(space, currentPaket, startPoint, rotate):
    if (rotate):

        i = startPoint[0]
        j = startPoint[1]

        for i in range(i, i+currentPaket.width):
            for j in range(j, j+currentPaket.length):
                space[i][j] = currentPaket.name

    else :
        i = startPoint[0]
        j = startPoint[1]

        for i in range(i, i + currentPaket.length):
            for j in range(j, j + currentPaket.width):
                space[i][j] = currentPaket.name





def printPackageInfo(currentPaket):
    print(currentPaket.toString())


# Counts the amount of empty cells
def emptyCells(space):
    emptyCells = 0
    for i in range(1, len(space)):
        for j in range(1, len(space[i])):
            if (space[i][j] == 0):
                emptyCells += 1

    return emptyCells


def endInfo(self):

    printSpace(Space, packageList.length)

    print("Final results:")
    print("Amount of placed packages: " + nPlacedPackages)
    print("Amount of skipped packages: " + nSkippedPackages)
    print("Value of all packages: " + valueOfAllPackages)
    print("Size of all packages: " + areaOfAllPackages)
    print("Value of all placed packages: " + valueOfPlacedPackages)
    print("Size of all placed packages: " + areaOfPlacedPackages)
    print("Weight/size ratio of all packages: " + valueOfAllPackages / areaOfAllPackages)
    print("Weight/size ratio of all placed packages: " + valueOfPlacedPackages / areaOfPlacedPackages)
    print("Number of cells " + lengthOfSpace * widthOfSpace)
    print("Number of empty cells: " + emptyCells(Space))
    print("Percentage of free cells: " + emptyCells(Space) / (lengthOfSpace * widthOfSpace) * 100 + " %")


def main():

    prepareSamples(packageList, 100, 100)
    preapareSpace(Space)
    sortPackages(packageList)

    for e in range(len(packageList)):
        valueOfAllPackages += packageList[e].value
        areaOfAllPackages += packageList[e].getArea()

        mostFreeCells = 1000
        bestPlacingPosition = [-1, 0]
        rotation = False

        for i in range(len(Space)) :
            for j in range(len(Space[i])):

                currentPosition = [i, j]
                # If the given point is empty
                if (Space[i][j] == 0):
                    # Checking the better Rotation
                    if doesFit(Space, packageList[e], currentPosition)[0] and freeCellsAroundPackage(Space, packageList[e].length, packageList[e].width, currentPosition) < mostFreeCells:

                        bestPlacingPosition = currentPosition
                        rotation = False
                        mostFreeCells = freeCellsAroundPackage(Space, packageList[e].length, packageList[e].width, currentPosition)

                    elif (doesFit(Space, packageList[e], currentPosition)[1]) and freeCellsAroundPackage(Space, packageList[e].width, packageList[e].length, currentPosition) < mostFreeCells:


                        bestPlacingPosition = currentPosition
                        rotation = True
                        mostFreeCells = freeCellsAroundPackage(Space, packageList[e].length, packageList[e].width, currentPosition)






        if (bestPlacingPosition[0] != -1):
            printPackage(Space, packageList[e], bestPlacingPosition, rotation)

            nPlacedPackages += 1
            valueOfPlacedPackages += packageList[e].value
            areaOfPlacedPackages += packageList[e].getArea()

        else :
            nSkippedPackages += 1
            if not testMode:
                print("Not able to place this package:")



        if not testMode:
            printPackageInfo(packageList[e])
            printSpace(Space, packageList.length)

    endInfo()
