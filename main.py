from UI import UI
from FieldClass import Field
from SolverClass import Solver


if __name__ == '__main__':
    # Initialize MyField
    MyField = Field(rows=4, columns=5)
    MyField.setWall(1, 1)
    MyField.setAbsorber(row=0, col=3, reward=100)
    MyField.setAbsorber(row=1, col=3, reward=-100)

    # Initialize MySolver
    MySolver = Solver(probForward=0.8, probRight=0.1, probLeft=0.1, price=3)

    # Initialize MyUI
    MyUI = UI(rows=4, columns=5, FieldInit=MyField, SolverInit=MySolver)

    # Begin Program
    MyUI.draw()


