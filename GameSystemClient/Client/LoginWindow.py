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
from Client.Settings import *
from Client.RegisterWindow import RegisterWindow

class LoginWindow:
    def __init__(self) -> None:
        self.__root = Tk()
        self.__root.title("Login")
        self.__root.resizable(False, False)

        self.__init_ui()

        self.__root.geometry("{0}x{1}".format(300, 100))

        self.token = ""
        self.username = ""
    
    def __init_ui(self):
        self.__user = StringVar()
        self.__pass = StringVar()

        self.__username_label = Label(self.__root, text = "Username: ", font = (14))
        self.__username_label.grid(row = 0, column = 0, padx = 4, pady = 4, sticky = E)
        self.__username_entry = Entry(self.__root, textvariable = self.__user, font = (14))
        self.__username_entry.grid(row = 0, column = 1)

        self.__password_label = Label(self.__root, text = "Password: ", font = (14))
        self.__password_label.grid(row = 1, column = 0, padx = 4, pady = 4, sticky = E)
        self.__password_entry = Entry(self.__root, textvariable = self.__pass, font = (14), show = "*")
        self.__password_entry.grid(row = 1, column = 1)

        self.__login_button = Button(self.__root, text = "Login", font = (14), width = 8, command = self.__login)
        self.__login_button.grid(row = 2, column = 1, sticky = W)
        self.__register_button = Button(self.__root, text = "Register", font = (14), width = 8, command = self.__register)
        self.__register_button.grid(row = 2, column = 1, sticky = E)
    
    def show(self):
        self.__root.mainloop()
    
    def __login(self):
        Logger.log("Trying to Login...")

        payload = {
            "username": self.__user.get(),
            "password": self.__pass.get()
        }

        Logger.log("Making POST request...")
        r =  None
        try:
            r = requests.post(url = Config.get_connection_string() + "/api/auth/login", json = payload)
        except requests.exceptions.RequestException:
            messagebox.showerror("Connection error", "Failed to connect with to server")
            return

        Logger.log(f"Recieved response: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            Logger.log("Login successful")
            self.token = data["token"]
            self.username = payload["username"]
            self.__exit()
        else:
            messagebox.showerror("Login error", "Invalid email or password")
    
    def __register(self):
        Logger.log("Opening RegisterWindow")
        RegisterWindow(self.__root)
    
    def __exit(self):
        self.__root.destroy()