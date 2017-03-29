#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys   # for flush
import copy

from tkinter import *
from tkinter import Tk
from tkinter import tix as Tix
from tkinter.ttk import Frame, Button, Label, Style
from tkinter.ttk import Entry
from tkinter import simpledialog

from sudoku_solve import  sudoku_txt, sudoku_solve


class Solver(Frame):
 
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.solve_entry = None
        self.texti = None
        self.texto = None
        
        self.initUI()
        
    def initUI(self):

        self.parent.title("Sudoku")
     
        frame0 = Tix.Frame(self, relief=RAISED, bd=1)
        frame0.pack(side=TOP)
        frame1, frame2 = self.MkEntries(frame0)
        frame3 = self.MkButtons()   
        
        frame1.pack(side=LEFT)
        frame2.pack(side=RIGHT)
        frame3.pack(side=BOTTOM,fill=X)

        self.pack()
        
    def quitNow(self):
        self.parent.destroy()
        
    def solveNow(self): 
        
        txi = self.texti
        if txi != None:
            txt = txi.get(1.0, END)
        if txt[0:5] == "Enter":
            print("Paste or type in 81 chars")
            return
        if len(txt) < 90:
            print("Not enough characters", len(txt), flush=True)
            return
        for i in range(len(txt)):
            if not txt[i].isdigit():
                if txt[i] != '\n':
                    print("Invalid character", txt[i], flush=True)
                    return
        
        #sudoku_txt_print("Sudoku is", txt)
        txt = sudoku_txt(sudoku_solve(txt))
        if len(txt) == 0:
            return
        txo = self.texto
        txo.delete(1.0, END)
        txo.insert(1.0, txt)

        
    def ok(self):
        print("Sudoku is", self.e.get(), flush=True)
        self.destroy()
            
    def MkEntries(self, parent):
        top = parent
        wi = Tix.Frame(top, relief=RAISED, bd=1)  
        txi = Tix.Text(wi, height=11, width=20, takefocus=True)
        txi.insert(1.0, 
            "Enter known values\nas a 9x9 array\nwith 0 for unknowns")
        txi.pack(side=LEFT)
        self.texti = txi
        
        wo = Tix.Frame(top, relief=RAISED, bd=1)  
        txo = Tix.Text(wo, height=11, width=20)
        txo.pack(side=RIGHT)
        self.texto = txo
     
        return wi,wo
    
    def MkButtons(self):
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10') 
        top = self.parent
        w = Tix.Frame(top, relief=RAISED, bd=1)    
        solve = Button(w, text="Solve", command=self.solveNow)
        solve.pack(side=LEFT)
        clo = Button(w, text="Close", command=self.quitNow)
        clo.pack(side=RIGHT)       
        
        return w
    
# end of Solver ---------------------------------------------
    
def main(): 
    #print(TkVersion)
    root = Tk()
    app = Solver(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
