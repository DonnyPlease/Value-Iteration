import tkinter
from tkinter import ttk
from tkinter import simpledialog
from SolverClass import Solver
from FieldClass import Field


class UI:
    def __init__(self, FieldInit, SolverInit, width=300, height=200, rows=3, columns=4):

        self.__solved = False
        """ This parameter decides whether arrows are drawn."""

        # Initialize Tkinter window
        self.__root = tkinter.Tk()
        self.__root.title('')
        self.__root.geometry()
        self.__style = tkinter.ttk.Style(self.__root)
        self.__style.theme_use('clam')

        # Save values of dimensions of canvas grid
        self.__height, self.__width = height, width  # These are currently not needed
        self.__rows, self.__columns = rows, columns

        # Set parameters for size of one grid edge
        self.__rowSize = 80  # Parameter of row height (used when calculating size of canvas and when drawing the grid.)
        self.__colSize = 60

        # Save initialized instances of SolverClass and fieldClass
        self.__MySolver = SolverInit
        self.__MyField = FieldInit

        # Calculate height and width of canvas and create canvas
        self.__height, self.__width = self.__rows * self.__colSize + 1, self.__columns * self.__rowSize + 1
        self.__canvas = tkinter.Canvas(self.__root, width=self.__width, height=self.__height, background='white')

        # Buttons
        self.__ButtonSolve = tkinter.ttk.Button(self.__root, text="Solve", command=lambda: self.__solveAndDraw())
        self.__ButtonUpdate = tkinter.ttk.Button(self.__root, text="Update",
                                                 command=lambda: self.updateSolverAndField())

        # Entries for number of rows and columns
        self.__labelRows = tkinter.Label(text="Rows:")
        self.__labelColumns = tkinter.Label(text="Columns:")
        self.__newRows = tkinter.IntVar(value=self.__rows)
        self.__newColumns = tkinter.IntVar(value=self.__columns)
        self.__entryRows = tkinter.ttk.Entry(textvariable=self.__newRows, width=3)
        self.__entryColumns = tkinter.ttk.Entry(textvariable=self.__newColumns, width=3)

        # Entry for price of one step
        self.__labelPrice = tkinter.Label(text="Price:")
        self.__newPrice = tkinter.IntVar(value=self.__MySolver.getPrice())
        self.__entryPrice = tkinter.ttk.Entry(textvariable=self.__newPrice, width=4)

        # Entries for probabilities
        self.__labelLeft = tkinter.Label(text="Prob. left:")
        self.__newProbLeft = tkinter.StringVar(value='0.1')
        self.__entryLeft = tkinter.ttk.Entry(textvariable=self.__newProbLeft, width=4)
        self.__labelForward = tkinter.Label(text="Prob. forward:")
        self.__newProbForward = tkinter.StringVar(value='0.8')
        self.__entryForward = tkinter.ttk.Entry(textvariable=self.__newProbForward, width=4)
        self.__labelRight = tkinter.Label(text="Prob. left:")
        self.__newProbRight = tkinter.StringVar(value='0.1')
        self.__entryRight = tkinter.ttk.Entry(textvariable=self.__newProbRight, width=4)

        # Set up radio buttons
        self.__radioSelection = tkinter.IntVar()
        self.__radioSelection.set(1)
        self.__radioWall = tkinter.Radiobutton(self.__root, text="Toggle wall",
                                               variable=self.__radioSelection, value=1)
        self.__radioAbsorber = tkinter.Radiobutton(self.__root, text="Set absorber",
                                                   variable=self.__radioSelection, value=2)

        # Set up the grid
        self.__canvas.grid(column=0, row=0, columnspan=7, rowspan=2)
        self.__ButtonSolve.grid(column=7, row=0, sticky='n')  # Solve button
        self.__ButtonUpdate.grid(column=7, row=2, )  # Update button
        self.__labelRows.grid(column=0, row=2, sticky='e')  # Label 'Rows'
        self.__labelColumns.grid(column=0, row=3, sticky='e')  # Label 'Columns'
        self.__entryRows.grid(column=1, row=2, sticky='w')  # Entry 'Rows'
        self.__entryColumns.grid(column=1, row=3, sticky='w')  # Entry 'Columns'

        # Label and entry of price parameter
        self.__labelPrice.grid(column=0, row=4, sticky='e')  # Label 'Price'
        self.__entryPrice.grid(column=1, row=4, sticky='w')  # Entry 'Price'

        # Labels and entries for parameters of probability
        self.__labelLeft.grid(column=2, row=2, sticky='e')
        self.__labelForward.grid(column=2, row=3, sticky='e')
        self.__labelRight.grid(column=2, row=4, sticky='e')
        self.__entryLeft.grid(column=3, row=2, sticky='w')
        self.__entryForward.grid(column=3, row=3, sticky='w')
        self.__entryRight.grid(column=3, row=4, sticky='w')

        # Place radio buttons in to the grid
        self.__radioWall.grid(column=5, row=2)
        self.__radioAbsorber.grid(column=5, row=3)

        self.__canvas.bind("<Button-1>", self.__clickAction)

    def __clickAction(self, event):
        value = self.__radioSelection.get()
        if value == 1:
            self.__toggleWall(event)
            self.draw()
            return
        if value == 2:
            self.__toggleAbsorber(event)
            self.draw()
            return

    def __toggleAbsorber(self, event):
        col = event.x // self.__rowSize
        row = event.y // self.__colSize
        if not self.__MyField.isAbsorber(col=col, row=row):
            self.__MyField.unsetWall(col=col, row=row)
            answer = tkinter.simpledialog.askinteger("Set absorber", "Please, write the value of the reward:",
                                                     parent=self.__root,
                                                     minvalue=-999, maxvalue=999)
            self.__MyField.setAbsorber(col=col, row=row, reward=answer)
        else:
            self.__MyField.unsetAbsorber(col=col, row=row)

    def __toggleWall(self, event):
        col = event.x // self.__rowSize
        row = event.y // self.__colSize
        if not self.__MyField.isWall(col=col, row=row):
            self.__MyField.setWall(col=col, row=row)
        else:
            self.__MyField.unsetWall(col=col, row=row)

    # Calls solve function and redraws the canvas
    def __solveAndDraw(self):
        self.__MySolver.solve(self.__MyField)
        self.__solved = True
        self.draw()

    # Returns Tkinter for manipulation outside the class
    def getRoot(self):
        return self.__root

    def __drawGrid(self):
        sizeX = self.__columns * self.__rowSize
        sizeY = self.__rows * self.__colSize
        for i in range(self.__rows + 1):
            self.__canvas.create_line(0, i * self.__colSize + 2, sizeX + 2, i * self.__colSize + 2,
                                      fill='black', width=1)
        for j in range(self.__columns + 1):
            self.__canvas.create_line(j * self.__rowSize + 2, 0, j * self.__rowSize + 2, sizeY + 2,
                                      fill='black', width=1)

    def __drawInsides(self):
        for row in range(self.__rows):
            for col in range(self.__columns):
                # draw walls
                if self.__MyField.isWall(col, row):
                    color = 'black'
                    self.__canvas.create_rectangle(col * self.__rowSize + 2, row * self.__colSize + 2,
                                                   col * self.__rowSize + self.__rowSize + 2,
                                                   row * self.__colSize + self.__colSize + 2,
                                                   outline='black', fill=color, width=1)
                    continue

                if self.__MyField.isAbsorber(col, row):
                    color = 'green'
                    self.__canvas.create_rectangle(col * self.__rowSize + 2, row * self.__colSize + 2,
                                                   col * self.__rowSize + self.__rowSize + 2,
                                                   row * self.__colSize + self.__colSize + 2,
                                                   outline='black', fill=color, width=1)
                reward = self.__MyField.getReward(col, row)
                self.__canvas.create_text(col * self.__rowSize + 30, row * self.__colSize + 45,
                                          text=str(round(reward)),fill="black", font='Helvetica 20 bold')

                if self.__solved and not self.__MyField.isAbsorber(col, row):
                    direction = self.__MyField.getBestDirection(col, row)
                    self.__drawArrow(col, row, direction)

    def getArrayOfWallsAndAbsorbers(self):
        walls = []
        absorbers = []
        for col in range(self.__columns):
            for row in range(self.__rows):
                if self.__MyField.isWall(col=col, row=row):
                    walls.append([col, row])
                    continue
                if self.__MyField.isAbsorber(col=col, row=row):
                    reward = self.__MyField.getReward(col=col, row=row)
                    absorbers.append([col, row, reward])

        return walls, absorbers

    def setWallsAndAbsorbers(self, walls, absorbers):
        for wall in walls:
            col = wall[0]
            row = wall[1]
            if (col < self.__columns) and (row < self.__rows):
                self.__MyField.setWall(col=col, row=row)

        for absorber in absorbers:
            col = absorber[0]
            row = absorber[1]
            reward = absorber[2]
            if (col < self.__columns) and (row < self.__rows):
                self.__MyField.setAbsorber(col=col, row=row, reward=reward)

    def updateSolverAndField(self):
        walls, absorbers = self.getArrayOfWallsAndAbsorbers()
        self.__rows = self.__newRows.get()
        self.__columns = self.__newColumns.get()
        self.__height, self.__width = self.__rows * self.__colSize + 1, self.__columns * self.__rowSize + 1
        self.__canvas.config(width=self.__width, height=self.__height)
        del self.__MyField
        del self.__MySolver
        self.__MyField = Field(rows=self.__rows, columns=self.__columns)
        self.__MySolver = Solver(probForward=float(self.__newProbForward.get()),
                                 probRight=float(self.__newProbRight.get()),
                                 probLeft=float(self.__newProbLeft.get()),
                                 price=self.__newPrice.get())
        self.setWallsAndAbsorbers(walls, absorbers)
        self.__solved = False
        self.draw()
        return

    def draw(self):
        self.__canvas.delete('all')
        self.__drawGrid()
        self.__drawInsides()
        # self.__canvas.pack()
        self.__root.update()
        self.__root.mainloop()

    def __drawArrow(self, col, row, direction):
        """
        This function draws arrow inside of cell with the direction based on the parameters.

        :param col: index of column
        :param row: index of row
        :param direction: (0 = north, 1 = east, 2 = south, 3 = west)
        """
        if direction == 0:
            self.__canvas.create_line(col * self.__rowSize + 65, row * self.__colSize + 50,
                                      col * self.__rowSize + 65, row * self.__colSize + 10,
                                      arrow=tkinter.LAST)

        if direction == 1:
            self.__canvas.create_line(col * self.__rowSize + 20, row * self.__colSize + 15,
                                      col * self.__rowSize + 60, row * self.__colSize + 15,
                                      arrow=tkinter.LAST)

        if direction == 2:
            self.__canvas.create_line(col * self.__rowSize + 65, row * self.__colSize + 10,
                                      col * self.__rowSize + 65, row * self.__colSize + 50,
                                      arrow=tkinter.LAST)

        if direction == 3:
            self.__canvas.create_line(col * self.__rowSize + 60, row * self.__colSize + 15,
                                      col * self.__rowSize + 20, row * self.__colSize + 15,
                                      arrow=tkinter.LAST)
