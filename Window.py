import tkinter as tk

class Window():
    def __init__(self):
        # Setup window
        self.window = tk.Tk()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.mainFrame = tk.Frame(self.window)

        self.window.title("Test")
        self.window.geometry("500x800")
        self.window.resizable(1, 1)


        self.populate()
        (self.window).mainloop()
    def populateMain(self):
        self.mainFrame.pack()
    def