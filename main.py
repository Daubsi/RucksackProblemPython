class Paket:
    #  The parameters
    name = 0
    value = 0
    width = 0
    length = 0
    valuePerArea = 0

    #  The creation
    def __init__(self, name, value, width, length):
        self.value = value
        self.width = width
        self.length = length
        self.name = name
        self.area = length * width
        self.valuePerArea = value / self.area

    def toString(self):
        return "Name: \t" + str(self.name) + "\n" + "Value: \t" + str(self.value) + "\n" + "Width: " + str(
            self.width) + "\n" + "Length: \t" + str(self.length) + "\n"


# --------------------------------------------------------------------------------------


from random import randint
import numpy as np
import matplotlib.pyplot as plt
import operator

# testMode saves on some printStatements
testMode = True

placingPosition = [1, 1]

rotation = True

# General Information for later
nPlacedPackages = 0
nSkippedPackages = 0
valueOfAllPackages = 0
areaOfAllPackages = 0
valueOfPlacedPackages = 0
areaOfPlacedPackages = 0


def prepareSpace(space):
    for i in range(len(Space)):
        for j in range(len(Space[i])):
            if i == 0 or i == len(Space) - 1 or j == 0 or j == len(Space[i]) - 1:
                Space[i][j] = -1


# Creates random sample packages
def prepareSamples(nPackages, min, max):
    PackageList = []
    for i in range(nPackages):
        name = i + 2
        value = randint(1, 10)
        width = randint(min, max)
        length = randint(min, max)
        PackageList.append(Paket(name, value, width, length))
    return PackageList


# Prints the space array in the console
def printSpace(space):
    print(np.matrix(space))


# Checks the amount of free cells around a package
def freeCellsAroundPackage(space, currentPaketLength, currentPaketWidth, startPoint):
    nAllAvailableCells = 0
    for i in range(startPoint[0] - 1, startPoint[0] + currentPaketLength + 1):
        for j in range(startPoint[1] - 1, startPoint[1] + currentPaketWidth + 1):
            if i < len(space) - 1 and j < len(space[i]) - 1:
                if i == startPoint[0] - 1 or i == startPoint[0] + currentPaketLength or \
                        j == startPoint[1] - 1 or j == startPoint[1] + currentPaketWidth:
                    if space[i][j] == 0:
                        nAllAvailableCells += 1

    return nAllAvailableCells


# Checking if the package would fit in both orientations
def doesFit(space, currentPaket, startPoint):
    orientationA = True
    orientationB = True

    for i in range(startPoint[0], startPoint[0] + currentPaket.length):
        for j in range(startPoint[1], startPoint[1] + currentPaket.width):
            if i <= widthOfSpace and j <= lengthOfSpace:
                if space[i][j] != 0:
                    orientationA = False
            else:
                orientationA = False

    for i in range(startPoint[0], startPoint[0] + currentPaket.width):
        for j in range(startPoint[1], startPoint[1] + currentPaket.length):
            if i <= widthOfSpace and j <= lengthOfSpace:
                if space[i][j] != 0:
                    orientationB = False
            else:
                orientationB = False

    # Returning the orientations that would fit
    return [orientationA, orientationB]


# Prints a package in the Space Array
def printPackage(space, currentPaket, startPoint, rotate):
    if rotate:
        for i in range(startPoint[0], startPoint[0] + currentPaket.width):
            for j in range(startPoint[1], startPoint[1] + currentPaket.length):
                space[i][j] = currentPaket.name

    else:

        for i in range(startPoint[0], startPoint[0] + currentPaket.length):
            for j in range(startPoint[1], startPoint[1] + currentPaket.width):
                space[i][j] = currentPaket.name


def printPackageInfo(currentPaket):
    print(currentPaket.toString())


# Counts the amount of empty cells
def emptyCells(space):
    emptyCells = 0
    for i in range(1, len(space)):
        for j in range(1, len(space[i])):
            if space[i][j] == 0:
                emptyCells += 1

    return emptyCells


def endInfo():
    print("\n")
    printSpace(Space)

    print("Final results:")
    print("Amount of placed packages: " + str(nPlacedPackages))
    print("Amount of skipped packages: " + str(nSkippedPackages))
    print("Value of all packages: " + str(valueOfAllPackages))
    print("Size of all packages: " + str(areaOfAllPackages))
    print("Size of given Space: " + str((lengthOfSpace + 2) * (widthOfSpace + 2)))
    print("Value of all placed packages: " + str(valueOfPlacedPackages))
    print("Size of all placed packages: " + str(areaOfPlacedPackages))
    print("Weight/size ratio of all packages: " + str(valueOfAllPackages / areaOfAllPackages))
    print("Weight/size ratio of all placed packages: " + str(valueOfPlacedPackages / areaOfPlacedPackages))
    print("Number of cells " + str(lengthOfSpace * widthOfSpace))
    print("Number of empty cells: " + str(emptyCells(Space)))
    print("Percentage of free cells: " + str(emptyCells(Space) / (lengthOfSpace * widthOfSpace) * 100) + " %")


# -------------------------------------------------------------

lengthOfSpace = 20
widthOfSpace = 20
Space = np.zeros((widthOfSpace + 2, lengthOfSpace + 2))

package_List = prepareSamples(1000, 3, 7)
# package_List = [Paket(1, 2, 6, 3), Paket(2, 1, 4, 1), Paket(3, 4, 2, 2), Paket(4, 2, 3, 2), Paket(5, 8, 3, 2),
#                Paket(6, 9, 2, 3), Paket(7, 90, 2, 2), Paket(8, 56, 4, 1), Paket(9, 2, 2, 1), Paket(10, 56, 2, 1)]

packageList = sorted(package_List, key=operator.attrgetter("valuePerArea"), reverse=True)
prepareSpace(Space)

for e in range(len(packageList)):
    valueOfAllPackages += packageList[e].value
    areaOfAllPackages += packageList[e].area

    mostFreeCells = 1000
    bestPlacingPosition = [-1, 0]
    rotation = False

    for i in range(len(Space)):
        for j in range(len(Space[i])):

            currentPosition = [i, j]
            # If the given point is empty
            if Space[i][j] == 0:
                # Checking the better Rotation
                if doesFit(Space, packageList[e], currentPosition)[0]:
                    if freeCellsAroundPackage(Space, packageList[e].length, packageList[e].width,
                                              currentPosition) < mostFreeCells:
                        bestPlacingPosition = currentPosition
                        rotation = False
                        mostFreeCells = freeCellsAroundPackage(Space, packageList[e].length, packageList[e].width,
                                                               currentPosition)

                elif doesFit(Space, packageList[e], currentPosition)[1]:
                    if freeCellsAroundPackage(Space, packageList[e].width, packageList[e].length,
                                              currentPosition) < mostFreeCells:
                        bestPlacingPosition = currentPosition
                        rotation = True
                        mostFreeCells = freeCellsAroundPackage(Space, packageList[e].length, packageList[e].width,
                                                               currentPosition)

    if bestPlacingPosition[0] != -1:
        printPackage(Space, packageList[e], bestPlacingPosition, rotation)

        nPlacedPackages += 1
        valueOfPlacedPackages += packageList[e].value
        areaOfPlacedPackages += packageList[e].area

    else:
        nSkippedPackages += 1
        if not testMode:
            print("Not able to place this package:")

    if not testMode:
        printPackageInfo(packageList[e])
        printSpace(Space)

    if e % 10 == 0:
        print(str(e) + " packages done")

endInfo()

fig = plt.figure(figsize=(6, 3.2))

ax = fig.add_subplot(111)
ax.set_title('colorMap')
plt.imshow(Space)
ax.set_aspect('equal')

cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
cax.get_xaxis().set_visible(False)
cax.get_yaxis().set_visible(False)
cax.patch.set_alpha(0)
cax.set_frame_on(False)
plt.colorbar(orientation='vertical')
plt.show()
