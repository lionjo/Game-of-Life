import tkinter as Tk

import numpy as np
import PIL.Image
import PIL.ImageTk

from GameOfLife.Rule import Rule


class RuleWindow(Tk.Frame):
    """
    Display an image on Tkinter.Canvas and delete it on button click
    """

    def __init__(self, parent, rule: Rule):
        """
        Inititialize the GUI with a button and a Canvas objects
        """
        self.window = Tk.Toplevel(parent)
        self.parent = parent
        self.rule = rule
        self.mult = 20
        self.ruleheight, self.rulewidth = np.shape(rule.rule_array)
        self.width = self.rulewidth * self.mult
        self.height = self.ruleheight * self.mult

        self.init_rule()

    def init_rule(self):
        """
        Draw the GUI
        """
        self.window.title("Set the rule")
        labels = []
        for i in range(0, self.rulewidth):
            labels.append(Tk.Label(self.window, text=str(i)))
            labels[-1].grid(row=0, column=i + 1, sticky="nesw")

        self.window.canvas = Tk.Canvas(self.window, width=self.width, height=self.height)
        self.window.canvas.grid(row=1, column=1, columnspan=self.rulewidth, rowspan=self.ruleheight)

        self.buttonless = Tk.Button(self.window, text="Less", command=self.lessneighbours)
        self.buttonless.grid(row=2, column=self.rulewidth + 1, sticky="nesw")

        self.buttonmore = Tk.Button(self.window, text="More", command=self.moreneighbours)
        self.buttonmore.grid(row=1, column=self.rulewidth + 1, sticky="nesw")

        self.buttonless = Tk.Button(self.window, text="Enter", command=self.enterfromDEC)
        self.buttonless.grid(row=0, column=self.rulewidth + 1, sticky="nesw")

        labelsh = []
        # Append a nonlabel
        labelsh.append(Tk.Label(self.window, text=None))
        labelsh[-1].grid(row=0, column=0, sticky="nesw")

        # labelsh.append(Tk.Label(self.window,text = None))
        # labelsh[-1].grid(row = 0,column =self.rulewidth+1)

        labelsh = []
        for i in range(0, self.ruleheight):
            labelsh.append(Tk.Label(self.window, text=str(i)))
            labelsh[-1].grid(row=i + 1, column=0, sticky="nesw")

        self.window.canvas.bind("<Button-1>", self.callback)
        self.update_img()

    def enterfromDEC(self):
        """
        Initializes a rule from a given Decimal number
        """
        DEC = Tk.simpledialog.askinteger("Rule from Decimal", "DEC", initialvalue=1)

        self.rule.rulefromDEC(DEC)
        self.parent.rule = self.rule
        self.ruleheight, self.rulewidth = np.shape(self.rule.rule_array)
        self.width = self.rulewidth * self.mult
        self.height = self.ruleheight * self.mult

        self.clear()
        self.init_rule()

    def moreneighbours(self):
        """
        Expands the rule by allowing for more neighbouring interactions
        """

        if self.rulewidth == 5:
            rule = np.zeros((2, 7), dtype=int)
        elif self.rulewidth == 7:
            rule = np.zeros((2, 9), dtype=int)
        elif self.rulewidth == 9:
            rule = np.zeros((2, 13), dtype=int)
        elif self.rulewidth == 13:
            rule = np.zeros((2, 25), dtype=int)
        elif self.rulewidth == 25:
            rule = np.zeros((2, 25), dtype=int)
        else:
            print("Invalid Rulewidth:", self.rulewidth)
            return

        self.rule.rule_array = rule
        self.parent.update_title_rule()

        self.ruleheight, self.rulewidth = np.shape(self.rule.rule_array)
        self.width = self.rulewidth * self.mult
        self.height = self.ruleheight * self.mult

        self.clear()
        self.init_rule()

    def lessneighbours(self):
        """
        Degrades the possible number of neighbours.
        The list of implemented rules are length: 5,9,13,25
        """
        if self.rulewidth == 5:
            rule = np.zeros((2, 5), dtype=int)
        elif self.rulewidth == 7:
            rule = np.zeros((2, 5), dtype=int)
        elif self.rulewidth == 9:
            rule = np.zeros((2, 7), dtype=int)
        elif self.rulewidth == 13:
            rule = np.zeros((2, 9), dtype=int)
        elif self.rulewidth == 25:
            rule = np.zeros((2, 13), dtype=int)
        else:
            print("Invalid Rulewidth:", self.rulewidth)
            return

        self.rule.rule_array = rule
        self.parent.update_title_rule()

        self.ruleheight, self.rulewidth = np.shape(self.rule.rule_array)
        self.width = self.rulewidth * self.mult
        self.height = self.ruleheight * self.mult

        self.clear()
        self.init_rule()

    def update_img(self):
        """
        Usual update function to update the canvas
        """
        self.myphoto = PIL.Image.fromarray(self.rule.rule_array.astype(bool)).resize(
            (self.width, self.height), 0
        )
        self.photo = PIL.ImageTk.PhotoImage(image=self.myphoto)
        self.window.canvas.create_image(0, self.height, image=self.photo, anchor=Tk.SW)

    def callback(self, event):
        """
        Callback method to handle clicks
        """
        self.parent.focus_set()

        self.adjust_image(event.x, event.y)
        self.parent.update_title_rule()
        self.clear()
        self.init_rule()

    def adjust_image(self, x, y):
        """
        Adjust the image to true/not true
        """
        pixelx = int(y / self.mult)
        pixely = int(x / self.mult)

        self.rule.rule_array[pixelx, pixely] = not (
            (self.rule.rule_array.astype(bool))[pixelx, pixely]
        )

        self.update_img()

    def clear(self):
        """
        Clears grid slaves
        """
        list = self.window.grid_slaves()
        for grid_slave in list:
            grid_slave.destroy()
