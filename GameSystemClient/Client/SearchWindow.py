from Client.Settings import Config
import tkinter
from tkinter import messagebox
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
from Tools.Logger import Logger
from typing import List
import requests

class SearchWindow:
    def __init__(self, master) -> None:
        self.__root = Toplevel(master)
        self.__root.title("Search")

        self.__ok = False

        self.__username = StringVar()
        self.__mapname = StringVar()

        Label(self.__root, text = "User:", anchor = "e", font = (14)).grid(row = 0, column = 0, padx = 4, pady = 4, sticky = EW)
        Label(self.__root, text = "Map name:", anchor = "e", font = (14)).grid(row = 1, column = 0, padx = 4, pady = 4, sticky = EW)

        self.__user_entry = Entry(self.__root, textvariable = self.__username, font = (14))
        self.__user_entry.grid(row = 0, column = 1, padx = 4, pady = 4, sticky = NSEW)

        self.__mapname_entry = Entry(self.__root, textvariable = self.__mapname, font = (14))
        self.__mapname_entry.grid(row = 1, column = 1, padx = 4, pady = 4, sticky = NSEW)

        self.__button = Button(self.__root, text = "Search", font = (14), command = self.__search)
        self.__button.grid(row = 2, column = 0, columnspan = 2, padx = 4, pady = 4, sticky = EW)

        window = self.__root.winfo_toplevel()
        window.columnconfigure(0, weight = 1)
        window.columnconfigure(1, weight = 999)
        window.rowconfigure(0, weight = 999)
        window.rowconfigure(1, weight = 999)
        window.rowconfigure(2, weight = 1)

    def show(self):
        self.__root.deiconify()
        self.__root.wait_window()

        if self.__ok:
            return [
                self.__username.get(),
                self.__mapname.get()
            ]
        else:
            return []
    
    def __search(self):
        if len(self.__username.get()) == 0 and len(self.__mapname.get()) == 0:
            messagebox.showerror("Error", "User and Map name filds cannot be both empty.", parent = self.__root)
            return
        
        self.__ok = True
        self.exit()
    
    def exit(self):
        self.__root.destroy()
