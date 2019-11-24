import tkinter as tk
import Window
import DataBase as mdb

class Login():
    def __init__(self):
        # Setup window
        self.dbInterface = mdb.DataBase()
        self.window = tk.Tk()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.loginFrame = tk.Frame(self.window)

        self.window.title("Test")
        self.window.geometry("300x150")
        self.window.resizable(0, 0)


        self.populate()
        (self.window).mainloop()

    def populate(self):
        self.loginFrame.pack()
        tk.Label(self.loginFrame,text = "Username").grid(row = 0, column = 0)
        tk.Label(self.loginFrame,text = "Password").grid(row = 1, column = 0)
        unEntry = tk.Entry(self.loginFrame, textvariable = self.username)
        unEntry.grid(row = 0, column = 1)
        pwEntry = tk.Entry(self.loginFrame, textvariable=self.password)
        pwEntry.grid(row = 1, column = 1)
        tk.Button(self.loginFrame,text = "Login", command = self.Login).grid(row = 2, column = 0)
        tk.Button(self.loginFrame,text = "Register").grid(row = 2, column = 1)
    def Login(self):
        user = self.dbInterface.get_user(self.username.get())
        if (not user):
            raise("User is not regestered")
        else:
            if user["password"] != self.password.get():
                raise("password is wrong")
            else:
                self.window.destroy()
                print(self.username.get())
                print(self.password.get())
                Window.Window()

