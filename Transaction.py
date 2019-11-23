import tkinter as tk

class Transaction():
    def __init__(self, name, date, amount, group):
        self.name = name
        self.date = date
        self.amount = amount
        self.group = group