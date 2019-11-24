import tkinter as tk
import time
from datetime import date
import DataBase as mdb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)

class Window():
    def __init__(self,butt):
        self.userName = butt

        # Setup window
        self.dbInterface = mdb.DataBase()
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

    def updateAllFrames(self):
        self.mainFrame.destroy()
        self.groupsFrame.destroy()
        self.membersFrame.destroy()
        self.profileFrame.destroy()
        self.friendsFrame.destroy()

        self.mainFrame = tk.Frame(self.window)
        self.groupsFrame = tk.Frame(self.window)
        self.membersFrame = tk.Frame(self.window)
        self.profileFrame = tk.Frame(self.window)
        self.friendsFrame = tk.Frame(self.window)

        self.populateMain()
        self.populateFriends()
        self.populateGroups()
        self.populateMembers()
        self.populateProfile()

        self.switchFrame(self.mainFrame, self.holdFrame)

    def switchFrame(self, frame, prevFrame):
        prevFrame.pack_forget()
        frame.pack()

    def populateMain(self):

        self.monthlyBudget.set(self.dbInterface.get_user(self.userName)["Budget"])
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

        #TODO
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
        tk.Button(transType, text="Friends", command=lambda: friends(transType, transactionWin)).pack(side="left")

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
            CATEGORIES = [
                "Bills",
                "Housing",
                "Transportation",
                "Gifts",
                "Groceries",
                "Entertainment"
            ]
            OPTIONS = [
                "Group 1",
                "Group 2",
                "Group 3",
                "Group 4"
            ]  # change to list of friends and groups

            default = tk.StringVar(groupF)
            default.set(OPTIONS[0])  # default value

            defaultCat = tk.StringVar(groupF)
            defaultCat.set(CATEGORIES[0])

            x = tk.OptionMenu(groupF,defaultCat,*CATEGORIES)
            x.grid(row = 3, column = 1)
            tk.Label(groupF,text = "Categories").grid(row = 3,column = 0)
            tk.Label(groupF,text = "Groups").grid(row=4,column = 0)
            w = tk.OptionMenu(groupF, default, *OPTIONS)
            w.grid(row=4, column =1)
            tk.Button(groupF, text = "Split Evenly",command = lambda: update()).grid(row =4, column = 2)
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

            groupMembers.grid(row = 5, columnspan = 3)

            tk.Button(groupF, text="Add", state = "normal", command =lambda: addExpense(groupF, amount,memberAmount)).grid(row=6, column=0) #add function creates expense in database, updates recent expenses and closes window
            tk.Button(groupF, text="Cancel", command = transactionWin.destroy).grid(row=6, column=1)

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
                    #save amount for each person
                    #TODO
                    self.dbInterface.add_transaction()
                    transactionWin.destroy()

        def friends(frame, window):
            frame.destroy()

            friendF = tk.Frame(window)
            expName = tk.StringVar(friendF)
            amount = tk.StringVar(friendF,value = "0")
            global memberAmount
            memberAmount= []
            members = []
            
            friendF.pack()

            tk.Label(friendF, text="Expense Name").grid(row=0, column=0)
            tk.Label(friendF, text="Amount").grid(row=1, column=0)
            unEntry = tk.Entry(friendF, textvariable=expName)
            unEntry.grid(row=0, column=1)
            pwEntry = tk.Entry(friendF, textvariable=amount)
            pwEntry.grid(row=1, column=1)

            CATEGORIES = [
                "Bills",
                "Housing",
                "Transportation",
                "Gifts",
                "Groceries",
                "Entertainment"
            ]
            OPTIONS = self.dbInterface.getFriendsList(self.userName)  # change to list of friends and groups
            OPTIONS.insert(0,self.userName)

            friendChoose = tk.StringVar(friendF)
            friendChoose.set(OPTIONS[0])  # default value

            category = tk.StringVar(friendF)
            category.set(CATEGORIES[0])

            x = tk.OptionMenu(friendF, category, *CATEGORIES)
            x.grid(row=2, column = 1)
            w = tk.OptionMenu(friendF, friendChoose, *OPTIONS)
            w.grid(row=2, column=0)
            tk.Button(friendF, text = "Add Friend",command = lambda: addFriendtoList()).grid(row =3, column = 0)
            tk.Button(friendF, text = "Split Evenly",command = lambda: update()).grid(row =3, column = 1)
            def update():
                for i in range(len(members)):  # according to Group getMembers
                    memberAmount[i].set(str(round(float(amount.get())/len(members),2)))

            def addFriendtoList():
                if (friendChoose.get() in members) == False:
                    members.append(friendChoose.get())
                    global memberAmount
                    memberAmount = []
                    print(len(members))
                    for i in range(len(members)):  # according to Group getMembers
                        memberName = tk.StringVar(friendF, value=members[i])  # change to group Member get name
                        memberAmount.append(
                            tk.StringVar(friendF, value=str(round(float(amount.get()) / len(members), 2))))
                        tk.Label(groupMembers, text=memberName.get()).grid(row=i, column=0)
                        amEntry = tk.Entry(groupMembers, textvariable=memberAmount[i])
                        amEntry.grid(row=i, column=1)

            groupMembers = tk.LabelFrame(friendF)
            groupMembers.grid(row = 4, columnspan = 2)

            tk.Button(friendF, text="Add", state = "normal", command =lambda: addExpense(friendF, amount,memberAmount,members)).grid(row=5, column=0) #add function creates expense in database, updates recent expenses and closes window
            tk.Button(friendF, text="Cancel", command = transactionWin.destroy).grid(row=5, column=1)

            def addExpense(friendF, amount, memberAmount, members):
                sum = 0
                print(memberAmount)
                print(members)

                for i in memberAmount:  # according to Group getMembers
                    sum += float(i.get())

                if round(sum,2) != round(float(amount.get()),2):
                    error = tk.Label(friendF, text="Amount does not add up to total")
                    error.grid(row=6, columnspan=2)
                    error.update()
                    time.sleep(1)
                    error.destroy()

                else:
                    start3 = 0
                    Transaction = {
                        "Balance": sum,
                        "To/From": "",
                        "Reason": expName.get(),
                        "Date": date.today().strftime("%d/%m/%Y"),
                        "UserName": self.userName,
                        "GroupID": 0,
                        "Category": category.get()
                    }
                    self.dbInterface.add_transaction(Transaction)
                    self.dbInterface.adjust_userBudget(self.userName,-sum)


                    if members[0] == self.userName:
                        start3 = 1
                    for i in range(start3,len(members)):
                        Debt = {
                            "UserName": members[i],
                            "Target": self.userName,
                            "Balance": int(float(memberAmount[i].get())),
                            "Reason": expName.get(),
                            "GroupID": 0,
                            "Date": date.today().strftime("%d/%m/%Y"),
                            "Category": category.get()
                        }
                        self.dbInterface.add_Debt(Debt)
                        self.dbInterface.adjust_userBudget(members[i],-int(float(memberAmount[i].get())))
                    self.updateAllFrames()
                    transactionWin.destroy()

        def personal(frame, window):
            frame.destroy()

            personalF = tk.Frame(window)
            expName = tk.StringVar(personalF)
            amount = tk.StringVar(personalF, value = "0")

            personalF.pack()

            tk.Label(personalF, text="Expense Name").grid(row=0, column=0)
            tk.Label(personalF, text="Amount").grid(row=1, column=0)
            unEntry = tk.Entry(personalF, textvariable=expName)
            unEntry.grid(row=0, column=1)
            pwEntry = tk.Entry(personalF, textvariable=amount)
            pwEntry.grid(row=1, column=1)

            CATEGORIES = [
                "Bills",
                "Housing",
                "Transportation",
                "Gifts",
                "Groceries",
                "Entertainment"
            ]
            category = tk.StringVar(personalF)
            category.set(CATEGORIES[0])
            tk.Label(personalF,text="Category").grid(row=2,column = 0)
            x = tk.OptionMenu(personalF, category, *CATEGORIES)
            x.grid(row=2, column=1)
            tk.Button(personalF, text="Add",command = lambda:addExpense(amount)).grid(row=3,column=0)  # add function creates expense in database, updates recent expenses and closes window
            tk.Button(personalF, text="Cancel", command=transactionWin.destroy).grid(row=3, column=1)

            def addExpense(amount):
                Transaction = {
                    "Balance": (round(float(amount.get()), 2)),
                    "To/From": self.userName,
                    "Reason": expName.get(),
                    "Date": date.today().strftime("%d/%m/%Y"),
                    "UserName": self.userName,
                    "GroupID":0,
                    "Category": category.get()
                }
                self.dbInterface.add_transaction(Transaction)
                self.dbInterface.adjust_userBudget(self.userName,-(round(float(amount.get()), 2)))
                self.updateAllFrames()
                transactionWin.destroy()


        transactionWin.mainloop()

    def openViewTransactionWin(self, transaction):
        transactionViewWin = tk.Tk()
        transactionViewWin.title("View Transaction")
        transactionViewWin.geometry("300x200")
        transactionViewWin.resizable(0, 0)

        (transactionViewWin).mainloop()

    def addNewFriendWin(self,frame):
        addfriendWin = tk.Tk()
        addfriendWin.title("Add Friend")
        addfriendWin.geometry("300x200")
        addfriendWin.resizable(0, 0)

        friendName= tk.StringVar(addfriendWin)

        NewFriend = tk.Frame(addfriendWin)
        NewFriend.pack()
        tk.Label(NewFriend, text="Name: ").grid(row=0, column=0)
        tk.Entry(NewFriend, textvariable = friendName).grid(row=0, column=1)
        buttonFriend = tk.Button(NewFriend, text="Add Friend",command = lambda: add(addfriendWin, friendName),state = "disabled")
        buttonFriend.grid(row=4, column=0)

        tk.Button(NewFriend, text="Cancel",command = lambda: cancel(addfriendWin)).grid(row=4, column=2)
        tk.Button(NewFriend, text="Search Friend", command = lambda: searchFriend(NewFriend,buttonFriend,friendName)).grid(row=1, column=1)
        
        def cancel(window):
            window.destroy()

        def add(window,friendName):
            listOfFriends = self.dbInterface.getFriendsList(self.userName)
            for i in range(len(listOfFriends)):
                DebtsToYou = self.dbInterface.get_owes(self.userName)
                Sum = 0
                for j in DebtsToYou:
                    if j["UserName"] == listOfFriends[i]:
                        Sum += j["Balance"]

            self.dbInterface.addFriend(self.userName,friendName.get())
            window.destroy()
            Friend = tk.LabelFrame(frame,padx=5 ,pady=10)
            tk.Label(Friend, text=friendName.get(), pady=10).grid(sticky="W", row=1, column=0) # change i to $ and actual friends
            tk.Label(Friend, text="$ " + str(Sum), pady=10).grid(sticky="W", row=1, column=1)
            Friend.pack()

        def searchFriend(frame, button,name):
            #if not name: return
            friend = self.dbInterface.get_user(name.get())
            if friend:
                if friend["UserName"] in self.dbInterface.getFriendsList(self.userName):
                    tk.Label(frame, text="Already Friends!").grid(row=2, column=1)
                    button.config(state="disabled")
                else:
                    tk.Label(frame, text="Friend Found!!!!").grid(row=2, column=1)
                    button.config(state="normal")
            else:
                tk.Label(frame, text="Friend not found").grid(row=2, column=1)
                button.config(state="disabled")

        addfriendWin.mainloop()

    def addNewGroupWin(self):
        addGroupWin = tk.Tk()
        addGroupWin.title("Add Group")
        addGroupWin.geometry("300x400")
        addGroupWin.resizable(0, 0)

        NewGroup = tk.Frame(addGroupWin)
        NewGroup.pack()

        OPTIONS = self.dbInterface.getFriendsList(self.userName)  # change to list of friends and groups
        OPTIONS.insert(0, self.userName)
        groupName = tk.StringVar(NewGroup)
        groupFriend = tk.StringVar(NewGroup, value = OPTIONS[0])
        groupMembers = []

        tk.Label(NewGroup, text="Group Name: ").grid(row=0, column=0)
        tk.Entry(NewGroup, textvariable=groupName).grid(row=0, column=1)

        w = tk.OptionMenu(NewGroup, groupFriend, *OPTIONS)
        w.grid(row=1, column=0)
        tk.Button(NewGroup, text="Add Friend", command=lambda: addFriendtoList()).grid(row=1, column=1)

        def addFriendtoList():
            if (groupFriend.get() in groupMembers) == False:
                groupMembers.append(groupFriend.get())
                for i in range(len(groupMembers)):  # according to Group getMembers
                    allFriends = tk.LabelFrame(NewGroup, padx=5, pady=10)
                    tk.Label(allFriends, text=groupMembers[i], padx = 10).pack()
                    allFriends.grid(row=3+i, columnspan = 3)
        tk.Button(NewGroup, text="Create Group", command = lambda: createGroup()).grid(row=2, columnspan = 2)

        def createGroup():
            #TODO: create a group using specified parameters and pass in nessesary variables
            addGroupWin.destroy()


        addGroupWin.mainloop()

    def populateFriends(self):
        NavBar = tk.LabelFrame(self.friendsFrame, pady=5, padx=5)
        tk.Button(NavBar, text="Friends",relief = "sunken",state = "disabled").pack(side = "left")
        tk.Button(NavBar, text="Groups",state = "normal",command=lambda: self.switchFrame(self.groupsFrame,self.friendsFrame)).pack(side = "left")
        NavBar.pack()

        allFriends = tk.LabelFrame(self.friendsFrame, pady=5, padx=5)

        tk.Button(self.friendsFrame, text="+",state = "normal",command=lambda: self.addNewFriendWin(allFriends)).pack()
        tk.Button(self.friendsFrame, text="Back",state = "normal",command=lambda: self.switchFrame(self.mainFrame,self.friendsFrame)).pack(side="bottom")

       #TODO replace friends list here

        listOfFriends = self.dbInterface.getFriendsList(self.userName)
        for i in range(len(listOfFriends)):
            DebtsToYou = self.dbInterface.get_owes(self.userName)
            Sum = 0
            for j in DebtsToYou:
                if j["UserName"] == listOfFriends[i]:
                    Sum += j["Balance"]

            Friend = tk.LabelFrame(allFriends,padx=5 ,pady=10)
            tk.Label(Friend, text="Friend Name: " + listOfFriends[i], pady=10).grid(sticky="W", row=i + 1, column=0) # change i to $ and actual friends
            tk.Label(Friend, text="$ " + str(Sum), pady=10).grid(sticky="W", row=i + 1, column=1)
            Friend.pack()
        allFriends.pack()

    def populateGroups(self):
        NavBar = tk.LabelFrame(self.groupsFrame, pady=5, padx=5)
        tk.Button(NavBar, text="Friends",state = "normal",command=lambda: self.switchFrame(self.friendsFrame,self.groupsFrame)).pack(side = "left")
        tk.Button(NavBar, text="Groups",relief = "sunken",state = "disabled").pack(side = "left")
        NavBar.pack()

        tk.Button(self.groupsFrame, text="+",state = "normal",command=lambda: self.addNewGroupWin()).pack()
        tk.Button(self.groupsFrame, text="Back",state = "normal",command=lambda: self.switchFrame(self.mainFrame,self.groupsFrame)).pack(side="bottom")

        allGroups = tk.LabelFrame(self.groupsFrame, pady=5, padx=5)
        # replace i with list of recent transactinos
        for i in range(3):
            GroupFr = tk.LabelFrame(allGroups,padx=5)
            
            tk.Label(GroupFr, text="Group Name: " + str(i), pady=10).grid(sticky="W", row=0, column=0) # change i to $ and actual groups
            tk.Button(GroupFr, text="Details",state = "normal",command=lambda: self.switchFrame(self.membersFrame,self.groupsFrame)).grid(sticky="W", row=0, column=2)
            Group = tk.LabelFrame(GroupFr,padx=5)
            tk.Label(Group, text="$" + str(i), pady=10).grid(sticky="W", row=i + 1, column=0,padx=(0,25))
            for j in range(3):
                tk.Label(Group, text="M" + str(j), pady=10).grid(sticky="W", row=i+1, column=j+1)
            Group.grid(sticky="W", row=i + 2, column=0)
            GroupFr.pack()
        allGroups.pack()

    def populateMembers(self):
        tk.Label(self.membersFrame, text="Group Budget: $232.34").pack() #mocking members up
        youFr = tk.LabelFrame(self.membersFrame,pady = 5,padx=5)
        youFr.pack()
        tk.Label(youFr, text="You").grid(row = 1, column = 0, padx=(0,25))
        tk.Label(youFr, text="Amount Owed").grid(row = 0, column = 2)
        tk.Label(youFr, text="$90.99").grid(row = 1, column = 2)

        memFr = tk.LabelFrame(self.membersFrame,pady = 15,padx=5)
        memFr.pack()

        for i in range(3):
            MemberFr = tk.LabelFrame(memFr,pady = 5,padx=5)
            MemberFr.pack()
            tk.Label(MemberFr, text="M" + str(i)).grid(row = 1, column = 0, padx=(0,25))
            tk.Label(MemberFr, text="Amount Owed").grid(row = 0, column = 2)
            tk.Label(MemberFr, text="$30.33").grid(row = 1, column = 2)
        
        tk.Button(self.membersFrame, text="Back",state = "normal",command=lambda: self.switchFrame(self.groupsFrame,self.membersFrame)).pack(side="bottom")

    def populateProfile(self):
        labels = 'Groceries', 'Bills', 'Gifts', 'Housing'
        sizes = [15, 30, 45, 10]
        data = {"N18": 10, "N19": 15, "N20": 5, "N21": 20, "N22": 66, "N23": 100, "N21": 24}
        dates = list(data.keys())
        expenses = list(data.values())

        fig, axs = plt.subplots(figsize=(2, 2))
        axs.bar(dates, expenses)
        fig.suptitle('Daily Spending')

        fig1, axs1 = plt.subplots(figsize=(2, 2))
        axs1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
        axs1.axis('equal')
        fig1.suptitle('Category')

        canvas = FigureCanvasTkAgg(fig, master=self.profileFrame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().grid(row = 0,column = 0)
        canvas1 = FigureCanvasTkAgg(fig1, master=self.profileFrame)  # A tk.DrawingArea.
        canvas1.draw()
        canvas1.get_tk_widget().grid(row = 0,column = 1)
        tk.Button(self.profileFrame, text="Back", command = lambda: self.switchFrame(self.mainFrame,self.profileFrame)).grid(row=1, columnspan = 2)