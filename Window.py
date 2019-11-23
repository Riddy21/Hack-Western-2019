import tkinter as tk


class Window():
    def __init__(self):
        # Setup window
        self.window = tk.Tk()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.mainFrame = tk.Frame(self.window)
        self.transactionFrame = tk.Frame(self.window)
        self.groupsFrame = tk.Frame(self.window)
        self.membersFrame = tk.Frame(self.window)

        self.window.title("Test")
        self.window.geometry("500x800")
        self.window.resizable(1, 1)

        self.populateMain()
        (self.window).mainloop()

    def destroyFrame(self, frame):
        frame.destroy()

    def populateMain(self):
        self.mainFrame.pack()
        tk.Label(self.mainFrame, text = "1").pack()

    def populateTransaction(self):
        self.destroyFrame(self.mainFrame)
        self.transactionFrame.pack()
        #fsfg
