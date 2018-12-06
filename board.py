import tkinter as tk


class BoardGUI:

    def __init__(self, root):
        self.width = 720
        self.height = 620
        canvas = tk.Canvas(root, width=self.width, height=self.height)
        canvas.pack()
        self.canvas = canvas
        self.drawBoard()

    def __repr__(self):
        return "Canvas - Width: %d, Height: %d" % (self.width, self.height)

    def drawBoard(self):
        for i in range(7):
            x = 10 + i * 100
            for j in range(6):
                y = 10 + j * 100
                self.canvas.create_rectangle(x, y, x + 100, y + 100,
                                             fill="blue")
                self.canvas.create_oval(x, y, x + 100, y + 100,
                                        fill="white")

root = tk.Tk()
b = BoardGUI(root)
root.mainloop()
