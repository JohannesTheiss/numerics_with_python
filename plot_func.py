import numpy as np
import matplotlib.pyplot as plt
import enum

class LINE_TYPE(enum.Enum):
    no_type = 0
    line = 1
    dotted = 2
    dashed = 3
    line_dotted = 4

class PlotFunc:
    def __init__(self, x, y, line_type=LINE_TYPE.no_type, color="", name=""):
        self.x = x
        self.y = y
        self.line_type = line_type
        self.color = color
        self.name = name

    def __iter__(self):
        return iter((self.x, self.y, self.line_type, self.color, self.name))


# args:
# functions: [PlotFunc,...]
def plot_funcs(functions):
    i = 0
    for (x_values, y_values, line_type, color, name) in functions:
        lt = 'o-' # default: dotted with line
        if LINE_TYPE.line == line_type:
            lt = '-'
        elif LINE_TYPE.dotted == line_type:
            lt = ':'
        elif LINE_TYPE.dashed == line_type:
            lt = '--'
        elif LINE_TYPE.line_dotted == line_type:
            lt = 'o:'

        # if color == "red" than use "r"
#        if len(color) > 1: color = color[0]

#        fmt = f"{lt}{color}"
        fmt = f"{lt}"
        lbl = name if name != "" else f"line{i}"

        #plt.plot(x_values, y_values, marker='o', label=f"line{i}")
        if len(color) > 1:
            plt.plot(x_values, y_values, fmt, label=lbl, color=color)
        else:
            plt.plot(x_values, y_values, fmt, label=lbl)

        i += 1

    plt.legend()
    plt.grid()
    plt.show()


# example call
#plot_funcs([PlotFunc(np.array([1,2,3]), np.array([3,4,5]))])

