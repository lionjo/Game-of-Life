import tkinter as Tk
import tkinter.filedialog
import tkinter.simpledialog
import PIL.Image, PIL.ImageTk
import numpy as np
import os

from Rules import next_step
from RuleWindow import RuleWindow

class GameofLife(Tk.Frame):
    '''
    Dislay an image on Tkinter.Canvas and delete it on button click
    '''
    def __init__(self, parent,width,height,res,speed=1000):
        '''
        Inititialize the GUI with a button and a Canvas objects
        '''
        Tk.Frame.__init__(self, parent)
        self.parent=parent

        self.width = width
        self.height = height
        self.mult = res

        self.speed = speed
        self.rule = np.array([[0,0,0,1,0,0,0,0,0],[0,0,1,1,0,0,0,0,0]]) # rule_example = np.array([[0,0,1,1,1,0,0,0,0],[0,0,1,0,1,0,0,1,1]])
        self.InitialRule = np.array([[0,0,0,1,0,0,0,0,0],[0,0,1,1,0,0,0,0,0]])

        self.arr = np.random.randint(0,high=2, size=(int(self.height/self.mult),int(self.width/self.mult)))
        self.init_pic()

    def init_pic(self):
        """
        Draw the GUI
        """
        self.parent.title("Our Game of Life")       
        
        self.parent.grid_rowconfigure(0,weight=0)
        self.parent.grid_columnconfigure(0,weight=0)

        self.parent.grid_columnconfigure(8,weight=1)
        self.parent.grid_columnconfigure(0,weight=1)

        # Create a button and append it  a callback method to clear the image          
        self.button_run = Tk.Button(self.parent, text = 'Start', command = self.runthingy)
        self.button_run.grid(row = 1, column = 0, sticky = "e")

        # Create another button         
        self.button_reset = Tk.Button(self.parent, text = 'Reset', command = self.reset)
        self.button_reset.grid(row = 1, column =1)

        self.button_random = Tk.Button(self.parent, text = 'Randomize', command = self.randomize)
        self.button_random.grid(row = 1, column =2)

        self.button_save = Tk.Button(self.parent, text = 'Save', command = self.save)
        self.button_save.grid(row = 1, column =3)

        self.button_open = Tk.Button(self.parent, text = 'Open', command = self.open)
        self.button_open.grid(row = 1, column =4)

        self.button_adjust = Tk.Button(self.parent, text = 'Size', command = self.changesize)
        self.button_adjust.grid(row = 1, column =5)

        self.button_speed = Tk.Button(self.parent, text = 'Speed', command = self.adjustspeed)
        self.button_speed.grid(row = 1, column =6)

        self.button_undo = Tk.Button(self.parent, text = 'Undo', command = self.undo)
        self.button_undo.grid(row = 1, column =7)


        self.button_rule = Tk.Button(self.parent, text = 'Rule', command = self.adjustrule)
        self.button_rule.grid(row = 1, column =8,sticky="w")

        self.canvas = Tk.Canvas(self.parent, width = self.width, height = self.height)
        self.canvas.grid(row = 0,columnspan = 9)



        self.canvas.bind("<Button-1>", self.callback)

        self.update_img()

        
    def adjustrule(self):

        newWindow = RuleWindow(self,self.rule)
        

        #print("state zero: %d,\state one: %d" % (var1.get(), var2.get()))
        #Label(master, text="Rule:").grid(row=0, sticky=W)
        #var1 = Tk.IntVar()
        #Checkbutton(master, text="Value Zero", variable=var1).grid(row=1, sticky=W, onvalue = 1, offvalue = 0, initialvalue=self.InitialRule[0](1))
        #var2 = Tk.IntVar()
        #Checkbutton(master, text="Value One", variable=var2).grid(row=2, sticky=W, onvalue = 1, offvalue = 0, initialvalue=self.InitialRule[1](1))

    def undo(self):
        pass

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

        self.arr[pixelx,pixely] = not((self.arr.astype(bool))[pixelx,pixely])


        self.update_img()

        
   
    def update_img(self):
        self.myphoto = PIL.Image.fromarray(self.arr.astype(bool)).resize((self.width,self.height),0)
        self.photo = PIL.ImageTk.PhotoImage(image = self.myphoto)
        self.canvas.create_image(0, self.height, image=self.photo, anchor=Tk.SW)


    def runthingy(self):
        self.evolve()

        self.button_open['state'] = 'disabled'
        self.button_save['state'] = 'disabled'
        self.button_reset['state'] = 'disabled'
        self.button_random['state'] = 'disabled' 
        self.button_adjust['state'] = 'disabled'   
        self.button_rule['state'] = 'disabled'

        self.button_run.configure(text = 'Stop', command = self.stopthingy)

    def stopthingy(self):
        self.parent.after_cancel(self.cancelid)

        self.button_open['state'] = 'normal'
        self.button_save['state'] = 'normal'
        self.button_reset['state'] = 'normal'
        self.button_random['state'] = 'normal' 
        self.button_adjust['state'] = 'normal'   
        self.button_rule['state'] = 'normal'

        self.button_run.configure(text = 'Start', command = self.runthingy)

    def evolve(self):
        self.arr = next_step(self.arr,self.rule)
        self.update_img()
        self.cancelid = self.parent.after(self.speed,self.evolve)

    def reset(self):
        self.arr = np.zeros(self.arr.shape).astype(int)

        self.update_img()

    def randomize(self):
        self.arr =np.random.randint(0,high=2, size=(int(self.height/self.mult),int(self.width/self.mult)))
        self.update_img()

    def open(self):
        filename = Tk.filedialog.askopenfilename(initialdir=os.getcwd(),filetypes=[("Text Files", "*.dat")])
        loadedarr = np.loadtxt(filename)

        width, height = loadedarr.shape

        self.width = width * self.mult
        self.height = height * self.mult
        self.arr = loadedarr.astype(int)

        self.clear()
        self.init_pic()
        self.update_img()

    def adjustspeed(self):
        self.speed = Tk.simpledialog.askinteger("Adjust Update Pause","Milliseconds:",initialvalue=1000)


    def save(self):
        filename = Tk.filedialog.asksaveasfilename(initialdir=os.getcwd(),filetypes=[("Text Files", "*.dat")],defaultextension='.txt',initialfile="output.dat")

        print(filename)
        if not filename: return

        np.savetxt(filename,self.arr,fmt=int)

    def changesize(self):
        width = Tk.simpledialog.askinteger("Input","Width",initialvalue=400)
        height = Tk.simpledialog.askinteger("Input","Height",initialvalue=400)
        res = Tk.simpledialog.askinteger("Input","Resolution",initialvalue=10)

        if not width or not height or not res:
            return


        self.width = width
        self.height = height
        self.mult = res
       
        self.clear()
        self.arr = np.random.randint(0,high=2, size=(int(self.height/self.mult),int(self.width/self.mult)))
        self.init_pic() 


    def clear(self):
        list = self.parent.grid_slaves()
        for l in list:
            l.destroy()



# Main method
def main(width=400,height=400,res=10,speed=1000):
    root=Tk.Tk()
    GameofLife(root,width,height,res,speed)
    root.mainloop()

