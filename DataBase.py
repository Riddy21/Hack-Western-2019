import pymongo
import random
import dns
from datetime import date

class DataBase:

    def __init__(self):
        self.client = pymongo.MongoClient(
            "mongodb+srv://DanielLu:HackTheHackTheHack@hackwesterndatabase-7vhqk.gcp.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.client.gettingStarted
        self.users = self.db.users
        self.debts = self.db.debts
        self.debtIDs = self.db.debtID
        self.groups = self.db.groups
        self.groupIDs = self.db.groupID
        self.transactions = self.db.transactions
        self.friendsList = self.db.friendsList
        self.test = self.db.TestingCollection


    ########################################################################################################################
    # DEBT
    # PURPOSE: Generates a uniqueID for the Debt
    def create_DebtID(self):
        UniqueID = False
        while (not UniqueID):
            debtID = random.randint(1, 999999999)
            DebtDict = self.debtIDs.find()[0]
            if str(debtID) not in DebtDict:
                DebtDict[str(debtID)] = 1
                self.debtIDs.replace_one({'Balance': 1000}, DebtDict)
                UniqueID = True
                return debtID


    # PURPOSE: Deletes a debt from debtID list
    def remove_DebtID(self,debtID):
        DebtDict = self.debtIDs.find()[0]
        del DebtDict[str(debtID)]
        self.debtIDs.replace_one({'Balance': 1000}, DebtDict)


    '''
    PURPOSE: Adds a debt between you and someone else.
    fields: debt (Dictionary) : Contains information for the created Debt. See DemoDebt for an example
    
    demoDebt = {
        "UserName": "DanielLu",
        "Target": "BobJoe",
        "Balance": 150,
        "Reason": "Pizza money",
        "Group": 6768044637,
        "Date": date.today().strftime("%d/%m/%Y"),
    }
    '''


    def add_Debt(self,debt):
        debt["DebtID"] = self.create_DebtID()
        self.debts.insert_one(debt)
        print("Debt Added")


    # PURPOSE: deletes a debt from debt list
    def remove_debt(self,debtID):
        self.remove_DebtID(debtID)
        self.debts.delete_one({"DebtID": debtID})


    # Turns debts into 2 transactions
    def pay_debt(self,debtID):
        debt = self.debts.find_one({"DebtID": debtID})
        transaction1 = {
            "Balance": debt["Balance"],
            "To/From": debt["Target"],
            "Reason": debt["Reason"],
            "DatePaid": date.today().strftime("%d/%m/%Y"),
            "UserName": debt["UserName"],
            "GroupID": debt["GroupID"]
        }

        transaction2 = {
            "Balance": -debt["Balance"],
            "To/From": debt["UserName"],
            "Reason": debt["Reason"],
            "DatePaid": date.today().strftime("%d/%m/%Y"),
            "UserName": debt["Target"],
            "GroupID": debt["GroupID"]
        }
        self.add_transaction(transaction1)
        self.add_transaction(transaction2)
        self.remove_debt(debtID)


    """
    PURPOSE: Returns debts of a user
    FIELDS: UserName : username of the debts that the user owes to people
    OUTPUT: Returns an iterable Collection of Dictionaries(Debts) that the user owes to people"""


    def get_debts(self,UserName):
        return self.debts.find({"UserName": UserName})


    """
    PURPOSE: Returns debts owed to a user
    FIELDS: UserName : username of the debts that are owed to the user
    OUTPUT: Returns an iterable Collection of Dictionaries(Debts) that people owe to the user"""


    def get_owes(self,UserName):
        return self.debts.find({"Target": UserName})


    ########################################################################################################################
    # TRANSACTIONS


    # Adds a transaction
    def add_transaction(self,transaction):
        transactionID = self.create_DebtID()
        transaction["TransactionID"] = transactionID
        self.transactions.insert_one(transaction)


    # Removes a transaction based on transactionID
    def remove_transaction(self,transactionID):
        self.transactions.delete_one({"TransactionID": transactionID})
        self.remove_DebtID(transactionID)


    """
    PURPOSE: Returns transactions relating a user
    FIELDS: UserName : username of user 
    OUTPUT: Returns an iterable Collection of Dictionaries(transactions) that the user has done"""


    def get_transactions(self,UserName):
        return self.transactions.find({"UserName": UserName})

    def get_recentTransactions(self):
        return self.transactions.find()

    ########################################################################################################################
    # USER SHIT

    # Adds users based on user object
    def add_user(self,user):
        for i in self.users.find():
            if i["UserName"] == user["UserName"]:
                return "That name is already taken"
        self.users.insert_one(user)
        self.createFriendsList(user["UserName"])


    # Removes User based on user userName and removes friends list
    def remove_user(self,UserName):
        self.users.delete_one({"UserName": UserName})
        self.friendsList.delete_one({"UserName": UserName})


    # finds specific user and returns it as a dictionary object
    def get_user(self,userName):
        return self.users.find_one({"UserName": userName})


    # sets budget for specific user
    def set_userBudget(self,userName, budget):
        user = self.users.find_one({"UserName": userName})
        user["Budget"] = budget
        self.users.replace_one({"UserName": userName})


    # adjusts budget for specific user
    def adjust_userBudget(self,userName, budget):
        user = self.users.find_one({"UserName": userName})
        user["Budget"] += budget
        self.users.replace_one({"UserName": userName},user)


    ########################################################################################################################
    # GROUP SHIT

    # Creates GroupIDs
    def create_groupID(self):
        UniqueID = False
        while (not UniqueID):
            groupID = random.randint(1, 999999999)
            groupDict = self.groupIDs.find()[0]
            if str(groupID) not in groupDict:
                groupDict[str(groupID)] = 1
                self.groupIDs.replace_one({'Balance': 1000}, groupDict)
                UniqueID = True
                return groupID


    # remove groupID from dictionary
    def remove_groupID(self,groupID):
        groupDict = self.groupIDs.find()[0]
        del groupDict[str(groupID)]
        self.groupIDs.replace_one({'Balance': 1000}, groupDict)


    # Creates group based on group object
    def create_group(self,group):
        group["GroupID"] = self.create_groupID()
        self.groups.insert_one(group)


    # removesGroup with corersponding groupID
    def remove_group(self,groupID):
        self.groups.delete_one({"GroupID": groupID})
        self.remove_groupID(groupID)


    # Adds user with userName to group with groupID
    def add_toGroup(self,userName, groupID):
        group = self.groups.find_one({"GroupID": groupID})
        group["Users"] += [userName]
        self.groups.replace_one({"GroupID": groupID}, group)


    # removes from user with userName from group with groupID
    def remove_fromGroup(self,userName, groupID):
        group = self.groups.find_one({"GroupID": groupID})
        group["Users"].remove(userName)
        self.groups.replace_one({"GroupID": groupID}, group)


    # finds all groups that has member username, returns array of all groups member is in(Groups are in dictionary)
    def find_groups(self,userName):
        group = self.groups.find()
        listOfGroups = []
        for i in group:
            if userName in i["Users"]:
                print("Found users")
                listOfGroups += [i]
        return listOfGroups


    # Gets specific group based on groupID
    def get_group(self,groupID):
        group = self.groups.find_one({"GroupID": groupID})
        return group


    # Adds budgetChange to budget of the group
    def adjust_groupBudget(self,groupID, budgetChange):
        group = self.groups.find_one({"GroupID": groupID})
        group["Budget"] += budgetChange
        self.groups.replace_one({"GroupID": groupID}, group)


    # returns interable collection of transactions(dictionary) that contain groupID
    def get_groupTransactions(self,groupID):
        return self.transactions.find({"groupID": groupID})


    ########################################################################################################################
    # Friends List garbage

    # takes owners username
    def createFriendsList(self,userName):
        friendList = {
            "Owner": userName,
            "Friends": []
        }
        self.friendsList.insert_one(friendList)


    # Gets List of friends from user
    def getFriendsList(self,userName):
        return self.friendsList.find_one({"Owner": userName})["Friends"]


    # Adds two friends to each other's friends list <3
    def addFriend(self,userName, targetFriend):
        friendList = self.friendsList.find_one({"Owner": userName})
        friendList2 = self.friendsList.find_one({"Owner": targetFriend})
        friendList["Friends"] += [targetFriend]
        friendList2["Friends"] += [userName]
        self.friendsList.replace_one({"Owner": userName}, friendList)
        self.friendsList.replace_one({"Owner": targetFriend}, friendList2)


    # removes friends from eachother friends list </3
    def removeFriend(self,userName, targetFriend):
        friendList = self.friendsList.find_one({"Owner": userName})
        friendList2 = self.friendsList.find_one({"Owner": targetFriend})
        friendList["Friends"].remove(targetFriend)
        friendList2["Friends"].remove(userName)
        self.friendsList.replace_one({"Owner": userName}, friendList)
        self.friendsList.replace_one({"Owner": targetFriend}, friendList2)


    ########################################################################################################################
    """
    demoDebt = {
        "UserName": "DanielLu",
        "Target": "BobJoe",
        "Balance": 150,
        "Reason": "Pizza money",
        "GroupID": 6768044637,
        "Date": date.today().strftime("%d/%m/%Y"),
        "Category":
    }

    demoUser = {
        "name": {"first": "John", "last": "Joe"},
        "UserName": "Johnny12",
        "password": "123123123abc",
        "Budget": 600  # monthly budget, resets at start of every month
    }

    demoGroup = {
        "GroupName": "SuperCoolGroup",
        "Users": ["DanielLu", "BobJoe", "Tom"],
        "GroupBudget": 500,
    }

    demoTransaction = {
        "Balance": -10,
        "To/From": "Tom",
        "Reason": "McDonalds",
        "Date": date.today().strftime("%d/%m/%Y"),
        "UserName": "DanielLu",
        "GroupID": 0,  # 0 signifies that there is no group attached to the transaction
        "Category": 
    }

    demoGroup = {
        "GroupName": "Cool Kids Club",
        "Users": ["DanielLu", "BobJoe", "Tomothy"],
        "Budget": 2000
    }"""
