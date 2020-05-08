import tkinter as Tk
import tkinter.filedialog
import tkinter.simpledialog
import PIL.Image, PIL.ImageTk
import numpy as np
import os



class GameofLife(Tk.Frame):
    '''
    Dislay an image on Tkinter.Canvas and delete it on button click
    '''
    def __init__(self, parent,width,height,res):
        '''
        Inititialize the GUI with a button and a Canvas objects
        '''
        Tk.Frame.__init__(self, parent)
        self.parent=parent

        self.width = width
        self.height = height
        self.mult = res

        self.init_pic()

    def init_pic(self):
        """
        Draw the GUI
        """
        self.parent.title("Our Game of Life")       
        
        self.arr =np.random.randint(0,high=2, size=(int(self.height/self.mult),int(self.width/self.mult))).astype(bool)

        self.parent.grid_rowconfigure(0,weight=0)
        self.parent.grid_columnconfigure(0,weight=0)

        self.parent.grid_columnconfigure(5,weight=1)
        self.parent.grid_columnconfigure(0,weight=1)

        # Create a button and append it  a callback method to clear the image          
        self.button_run = Tk.Button(self.parent, text = 'Run', command = self.runthingy)
        self.button_run.grid(row = 1, column = 0, sticky = "e")

        # Create another button         
        self.button_reset = Tk.Button(self.parent, text = 'Reset', command = self.reset)
        self.button_reset.grid(row = 1, column =1)

        self.button_random = Tk.Button(self.parent, text = 'Randomize', command = self.randomize)
        self.button_random.grid(row = 1, column =2)

        self.button_save = Tk.Button(self.parent, text = 'Save', command = self.save)
        self.button_save.grid(row = 1, column =3)

        self.button_open = Tk.Button(self.parent, text = 'Open', command = self.open)
        self.button_open.grid(row = 1, column =4,sticky="w")

        self.button_adjust = Tk.Button(self.parent, text = 'Adjust', command = self.changesize)
        self.button_adjust.grid(row = 1, column =5,sticky="w")

        self.canvas = Tk.Canvas(self.parent, width = self.width, height = self.height)
        self.canvas.grid(row = 0,columnspan = 6)

        self.canvas.bind("<Button-1>", self.callback)

        self.update_img()

        

    

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

        self.arr[pixelx,pixely] = not(self.arr[pixelx,pixely])


        self.update_img()

        

    @staticmethod
    def arr2photo(arr):
        myphoto=PIL.Image.fromarray(arr).resize((self.width,self.height),0)
        return PIL.ImageTk.PhotoImage(image = myphoto)
    
    def update_img(self):
        self.myphoto = PIL.Image.fromarray(self.arr).resize((self.width,self.height),0)
        self.photo = PIL.ImageTk.PhotoImage(image = self.myphoto)
        self.canvas.create_image(0, self.height, image=self.photo, anchor=Tk.SW)


    def runthingy(self):
        pass

    def reset(self):
        self.arr = np.zeros(self.arr.shape).astype(bool)

        self.update_img()

    def randomize(self):
        self.arr =np.random.randint(0,high=2, size=(int(self.height/self.mult),int(self.width/self.mult))).astype(bool)
        self.update_img()

    def open(self):
        filename = Tk.filedialog.askopenfilename(initialdir=os.getcwd(),filetypes=[("Text Files", "*.dat")])
        loadedarr = np.loadtxt(filename)

        self.arr = loadedarr.astype(bool)
        self.update_img()

        


    def save(self):
        filename = Tk.filedialog.asksaveasfilename(initialdir=os.getcwd(),filetypes=[("Text Files", "*.dat")],defaultextension='.txt',initialfile="output.dat")

        print(filename)
        if not filename: return

        np.savetxt(filename,self.arr)

    def changesize(self):
        width = Tk.simpledialog.askinteger("Input","Width",initialvalue=400)
        height = Tk.simpledialog.askinteger("Input","Height",initialvalue=400)
        res = Tk.simpledialog.askinteger("Input","Resolution",initialvalue=10)

        if not width or not height or not res:
            return
            

        self.width = width
        self.height = height
        self.mult = res
       
        self.init_pic()

# Main method
def main(width=400,height=400,res=10):
    root=Tk.Tk()
    d=GameofLife(root,width,height,res)
    root.mainloop()

