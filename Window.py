import tkinter as tk


class Window():
    def __init__(self):
        # Setup window
        self.window = tk.Tk()

        self.monthlyBudget = tk.StringVar()

        #Create list of Groups

        #Create list of recent transactions


        #Frames
        self.mainFrame = tk.Frame(self.window)
        self.groupsFrame = tk.Frame(self.window)
        self.membersFrame = tk.Frame(self.window)
        self.profileFrame = tk.Frame(self.window)
        self.friendsFrame = tk.Frame(self.window)
        self.holdFrame = tk.Frame(self.window) # holder frame

        self.window.title("Test")
        self.window.geometry("500x500")
        self.window.resizable(1, 1)

        self.populateMain()
        self.populateFriends()
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
        tk.Button(self.mainFrame,text = "Add a Transaction",command = self.openTransactionWin).pack()

        profiles = tk.LabelFrame(self.mainFrame, text = "Profiles and Groups",pady = 5, padx = 5 )

        tk.Button(profiles, text="Your\nProfile",command = lambda: self.switchFrame(self.profileFrame,self.mainFrame)).pack(side="left")
        tk.Button(profiles, text = "Friends\n#",command = lambda: self.switchFrame(self.friendsFrame,self.mainFrame)).pack(side = "left")
        tk.Button(profiles, text="Groups\n#",command = lambda: self.switchFrame(self.groupsFrame,self.mainFrame)).pack(side="left")

        profiles.pack()

        recentTrans = tk.LabelFrame(self.mainFrame, text = "Recent Transactions",pady = 5, padx = 5 )

        tk.Label(recentTrans, text="Name",pady = 10).grid(sticky = "W", row = 0, column = 0)
        tk.Label(recentTrans, text="Date",pady = 10).grid(sticky = "W",row=0, column=1)
        tk.Label(recentTrans, text="Amount",pady = 10).grid(sticky = "W",row=0, column=2)

        #replace i with list of recent transactinos
        for i in range(10):
            tk.Label(recentTrans, text="Amazon").grid(sticky = "W",row = i+1, column = 0)
            tk.Label(recentTrans, text="11/12/2019").grid(sticky = "W",row = i+1, column = 1)
            tk.Label(recentTrans, text="$50").grid(sticky = "W",row = i+1, column = 2)
            tk.Button(recentTrans, text = "View", command = lambda: self.openViewTransactionWin(i)).grid(sticky = "W",row = i+1, column = 3) # change i into list of transactions

        recentTrans.pack()


    def openTransactionWin(self):
        transactionWin = tk.Tk()
        transactionWin.title("Add Transaction")
        transactionWin.geometry("300x200")
        transactionWin.resizable(0, 0)

        (transactionWin).mainloop()
    def openViewTransactionWin(self,transaction):
        transactionViewWin = tk.Tk()
        transactionViewWin.title("View Transaction")
        transactionViewWin.geometry("300x200")
        transactionViewWin.resizable(0, 0)

        (transactionViewWin).mainloop()
    def addNewFriendWin(self):
        addfriendWin = tk.Tk()
        addfriendWin.title("Add Friend")
        addfriendWin.geometry("300x200")
        addfriendWin.resizable(0,0)

        addfriendWin.mainloop()

    def addNewGroupWin(self):
        addGroupWin = tk.Tk()
        addGroupWin.title("Add Friend")
        addGroupWin.geometry("300x200")
        addGroupWin.resizable(0, 0)

        addGroupWin.mainloop()
    def populateFriends(self):
        tk.Label(self.friendsFrame, text="empty").pack()

    def populateGroups(self):
        tk.Label(self.groupsFrame, text="empty").pack()

    def populateMembers(self):
        tk.Label(self.membersFrame, text="empty").pack()

    def populateProfile(self):
        tk.Label(self.profileFrame, text="empty").pack()
