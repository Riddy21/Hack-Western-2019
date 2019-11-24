import tkinter as tk
import time


class Window():
    def __init__(self):
        # Setup window
        self.window = tk.Tk()

        self.monthlyBudget = tk.StringVar()

        # Create list of Groups

        # Create list of recent transactions

        # Frames
        self.mainFrame = tk.Frame(self.window)
        self.groupsFrame = tk.Frame(self.window)
        self.membersFrame = tk.Frame(self.window)
        self.profileFrame = tk.Frame(self.window)
        self.friendsFrame = tk.Frame(self.window)
        self.holdFrame = tk.Frame(self.window)  # holder frame

        self.window.title("Test")
        self.window.geometry("500x500")
        self.window.resizable(1, 1)

        self.populateMain()
        self.populateFriends()
        self.populateGroups()
        self.populateMembers()
        self.populateProfile()

        self.switchFrame(self.mainFrame, self.holdFrame)
        (self.window).mainloop()

    def switchFrame(self, frame, prevFrame):
        prevFrame.pack_forget()
        frame.pack()

    def populateMain(self):
        self.monthlyBudget.set("500")
        tk.Label(self.mainFrame, text="Your Monthly Budget is:").pack()
        tk.Label(self.mainFrame, text=self.monthlyBudget.get()).pack()
        tk.Button(self.mainFrame, text="Add a Transaction", command=self.openTransactionWin).pack()

        profiles = tk.LabelFrame(self.mainFrame, text="Profiles and Groups", pady=5, padx=5)

        tk.Button(profiles, text="Your\nProfile",
                  command=lambda: self.switchFrame(self.profileFrame, self.mainFrame)).pack(side="left")
        tk.Button(profiles, text="Friends\n#",
                  command=lambda: self.switchFrame(self.friendsFrame, self.mainFrame)).pack(side="left")
        tk.Button(profiles, text="Groups\n#", command=lambda: self.switchFrame(self.groupsFrame, self.mainFrame)).pack(
            side="left")

        profiles.pack()

        recentTrans = tk.LabelFrame(self.mainFrame, text="Recent Transactions", pady=5, padx=5)

        tk.Label(recentTrans, text="Name", pady=10).grid(sticky="W", row=0, column=0)
        tk.Label(recentTrans, text="Date", pady=10).grid(sticky="W", row=0, column=1)
        tk.Label(recentTrans, text="Amount", pady=10).grid(sticky="W", row=0, column=2)

        # replace i with list of recent transactinos
        for i in range(10):
            tk.Label(recentTrans, text="Amazon").grid(sticky="W", row=i + 1, column=0)
            tk.Label(recentTrans, text="11/12/2019").grid(sticky="W", row=i + 1, column=1)
            tk.Label(recentTrans, text="$50").grid(sticky="W", row=i + 1, column=2)
            tk.Button(recentTrans, text="View", command=lambda: self.openViewTransactionWin(i)).grid(sticky="W",
                                                                                                     row=i + 1,
                                                                                                     column=3)  # change i into list of transactions

        recentTrans.pack()

    def openTransactionWin(self):
        transactionWin = tk.Tk()
        transactionWin.title("Add Transaction")
        transactionWin.geometry("300x600")
        transactionWin.resizable(0, 0)

        transType = tk.Frame(transactionWin)
        transType.pack()

        tk.Label(transType, text="What kind of transaction?").pack()
        tk.Button(transType, text="Personal", command=lambda: personal(transType, transactionWin)).pack(side="left")
        tk.Button(transType, text="Group", command=lambda: group(transType, transactionWin)).pack(side="left")
        tk.Button(transType, text="Friends", command=lambda: group(transType, transactionWin)).pack(side="left")

        def group(frame, window):
            frame.destroy()

            groupF = tk.Frame(window)
            expName = tk.StringVar(groupF)
            amount = tk.StringVar(groupF,value = "0")
            memberAmount = []


            groupF.pack()

            tk.Label(groupF, text="Expense Name").grid(row=0, column=0)
            tk.Label(groupF, text="Amount").grid(row=1, column=0)
            unEntry = tk.Entry(groupF, textvariable=expName)
            unEntry.grid(row=0, column=1)
            pwEntry = tk.Entry(groupF, textvariable=amount)
            pwEntry.grid(row=1, column=1)

            OPTIONS = [
                "Group 1",
                "Group 2",
                "Group 3",
                "Group 4"
            ]  # change to list of friends and groups

            default = tk.StringVar(groupF)
            default.set(OPTIONS[0])  # default value

            w = tk.OptionMenu(groupF, default, *OPTIONS)
            w.grid(row=2, column =0)
            tk.Button(groupF, text = "Split Evenly",command = lambda: update()).grid(row =2, column = 1)
            def update():
                for i in range(10):  # according to Group getMembers
                    memberAmount[i].set(str(round(float(amount.get())/10,2)))



            groupMembers = tk.LabelFrame(groupF)

            for i in range(10):  # according to Group getMembers
                memberName = tk.StringVar(groupF, value = "bob") #change to group Member get name
                memberAmount.append(tk.StringVar(groupF,value = str(round(float(amount.get())/10,2))))
                tk.Label(groupMembers, text = memberName.get()).grid(row=i, column=0)
                amEntry = tk.Entry(groupMembers, textvariable=memberAmount[i])
                amEntry.grid(row=i, column=1)

            groupMembers.grid(row = 3, columnspan = 2)

            addBut = tk.Button(groupF, text="Add", state = "normal", command =lambda: addExpense(groupF, amount,memberAmount)).grid(row=4, column=0) #add function creates expense in database, updates recent expenses and closes window
            tk.Button(groupF, text="Cancel", command = transactionWin.destroy).grid(row=4, column=1)

            def addExpense(groupF, amount, memberAmount):
                sum = 0
                for i in range(10):  # according to Group getMembers
                    sum += float(memberAmount[i].get())
                if round(sum,2) != round(float(amount.get()),2):
                    error = tk.Label(groupF, text="Amount does not add up to total")
                    error.grid(row=5, columnspan=2)
                    error.update()
                    time.sleep(1)
                    error.destroy()


                else:
                    #save amount for ea

        def personal(frame, window):
            frame.destroy()

            personalF = tk.Frame(window)
            expName = tk.StringVar()
            amount = tk.StringVar()

            personalF.pack()

            tk.Label(personalF, text="Expense Name").grid(row=0, column=0)
            tk.Label(personalF, text="Amount").grid(row=1, column=0)
            unEntry = tk.Entry(personalF, textvariable=expName)
            unEntry.grid(row=0, column=1)
            pwEntry = tk.Entry(personalF, textvariable=amount)
            pwEntry.grid(row=1, column=1)
            tk.Button(personalF, text="Add").grid(row=2,column=0)  # add function creates expense in database, updates recent expenses and closes window
            tk.Button(personalF, text="Cancel", command=transactionWin.destroy).grid(row=2, column=1)

        transactionWin.mainloop()

    def openViewTransactionWin(self, transaction):
        transactionViewWin = tk.Tk()
        transactionViewWin.title("View Transaction")
        transactionViewWin.geometry("300x200")
        transactionViewWin.resizable(0, 0)

        (transactionViewWin).mainloop()

    def addNewFriendWin(self):
        addfriendWin = tk.Tk()
        addfriendWin.title("Add Friend")
        addfriendWin.geometry("300x200")
        addfriendWin.resizable(0, 0)

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
