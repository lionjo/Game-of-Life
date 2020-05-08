import tkinter as Tk
import tkinter.filedialog
import tkinter.simpledialog
import PIL.Image, PIL.ImageTk
import numpy as np
import os

mywidth=400
myheight=400

class GameofLife(Tk.Frame):
    '''
    Dislay an image on Tkinter.Canvas and delete it on button click
    '''
    def __init__(self, parent):
        '''
        Inititialize the GUI with a button and a Canvas objects
        '''
        Tk.Frame.__init__(self, parent)
        self.parent=parent
        self.init_pic()

    def init_pic(self):
        """
        Draw the GUI
        """
        self.parent.title("Our Game of Life")       
        
        self.arr =np.random.randint(0,high=2, size=(40,40)).astype(bool)
        self.parent.grid_rowconfigure(0,weight=0)
        self.parent.grid_columnconfigure(0,weight=0)

        self.parent.grid_columnconfigure(4,weight=1)
        self.parent.grid_columnconfigure(0,weight=1)


        # Create a button and append it  a callback method to clear the image          
        self.mybotton = Tk.Button(self.parent, text = 'run', command = self.runthingy)
        self.mybotton.grid(row = 1, column = 0, sticky = "e")

        # Create another button         
        self.mybotton2 = Tk.Button(self.parent, text = 'reset', command = self.reset)
        self.mybotton2.grid(row = 1, column =1)

        self.button_random = Tk.Button(self.parent, text = 'randomize', command = self.randomize)
        self.button_random.grid(row = 1, column =2)

        self.button_random = Tk.Button(self.parent, text = 'save', command = self.save)
        self.button_random.grid(row = 1, column =3)

        self.button_random = Tk.Button(self.parent, text = 'open', command = self.open)
        self.button_random.grid(row = 1, column =4,sticky="w")

        self.canvas = Tk.Canvas(self.parent, width = mywidth, height = myheight)
        self.canvas.grid(row = 0,columnspan = 5)

        self.canvas.bind("<Button-1>", self.callback)

        self.update_img()
    

    def callback(self,event):
        '''
        Callback method to delete image
        '''
        self.parent.focus_set()
        print("clicked at", event.x, event.y)

        self.adjust_image(event.x,event.y)


    def adjust_image(self,x,y):
        '''
        Adjust the image to true/not true
        '''
        pixelx = int(y/10)
        pixely = int(x/10)

        print("Trying to change pixel", pixelx,pixely)

        self.arr[pixelx,pixely] = not(self.arr[pixelx,pixely])


        self.update_img()
        #self.myphoto = PIL.Image.fromarray(self.arr).resize((mywidth,myheight),0)
        #self.photo = PIL.ImageTk.PhotoImage(image = self.myphoto)

        #self.canvas.create_image(0, myheight, image=self.photo, anchor=Tk.SW)
        

    @staticmethod
    def arr2photo(arr):
        myphoto=PIL.Image.fromarray(arr).resize((mywidth,myheight),0)
        return PIL.ImageTk.PhotoImage(image = myphoto)
    
    def update_img(self):
        self.myphoto = PIL.Image.fromarray(self.arr).resize((mywidth,myheight),0)
        self.photo = PIL.ImageTk.PhotoImage(image = self.myphoto)
        self.canvas.create_image(0, myheight, image=self.photo, anchor=Tk.SW)


    def runthingy(self):
        pass

    def reset(self):
        self.arr = np.zeros(self.arr.shape).astype(bool)

        self.myphoto = PIL.Image.fromarray(self.arr).resize((mywidth,myheight),0)
        self.photo = PIL.ImageTk.PhotoImage(image = self.myphoto)

        self.canvas.create_image(0, 400, image=self.photo, anchor=Tk.SW)

    def randomize(self):
        pass

    def open(self):
        filename = Tk.filedialog.askopenfilename(initialdir=os.getcwd(),filetypes=[("Text Files", "*.dat")])
        loadedarr = np.loadtxt(filename)

        


    def save(self):
        filename = Tk.filedialog.asksaveasfilename(initialdir=os.getcwd(),filetypes=[("Text Files", "*.dat")],defaultextension='.txt',initialfile="output.dat")

        print(filename)
        if not filename: return

        np.savetxt(filename,self.arr)


"""
def callback(event):
    window.focus_set()
    print("clicked at", event.x, event.y)

"""
"""
window = tkinter.Tk()

window.bind("<Button-1>", callback)

window.title("Our Game of Life")




height, width = cv_img.shape

canvas = tkinter.Canvas(window, width = mywidth, height = myheight)
canvas.pack()

myphoto=PIL.Image.fromarray(cv_img).resize((mywidth,myheight),0)


photo = PIL.ImageTk.PhotoImage(image = myphoto)



canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

window.mainloop()
"""


# Main method
def main():
    root=Tk.Tk()
    d=GameofLife(root)
    root.mainloop()

# Main program       
if __name__=="__main__":
    main()