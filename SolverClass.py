class Solver:
    """Class operating on the class Field. It is a core of the value iteration algorithm."""

    def __init__(self, probForward=0.8, probLeft=0.1, probRight=0.1, price=3):

        self.__probForward = probForward
        """Probability of moving in the chosen direction."""
        self.__probLeft = probLeft
        """Probability of moving to the left of the chosen direction. (I.E.:The chosen direction is North,
        but with some probability we take a step to the West.)"""
        self.__probRight = probRight
        """Probability of moving right of the chosen direction."""
        self.__price = price
        """Price of one step. Positive values make the algorithm converge."""

        self.__cols = None
        """Number of columns."""
        self.__rows = None
        """Number of rows."""
        self.__field = None
        """Instance of Field class. This is the object on which runs the algorithm."""

    def setPrice(self, newPrice):
        self.__price = newPrice

    def getPrice(self):
        return self.__price

    def setProbs(self, probForward, probLeft, probRight):
        self.__probForward = probForward
        self.__probLeft = probLeft
        self.__probRight = probRight

    def exploreOne(self, direction, col, row):
        if (direction == 0) or (direction == 4):
            if self.__field.isWall(col=col, row=max(row - 1, 0)):
                return self.__field.getReward(col=col, row=row)
            return self.__field.getReward(col=col, row=max(row - 1, 0))

        if direction == 1:
            if self.__field.isWall(col=min(col + 1, self.__cols - 1), row=row):
                return self.__field.getReward(col=col, row=row)
            return self.__field.getReward(col=min(col + 1, self.__cols - 1), row=row)

        if direction == 2:
            if self.__field.isWall(col=col, row=min(row + 1, self.__rows - 1)):
                return self.__field.getReward(col=col, row=row)
            return self.__field.getReward(col=col, row=min(row + 1, self.__rows - 1))

        if (direction == 3) or (direction == -1):
            if self.__field.isWall(col=max(col - 1, 0), row=row):
                return self.__field.getReward(col=col, row=row)
            return self.__field.getReward(col=max(col - 1, 0), row=row)

    def exploreAllThree(self, direction, col, row):
        rewardLeft = self.exploreOne(direction - 1, col, row) * self.__probLeft
        rewardForward = self.exploreOne(direction, col, row) * self.__probForward
        rewardRight = self.exploreOne(direction + 1, col, row) * self.__probRight
        return rewardForward + rewardRight + rewardLeft - self.__price

    def solve(self, field):
        self.__field = field
        self.__rows, self.__cols = field.getRowsAndCols()

        while True:
            changed = False
            for row in range(self.__rows):
                for col in range(self.__cols):
                    if self.__field.isAbsorber(col=col, row=row):
                        continue
                    if self.__field.isWall(col=col, row=row):
                        continue

                    currentReward = self.__field.getReward(col=col, row=row)
                    currentBestDirection = self.__field.getBestDirection(col=col, row=row)
                    newRewards = [self.exploreAllThree(0, col, row), self.exploreAllThree(1, col, row),
                                  self.exploreAllThree(2, col, row), self.exploreAllThree(3, col, row)]

                    newReward = max(newRewards)
                    newBestDirection = newRewards.index(newReward)
                    if currentReward != newReward:
                        changed = True
                        self.__field.setReward(col, row, newReward)

                    if currentBestDirection != newBestDirection:
                        self.__field.setBestDirection(col, row, newBestDirection)
                        changed = True

            if not changed:
                break
