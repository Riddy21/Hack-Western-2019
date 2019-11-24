import pymongo
import random
import dns
from datetime import date

########################################################################################################################

client = pymongo.MongoClient(
    "mongodb+srv://DanielLu:HackTheHackTheHack@hackwesterndatabase-7vhqk.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.gettingStarted
users = db.users
debts = db.debts
debtIDs = db.debtID
groups = db.groups
groupIDs = db.groupID
transactions = db.transactions
friendsList = db.friendsList
test = db.TestingCollection


########################################################################################################################
#DEBT
# PURPOSE: Generates a uniqueID for the Debt
def create_DebtID():
    UniqueID = False
    while (not UniqueID):
        debtID = random.randint(1, 999999999)
        DebtDict = debtIDs.find()[0]
        if str(debtID) not in DebtDict:
            DebtDict[str(debtID)] = 1
            debtIDs.replace_one({'Balance': 1000}, DebtDict)
            UniqueID = True
            return debtID


# PURPOSE: Deletes a debt from debtID list
def remove_DebtID(debtID):
    DebtDict = debtIDs.find()[0]
    del DebtDict[str(debtID)]
    debtIDs.replace_one({'Balance': 1000}, DebtDict)


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
def add_Debt(debt):
    debt["DebtID"] = create_DebtID()
    debts.insert_one(debt)
    print("Debt Added")


# PURPOSE: deletes a debt from debt list
def remove_debt(debtID):
    remove_DebtID(debtID)
    debts.delete_one({"DebtID": debtID})

#Turns debts into 2 transactions
def pay_debt(debtID):
    debt = debts.find_one({"DebtID":debtID})
    transaction1 = {
        "Balance" : debt["Balance"],
        "To/From" : debt["Target"],
        "Reason" : debt["Reason"],
        "DatePaid": date.today().strftime("%d/%m/%Y"),
        "UserName" : debt["UserName"],
        "GroupID": debt["GroupID"]
    }

    transaction2 = {
        "Balance" : -debt["Balance"],
        "To/From" : debt["UserName"],
        "Reason" : debt["Reason"],
        "DatePaid": date.today().strftime("%d/%m/%Y"),
        "UserName" : debt["Target"],
        "GroupID": debt["GroupID"]
    }
    add_transaction(transaction1)
    add_transaction(transaction2)
    remove_debt(debtID)

"""
PURPOSE: Returns debts of a user
FIELDS: UserName : username of the debts that the user owes to people
OUTPUT: Returns an iterable Collection of Dictionaries(Debts) that the user owes to people"""
def get_debts(UserName):
    return debts.find({"UserName": UserName})

"""
PURPOSE: Returns debts owed to a user
FIELDS: UserName : username of the debts that are owed to the user
OUTPUT: Returns an iterable Collection of Dictionaries(Debts) that people owe to the user"""
def get_owes(UserName):
    return debts.find({"Target": UserName})

########################################################################################################################
#TRANSACTIONS


# Adds a transaction
def add_transaction(transaction):
    transactionID = create_DebtID()
    transaction["TransactionID"] = transactionID
    transactions.insert_one(transaction)

#Removes a transaction based on transactionID
def remove_transaction(transactionID):
    transactions.removeOne({"TransactionID": transactionID})
    remove_DebtID(transactionID)

"""
PURPOSE: Returns transactions relating a user
FIELDS: UserName : username of user 
OUTPUT: Returns an iterable Collection of Dictionaries(transactions) that the user has done"""
def get_transactions(UserName):
    return transactions.find({"UserName": UserName})

########################################################################################################################
# USER SHIT

#Adds users based on user object
def add_user(user):
    for i in users.find():
        if i["UserName"] == user["UserName"]:
            return "That name is already taken"
    users.insert_one(user)
    createFriendsList(user["UserName"])

#Removes User based on user userName and removes friends list
def remove_user(UserName):
    users.delete_one({"UserName" : UserName})
    friendsList.delete_one({"UserName": UserName})

#finds specific user and returns it as a dictionary object
def get_user(userName):
    return users.find_one({"UserName": userName})

#sets budget for specific user
def set_userBudget(userName,budget):
    user = users.find_one({"UserName": userName})
    user["Budget"] = budget
    users.replace_one({"UserName": userName})

#adjusts budget for specific user
def adjust_userBudget(userName,budget):
    user = users.find_one({"UserName": userName})
    user["Budget"] += budget
    users.replace_one({"UserName": userName})

########################################################################################################################
# GROUP SHIT

# Creates GroupIDs
def create_groupID():
    UniqueID = False
    while (not UniqueID):
        groupID = random.randint(1, 999999999)
        groupDict = groupIDs.find()[0]
        if str(groupID) not in groupDict:
            groupDict[str(groupID)] = 1
            groupIDs.replace_one({'Balance': 1000}, groupDict)
            UniqueID = True
            return groupID

#remove groupID from dictionary
def remove_groupID(groupID):
    groupDict = groupIDs.find()[0]
    del groupDict[str(groupID)]
    groupIDs.replace_one({'Balance': 1000}, groupDict)

#Creates group based on group object
def create_group(group):
    group["GroupID"] = create_groupID()
    groups.insert_one(group)

#removesGroup with corersponding groupID
def remove_group(groupID):
    groups.delete_one({"GroupID":groupID})
    remove_groupID(groupID)

#Adds user with userName to group with groupID
def add_toGroup(userName,groupID):
    group = groups.find_one({"GroupID":groupID})
    group["Users"] += [userName]
    groups.replace_one({"GroupID":groupID},group)

#removes from user with userName from group with groupID
def remove_fromGroup(userName,groupID):
    group = groups.find_one({"GroupID":groupID})
    group["Users"].remove(userName)
    groups.replace_one({"GroupID": groupID}, group)

#finds all groups that has member username, returns array of all groups member is in(Groups are in dictionary)
def find_groups(userName):
    group = groups.find()
    listOfGroups = []
    for i in group:
        if userName in i["Users"]:
            print("Found users")
            listOfGroups +=[i]
    return listOfGroups

#Gets specific group based on groupID
def get_group(groupID):
    group = groups.find_one({"GroupID": groupID})
    return group

#Adds budgetChange to budget of the group
def adjust_groupBudget(groupID,budgetChange):
    group = groups.find_one({"GroupID": groupID})
    group["Budget"] += budgetChange
    groups.replace_one({"GroupID": groupID}, group)

#returns interable collection of transactions(dictionary) that contain groupID
def get_groupTransactions(groupID):
    return transactions.find({"groupID": groupID})

########################################################################################################################
# Friends List garbage

#takes owners username
def createFriendsList(userName):
    friendList = {
        "Owner": userName,
        "Friends":[]
    }
    friendsList.insert_one(friendList)

#Gets List of friends from user
def getFriendsList(userName):
    return friendsList.find_one({"Owner": userName})

#Adds two friends to each other's friends list <3
def addFriend(userName, targetFriend):
    friendList = friendsList.find_one({"Owner": userName})
    friendList2 = friendsList.find_one({"Owner": targetFriend})
    friendList["Friends"] += [targetFriend]
    friendList2["Friends"] += [userName]
    friendsList.replace_one({"Owner": userName},friendList)
    friendsList.replace_one({"Owner": targetFriend},friendList2)

#removes friends from eachother friends list </3
def removeFriend(userName, targetFriend):
    friendList = friendsList.find_one({"Owner": userName})
    friendList2 = friendsList.find_one({"Owner": targetFriend})
    friendList["Friends"].remove(targetFriend)
    friendList2["Friends"].remove(userName)
    friendsList.replace_one({"Owner": userName}, friendList)
    friendsList.replace_one({"Owner": targetFriend}, friendList2)


########################################################################################################################
demoDebt = {
    "UserName": "DanielLu",
    "Target": "BobJoe",
    "Balance": 150,
    "Reason": "Pizza money",
    "GroupID": 6768044637,
    "Date": date.today().strftime("%d/%m/%Y")
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
    "GroupID": 0 #0 signifies that there is no group attached to the transaction
}

demoGroup = {
    "GroupName": "Cool Kids Club",
    "Users": ["DanielLu","BobJoe","Tomothy"],
    "Budget": 2000
}
