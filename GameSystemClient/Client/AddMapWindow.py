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

class AddMapWindow:
    ILLEGAL_CHARS = [";", "\t", "\n", "\b"]

    def __init__(self, master, token) -> None:
        self.__root = Toplevel(master)
        self.__root.title("Add new map")

        self.__token = token

        self.__map_name = StringVar()

        Label(self.__root, text = "Map name: ", font = (14), anchor = "e").grid(row = 0, column = 0, sticky = EW)
        self.__map_name_entry = Entry(self.__root, textvariable = self.__map_name, font = (14))
        self.__map_name_entry.grid(row = 0, column = 1, sticky = EW, columnspan = 2)

        Label(self.__root, text = "Map data:", font = (14), anchor = "center").grid(row = 1, column = 0, columnspan = 3, sticky = EW)

        self.__scrollbar = Scrollbar(self.__root)
        
        self.__map_data_text = Text(self.__root, font = (14), yscrollcommand = self.__scrollbar.set)
        self.__map_data_text.grid(row = 2, column = 0, columnspan = 2, sticky = NSEW, padx = (4, 0))

        self.__scrollbar["command"] = self.__map_data_text.yview
        self.__scrollbar.grid(row = 2, column = 2, sticky = NS, padx = (0, 4))

        self.__send_button = Button(self.__root, text = "Add map", font = (14), command = self.__send_map)
        self.__send_button.grid(row = 3, column = 0, columnspan = 3, sticky = EW, padx = 4, pady = 4)

        window = self.__root.winfo_toplevel()
        window.columnconfigure(0, weight = 1)
        window.columnconfigure(1, weight = 999)
        window.columnconfigure(2, weight = 1)
        window.rowconfigure(0, weight = 1)
        window.rowconfigure(1, weight = 1)
        window.rowconfigure(2, weight = 999)
        window.rowconfigure(3, weight = 1)

    def show(self):
        self.__root.deiconify()
        self.__root.wait_window()

        return 0
    
    def __send_map(self):
        map_name = self.__map_name.get().strip(" \n\t")
        data = self.__map_data_text.get(1.0, "end").strip(" \n\t")

        if len(map_name) == 0:
            messagebox.showerror("Error", "Map name cannot be empty!", parent = self.__root)
            return
        
        if len(data) == 0:
            messagebox.showerror("Error", "Map data cannot be empty!", parent = self.__root)
            return

        for char in AddMapWindow.ILLEGAL_CHARS:
            if map_name.find(char) != -1:
                messagebox.showerror("Error", "Map name contains illegal data!", parent = self.__root)
                return
            if data.find(char) != -1:
                messagebox.showerror("Error", "Map data contains illegal data!", parent = self.__root)
                return
        
        r = requests.post(url = Config.get_connection_string() + "/api/maps", headers = {"Authorization": "Bearer " + self.__token}, json = {"map_name": map_name, "data": data})

        if r.status_code == 200:
            messagebox.showinfo("Successful", "Map added successfully!", parent = self.__root)
            self.exit()
        elif r.status_code == 400:
            result = r.json()
            messagebox.showerror("Error", result["error"])

    def exit(self):
        self.__root.destroy()