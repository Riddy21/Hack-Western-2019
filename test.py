import DataBase as mdb

DBinterface = mdb.DataBase()

demoUser = {
    "name": {"first": "Test", "last": "Account"},
    "UserName": "User",
    "password": "pass",
    "Budget": 600  # monthly budget, resets at start of every month
}

DBinterface.add_user(demoUser)