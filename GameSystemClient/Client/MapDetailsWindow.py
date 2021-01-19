import tkinter
from tkinter import messagebox
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import font

from requests.api import request
from Tools.Logger import Logger
from typing import List, Dict, Any
import requests
from Client.Settings import *
from Client.GameManager import GameManager

class MapDetailsWindow:
    def __init__(self, master, map_data: Dict[str, Any], username, token: str) -> None:
        self.__root = Toplevel(master)
        self.__root.title("Map - " + map_data["map_name"])

        self.__username = username
        
        r =  None
        try:
            r = requests.get(url = Config.get_connection_string() + "/api/maps/" + map_data["map_id"])
            self.__map_data = r.json()
        except requests.exceptions.RequestException:
            messagebox.showerror("Connection error", "Failed to connect with to server", parent = self.__root)
            return
        
        self.__token = token

        self.__country = StringVar()
        self.__mode = StringVar()
        self.__mode_options = ["All", "Last 365 days", "Last 30 days", "Last 7 days", "Last day"]
        self.__mode.set(self.__mode_options[0])

        self.__init_ui()
        self.__root.geometry("{0}x{1}".format(500, 500))
    
    def __init_ui(self):
        self.__frame = Frame(self.__root)

        self.__map_details_label = Label(self.__frame, text = "MAP DETAILS", font = (14))
        self.__map_details_label.grid(row = 0, column = 0, sticky = NSEW, columnspan = 2, rowspan = 2)
        
        Label(self.__frame, text = "Map name:", anchor = "e", font = (14)).grid(row = 2, column = 0, sticky = EW)
        Label(self.__frame, text = "Map id:", anchor = "e", font = (14)).grid(row = 3, column = 0, sticky = EW)
        Label(self.__frame, text = "Added by:", anchor = "e", font = (14)).grid(row = 4, column = 0, sticky = EW)

        Label(self.__frame, text = self.__map_data["map_name"], anchor = "w", font = (14)).grid(row = 2, column = 1, sticky = EW, columnspan = 2)
        Label(self.__frame, text = self.__map_data["map_id"], anchor = "w", font = (14)).grid(row = 3, column = 1, sticky = EW, columnspan = 2)
        Label(self.__frame, text = self.__map_data["username"], anchor = "w", font = (14)).grid(row = 4, column = 1, sticky = EW, columnspan = 2)

        separator = ttk.Separator(self.__frame, orient = 'horizontal')
        separator.grid(row = 5, column = 0, columnspan = 3, sticky = EW, pady = 8)

        Label(self.__frame, text = "RANKING", font = (14)).grid(row = 6, column = 0, columnspan = 3, sticky = EW)

        r =  None
        try:
            r = requests.get(url = Config.get_connection_string() + "/api/countries")
        except requests.exceptions.RequestException:
            messagebox.showerror("Connection error", "Failed to connect with to server", parent = self.__root)
            self.__root.destroy()
            return

        countries: List = r.json()
        countries.sort()
        countries.insert(0, "World")
        self.__country_combobox = ttk.Combobox(self.__frame, values = countries, textvariable = self.__country, font = (14), justify = "center")
        self.__country_combobox.grid(row = 7, column = 1, columnspan = 1, sticky = EW)
        self.__country_combobox.current(0)
        self.__country_combobox.bind("<<ComboboxSelected>>", self.__country_changed)

        self.__mode_optionsmenu = OptionMenu(self.__frame, self.__mode, *self.__mode_options, command = self.__mode_changed)
        self.__mode_optionsmenu.config(font=(14))
        self.__mode_optionsmenu.grid(row = 7, column = 0, columnspan = 1, sticky = EW)

        self.__scrollbar = Scrollbar(self.__frame, orient = VERTICAL)
        self.__ranking_listbox = Listbox(self.__frame, yscrollcommand = self.__scrollbar.set, font = (14))
        self.__ranking_listbox.grid(row = 8, column = 0, sticky = NSEW, columnspan = 2)
        self.__ranking_listbox.focus_set()

        self.__scrollbar["command"] = self.__ranking_listbox.yview
        self.__scrollbar.grid(row = 8, column = 2, sticky = NS)

        if Config.GAME_EXECUT_COMMAND == "":
            self.__play_button = Button(self.__frame, text = "PLAY MAP", command = self.__play_map, font = (14), state = DISABLED)
        else:
            self.__play_button = Button(self.__frame, text = "PLAY MAP", command = self.__play_map, font = (14))
        self.__play_button.grid(row = 9, column = 0, columnspan = 3, sticky = NSEW, padx = 8, pady = 8)
        
        self.__frame.grid(row = 0, column = 0, sticky = NSEW)
        self.__frame.columnconfigure(0, weight = 999)
        self.__frame.columnconfigure(1, weight = 999)
        self.__frame.columnconfigure(2, weight = 1)
        self.__frame.rowconfigure(0, weight = 1)
        self.__frame.rowconfigure(1, weight = 1)
        self.__frame.rowconfigure(2, weight = 1)
        self.__frame.rowconfigure(3, weight = 1)
        self.__frame.rowconfigure(4, weight = 1)
        self.__frame.rowconfigure(5, weight = 1)
        self.__frame.rowconfigure(6, weight = 1)
        self.__frame.rowconfigure(7, weight = 1)
        self.__frame.rowconfigure(8, weight = 999)
        self.__frame.rowconfigure(9, weight = 1)

        window = self.__root.winfo_toplevel()
        window.columnconfigure(0, weight = 1)
        window.rowconfigure(0, weight = 1)

        r =  None
        try:
            r = requests.get(url = Config.get_connection_string() + f"/api/ranking/{self.__map_data['map_id']}:World:0")
        except requests.exceptions.RequestException:
            messagebox.showerror("Connection error", "Failed to connect with to server", parent = self.__root)
            self.__root.destroy()
            return
        
        scores: List = r.json()
        sorted_scores = sorted(scores, key = lambda x: x["points"], reverse = True)

        self.__fill_list(sorted_scores)
    
    def __country_changed(self, event):
        country: str = self.__country.get()
        mode: int = self.__get_mode(self.__mode.get())

        r =  None
        try:
            r = requests.get(url = Config.get_connection_string() + f"/api/ranking/{self.__map_data['map_id']}:{country}:{mode}")
        except requests.exceptions.RequestException:
            messagebox.showerror("Connection error", "Failed to connect with to server", parent = self.__root)
            self.__root.destroy()
            return
        scores: List = r.json()
        sorted_scores = sorted(scores, key = lambda x: x["points"], reverse = True)
        self.__fill_list(sorted_scores)
    
    def __mode_changed(self, event):
        country: str = self.__country.get()
        mode: int = self.__get_mode(self.__mode.get())

        r =  None
        try:
            r = requests.get(url = Config.get_connection_string() + f"/api/ranking/{self.__map_data['map_id']}:{country}:{mode}")
        except requests.exceptions.RequestException:
            messagebox.showerror("Connection error", "Failed to connect with to server", parent = self.__root)
            self.__root.destroy()
            return
        scores: List = r.json()
        sorted_scores = sorted(scores, key = lambda x: x["points"], reverse = True)
        self.__fill_list(sorted_scores)
    
    def __get_mode(self, mode) -> int:
        for i in range(len(self.__mode_options)):
            if mode == self.__mode_options[i]:
                return i
        return -1

    def __fill_list(self, data):
        self.__ranking_listbox.delete(0, END)

        for score in data:
            user = score["user"]
            points = score["points"]
            day = str(score["day"]) if score["day"] > 9 else "0" + str(score["day"])
            month = str(score["month"]) if score["month"] > 9 else "0" + str(score["month"])
            year = score["year"]

            value = f"{points} - {user} - {day}.{month}.{year}"
            if user == self.__username:
                value = value.upper()

            self.__ranking_listbox.insert(END, value)
    
    def __play_map(self):
        r = None
        try:
            r = requests.get(url = Config.get_connection_string() + f"/api/score/user/{self.__username}")
        except requests.exceptions.RequestException:
            messagebox.showerror("Connection error", "Failed to connect with to server", parent = self.__root)
            self.__root.destroy()
            return
        
        scores: List = r.json()

        my_score = None
        for score in scores:
            if score["map_id"] == self.__map_data["map_id"]:
                my_score = score
        
        points = 0
        if my_score != None:
            points = my_score["points"]
        
        new_points = GameManager.start_game(self.__username, self.__map_data["map_name"], self.__map_data["data"], points)
        if new_points == -1:
            messagebox.showerror("Error", "Game crashed!", parent = self.__root)
            return
        elif new_points == -2:
            messagebox.showerror("Error", "Couldn't create game config file!", parent = self.__root)
            return
        elif new_points == -3:
            messagebox.showerror("Error", "Couldn't read game result file!", parent = self.__root)
            return
        elif new_points == -4:
            messagebox.showerror("Error", "Result file does not contain an integer!", parent = self.__root)
            return
        elif new_points == -5:
            messagebox.showerror("Error", "Result is less then 0!", parent = self.__root)
            return
        elif new_points == -6:
            messagebox.showerror("Error", "Game does not exists!", parent = self.__root)
            return
        
        if new_points > points:            
            r = requests.post(url = Config.get_connection_string() + "/api/score", headers = {"Authorization": "Bearer " + self.__token}, json = {"map_id": self.__map_data["map_id"], "score": new_points})
            if r.status_code != 204:
                messagebox.showerror("Error", r.json()["error"], parent = self.__root)
            else:
                Logger.log("New score saved.")
                messagebox.showinfo("Success", "New score saved!", parent = self.__root)

                try:
                    r = requests.get(url = Config.get_connection_string() + f"/api/ranking/{self.__map_data['map_id']}:{self.__country.get()}")
                    scores: List = r.json()
                    sorted_scores = sorted(scores, key = lambda x: x["points"], reverse = True)
                    self.__fill_list(sorted_scores)
                except requests.exceptions.RequestException:
                    messagebox.showerror("Connection error", "Failed to connect with to server", parent = self.__root)
                    self.__root.destroy()
                    return

        else:
            Logger.log("Old score remains.")
            messagebox.showinfo("Success", "Old score remains...", parent = self.__root)


    def show(self):
        self.__root.mainloop()