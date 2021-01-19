from Client.SearchWindow import SearchWindow
from Client.AddMapWindow import AddMapWindow
from Client.MapDetailsWindow import MapDetailsWindow
from Tools.Logger import Logger
from Client.Settings import *
import tkinter
from tkinter import messagebox
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from typing import List

import requests

def not_implemented():
    print("NOT IMPLEMENTED")

class MainWindow:
    def __init__(self, token, username) -> None:
        self.__root = Tk()
        self.__root.title(Config.NAME)
        self.__token = token
        self.__username = username

        self.__init_ui()

        self.__maps = []
        self.__refresh_maps_list()

        self.__root.mainloop()
    
    def __init_ui(self):
        self.__init_menubar()

        self.__frame = Frame(self.__root)
        self.__init_list()
        self.__init_statusbar()
        self.__frame.grid(row = 0, column = 0, sticky = NSEW)

        self.__frame.columnconfigure(0, weight = 999)
        self.__frame.columnconfigure(1, weight = 1)
        self.__frame.rowconfigure(0, weight = 1)
        self.__frame.rowconfigure(1, weight = 999)
        self.__frame.rowconfigure(2, weight = 1)

        window = self.__root.winfo_toplevel()
        window.columnconfigure(0, weight = 1)
        window.rowconfigure(0, weight = 1)

        self.__root.geometry("{0}x{1}".format(600, 600))
         
    def __init_menubar(self):
        self.__menubar = Menu(self.__root)

        # FileMenu
        self.__filemenu = Menu(self.__menubar, tearoff = 0)
        self.__filemenu.add_command(label = "Exit", command = self.__exit)

        self.__menubar.add_cascade(label = "File", menu = self.__filemenu)

        # QueriesMenu
        self.__querymenu = Menu(self.__menubar, tearoff = 0)
        self.__querymenu.add_command(label = "Add map", command = self.__open_add_map)
        self.__querymenu.add_command(label = "Find map", command = self.__open_search_dialog)
        self.__querymenu.add_separator()
        self.__querymenu.add_command(label = "Refresh map list", command = self.__refresh_maps_list)

        self.__menubar.add_cascade(label = "Maps", menu = self.__querymenu)

        self.__root.config(menu = self.__menubar)

    def __init_list(self):
        self.__scrollbar = Scrollbar(self.__frame, orient = VERTICAL)
        
        self.__listbox = Listbox(self.__frame, yscrollcommand = self.__scrollbar.set, font = (14))
        self.__listbox.grid(row = 1, column = 0, sticky = NSEW)
        self.__listbox.focus_set()

        self.__listbox.bind("<<ListboxSelect>>", self.__list_select_callback)

        self.__scrollbar["command"] = self.__listbox.yview
        self.__scrollbar.grid(row = 1, column = 1, sticky = NS)
    
    def __init_statusbar(self):
        self.__statusbar = Label(self.__frame, text = "Ready...", anchor = W, font = (14))
        self.__statusbar.grid(row = 2, column = 0, columnspan = 2, sticky = EW)

    def __set_status_bar(self, text: str):
        self.__statusbar["text"] = self.__username + ": " +  text
    
    def __exit(self):
        self.__root.destroy()
    
    def __refresh_maps_list(self):
        self.__clean_maps_list()
        self.__set_status_bar("Loading maps list...")
        self.__root.after(500, self.__load_maps_list)

    def __load_maps_list(self):
        r =  None
        try:
            r = requests.get(url = Config.get_connection_string() + "/api/maps")
        except requests.exceptions.RequestException:
            messagebox.showerror("Connection error", "Failed to connect with to server")
            return

        self.__maps = r.json()
        self.__show_maps_list()
        
        self.__set_status_bar("Maps loaded.")
    
    def __show_maps_list(self):
        self.__clean_maps_list()
        for map_data in self.__maps:
            value = f"{map_data['map_name']} | added by {map_data['username']} | id: {map_data['map_id']}"
            self.__listbox.insert(END, value)
    
    def __list_select_callback(self, event):
        Logger.log("List clicked.")
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            text = str(event.widget.get(index))
            map_name = text[:text.find("|")-1]
            Logger.log(f"Map selected: '{map_name}'")
            self.__open_map_details(map_name)
    
    def __open_map_details(self, map_name):
        map_data = ""
        for map in self.__maps:
            if map["map_name"] == map_name:
                map_data = map
                break
        MapDetailsWindow(self.__root, map_data, self.__username, self.__token).show()
    
    def __open_add_map(self):
        window = AddMapWindow(self.__root, self.__token)
        rs = window.show()

        if rs == 0:
            self.__refresh_maps_list()
    
    def __open_search_dialog(self):
        window = SearchWindow(self.__root)
        ls = window.show()

        if len(ls) == 0:
            return
        
        r =  None
        try:
            r = requests.get(url = Config.get_connection_string() + "/api/maps")
        except requests.exceptions.RequestException:
            messagebox.showerror("Connection error", "Failed to connect with to server")
            return

        self.__maps = r.json()

        if len(ls[0]) == 0:
            self.__maps = list(filter((lambda x: x["map_name"].find(ls[1]) != -1), self.__maps))
        elif len(ls[1]) == 0:
            self.__maps = list(filter((lambda x: x["username"].find(ls[0]) != -1), self.__maps))
        else:
            self.__maps = list(filter((lambda x: x["username"].find(ls[0]) != -1 and x["map_name"].find(ls[1]) != -1), self.__maps))
        
        self.__show_maps_list()
    
    def __clean_maps_list(self):
        self.__listbox.delete(0, END)