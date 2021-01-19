import tkinter
from tkinter import messagebox
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
from typing import List
import requests
from Client.Settings import *
from Tools.Logger import Logger

class RegisterWindow:
    def __init__(self, master) -> None:
        self.__root = tkinter.Toplevel(master)
        self.__root.title("Register")
        self.__root.resizable(False, False)

        self.__init_ui()

        self.__root.geometry("{0}x{1}".format(300, 164))

        self.token = ""
    
    def __init_ui(self):
        self.__user = StringVar()
        self.__email = StringVar()
        self.__pass = StringVar()
        self.__country = StringVar()

        self.__user_label = Label(self.__root, text = "Username: ", font = (14))
        self.__user_label.grid(row = 0, column = 0, padx = 4, pady = 4, sticky = E)
        self.__user_entry = Entry(self.__root, textvariable = self.__user, font = (14), width = ENTRIES_WIDTH)
        self.__user_entry.grid(row = 0, column = 1)

        self.__email_label = Label(self.__root, text = "Email: ", font = (14))
        self.__email_label.grid(row = 1, column = 0, padx = 4, pady = 4, sticky = E)
        self.__email_entry = Entry(self.__root, textvariable = self.__email, font = (14), width = ENTRIES_WIDTH)
        self.__email_entry.grid(row = 1, column = 1)

        self.__password_label = Label(self.__root, text = "Password: ", font = (14))
        self.__password_label.grid(row = 2, column = 0, padx = 4, pady = 4, sticky = E)
        self.__password_entry = Entry(self.__root, textvariable = self.__pass, font = (14), show = "*", width = ENTRIES_WIDTH)
        self.__password_entry.grid(row = 2, column = 1)

        self.__country_label = Label(self.__root, text = "Country: ", font = (14))
        self.__country_label.grid(row = 3, column = 0, padx = 4, pady = 4, sticky = E)

        r =  None
        try:
            r = requests.get(url = Config.get_connection_string() + "/api/countries")
        except requests.exceptions.RequestException:
            messagebox.showerror("Connection error", "Failed to connect with to server", parent = self.__root)
            self.__exit()
            return
        countries: List = r.json()
        countries.sort()

        self.__country_combobox = ttk.Combobox(self.__root, values = countries, textvariable = self.__country, font = (14), width = ENTRIES_WIDTH - 2)
        self.__country_combobox.grid(row=3, column=1)
        self.__country_combobox.current(0)

        self.__register_button = Button(self.__root, text = "Register", font = (14), width = 8, command = self.__register)
        self.__register_button.grid(row = 4, column = 1, sticky = EW)
    
    def __register(self):
        Logger.log("Trying to Register...")
        payload = {
            "email": self.__email.get(),
            "username": self.__user.get(),
            "password": self.__pass.get(),
            "country": self.__country.get()
        }
        Logger.log("Making POST request...")
        
        r =  None
        try:
            r = requests.post(url = Config.get_connection_string() + "/api/auth/sign", json = payload)
        except requests.exceptions.RequestException:
            messagebox.showerror("Connection error", "Failed to connect with to server", parent = self.__root)
            self.__exit()
            return

        Logger.log(f"Recieved response: {r.status_code}")
        if r.status_code == 204:
            messagebox.showinfo("Register info", "Successfully registered!", parent = self.__root)
            self.__exit()
        else:
            data = r.json()
            messagebox.showerror("Register error", data["error"], parent = self.__root)
    
    def show(self):
        self.__root.mainloop()

    def __exit(self):
        self.__root.destroy()