from tkinter import *
import tkinter as tk



class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.do_stuff()



    def dienstag(self,tvar):
        if (tvar == 1):
            print(text='Irrigate on Tuesday')

    def mittwoch(self,wvar):
        if (wvar == 1):
            print('Irrigate on Wednesday')

    def donnerstag(self,thvar):
        if (thvar == 1):
            print('Irrigate on Thursday')

    def freitag(self,fvar):
        if (fvar == 1):
            print('Irrigate on Friday')

    def samstag(self, savar):
        if (savar == 1):
            print('Irrigate on Saturday')

    def sonntag(self, suvar):
        if (suvar == 1):
            print('Irrigate on Sunday');
    def do_stuff(self):
        self.w1 = Scale(self, from_=0, to=200, orient=HORIZONTAL)
        self.w1.pack()
        self.w2 = Scale(self, from_=0, to=200, orient=HORIZONTAL)
        self.w2.pack()
        self.w3 = Scale(self, from_=0, to=200, orient=HORIZONTAL)
        self.w3.pack()
        print(self.w1.get(), self.w2.get(), self.w3.get())
        mvar = tk.IntVar()
        tvar = tk.IntVar()
        wvar = tk.IntVar()
        thvar = tk.IntVar()
        fvar = tk.IntVar()
        savar = tk.IntVar()
        suvar = tk.IntVar()
        #Button(self, text='Show Runtimes', command=self.start).pack()
        self.monday = tk.Checkbutton(self, text='Monday', variable=mvar, onvalue=1, offvalue=0, command=self.montag)
        self.monday.pack()
        self.tuesday = tk.Checkbutton(self, text='Tuesday', variable=tvar, onvalue=1, offvalue=0, command=self.dienstag(tvar))
        self.tuesday.pack()
        self.wednesday = tk.Checkbutton(self, text='Wednesday', variable=wvar, onvalue=1, offvalue=0, command=self.mittwoch(wvar))
        self.wednesday.pack()
        self.thursday = tk.Checkbutton(self, text='Thursday', variable=thvar, onvalue=1, offvalue=0, command=self.donnerstag(thvar))
        self.thursday.pack()
        self.friday = tk.Checkbutton(self, text='Friday', variable=fvar, onvalue=1, offvalue=0, command=self.freitag(fvar))
        self.friday.pack()
        self.saturday = tk.Checkbutton(self, text='Saturday', variable=savar, onvalue=1, offvalue=0, command=self.samstag(savar))
        self.saturday.pack()
        self.sunday = tk.Checkbutton(self, text='Sunday', variable=suvar, onvalue=1, offvalue=0, command=self.sonntag(suvar))
        self.sunday.pack()
        #print(self.monday.get(), self.tuesday.get(), self.wednesday.get(), self.thursday.get(), self.friday.get(),
              #self.saturday.get(), self.sunday.get())

        def montag():
            if(mvar == 1):
                print(text='Irrigate on Monday')

    #def start(self):


root = tk.Tk()
app = Application(master=root)
app.mainloop()