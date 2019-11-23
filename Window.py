import tkinter as tk


class Window():
    def __init__(self):
        # Setup window
        self.window = tk.Tk()

        self.monthlyBudget = tk.StringVar()

        #Groups


        #Frames
        self.mainFrame = tk.Frame(self.window)
        self.transactionFrame = tk.Frame(self.window)
        self.groupsFrame = tk.Frame(self.window)
        self.membersFrame = tk.Frame(self.window)
        self.profileFrame = tk.Frame(self.window)
        self.holdFrame = tk.Frame(self.window) # holder frame

        self.window.title("Test")
        self.window.geometry("500x800")
        self.window.resizable(1, 1)

        self.populateMain()
        self.populateTransaction()
        self.populateGroups()
        self.populateMembers()
        self.populateProfile()

        self.switchFrame(self.mainFrame,self.holdFrame)
        (self.window).mainloop()

    def switchFrame(self, frame, prevFrame):
        prevFrame.pack_forget()
        frame.pack()

    def populateMain(self):
        self.monthlyBudget.set("500")
        tk.Label(self.mainFrame, text = "Your Monthly Budget is:").pack()
        tk.Label(self.mainFrame, text = self.monthlyBudget.get()).pack()
        tk.Button(self.mainFrame,text = "Add a Transaction",command = lambda: self.switchFrame(self.transactionFrame,self.mainFrame)).pack()
        profiles = tk.Frame(self.mainFrame).pack()

        tk.Button(profiles, text = "Your\nProfile").pack(side = "left")
        tk.Button(profiles, text = "Group").pack(side = "left")



    def populateTransaction(self):
        tk.Label(self.transactionFrame,text = "2").pack()
        tk.Button(self.transactionFrame,text = "bop",command = lambda: self.switchFrame(self.mainFrame,self.transactionFrame)).pack()

    def populateGroups(self):
        tk.Label(self.groupsFrame, text="empty").pack()

    def populateMembers(self):
        tk.Label(self.membersFrame, text="empty").pack()

    def populateProfile(self):
        tk.Label(self.profileFrame, text="empty").pack()
