import numpy as np
import tkinter as Tk
import PIL.Image, PIL.ImageTk


class RuleWindow(Tk.Frame):
    '''
    Dislay an image on Tkinter.Canvas and delete it on button click
    '''
    def __init__(self,parent,rule):
        '''
        Inititialize the GUI with a button and a Canvas objects
        '''
        self.window = Tk.Toplevel(parent)
        self.parent=parent
        self.rule = rule
        self.mult = 20
        self.ruleheight, self.rulewidth = np.shape(rule)
        self.width = self.rulewidth*self.mult
        self.height = self.ruleheight*self.mult

        self.init_rule()

    def init_rule(self):
        """
        Draw the GUI
        """
        self.window.title("Set the rule") 

        self.window.grid_rowconfigure(0,weight=0)
        self.window.grid_columnconfigure(0,weight=0)

        #self.window.grid_columnconfigure(self.rulewidth,weight=1)
        #self.window.grid_columnconfigure(0,weight=1)

        # Create a button and append it  a callback method to clear the image     
        # 
        #
        labels = []
        for i in range(0,self.rulewidth):
            labels.append(Tk.Label(self.window,text = str(i)))
            labels[-1].grid(row = 0, column = i)


        self.window.canvas = Tk.Canvas(self.window, width = self.width, height = self.height)
        self.window.canvas.grid(row = 1,column = 1,columnspan = self.rulewidth, rowspan = self.ruleheight)

        labelsh = []
        # Append a nonlabel
        labelsh.append(Tk.Label(self.window,text = None))
        labelsh[-1].grid(row = 0, column = 0)

        labelsh = []
        for i in range(0,self.ruleheight):
            labelsh.append(Tk.Label(self.window,text = str(i)))
            labelsh[-1].grid(row = i+1, column = 0)


        self.window.canvas.bind("<Button-1>", self.callback)    
        self.update_img()


    def update_img(self):
        self.myphoto = PIL.Image.fromarray(self.rule.astype(bool)).resize((self.width,self.height),0)
        self.photo = PIL.ImageTk.PhotoImage(image = self.myphoto)
        self.window.canvas.create_image(0, self.height, image=self.photo, anchor=Tk.SW)


    def callback(self,event):
        '''
        Callback method to handle clicks
        '''
        self.parent.focus_set()

        self.adjust_image(event.x,event.y)

    def adjust_image(self,x,y):
        '''
        Adjust the image to true/not true
        '''
        pixelx = int(y/self.mult)
        pixely = int(x/self.mult)

        self.rule[pixelx,pixely] = not((self.rule.astype(bool))[pixelx,pixely])


        self.update_img()