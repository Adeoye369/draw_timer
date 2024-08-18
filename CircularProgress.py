import tkinter as tk

class CircularProgress(tk.Canvas):
    def __init__(self, main=None, **kw):
        super().__init__(main, **kw)
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.radius = min(self.center_x, self.center_y) - 5
        self.angle = 0
        self.speed = 1

        self.config(bg="white", highlightthickness=0)

        self.pos_x = self.center_x - self.radius
        self.pos_y = self.center_y - self.radius
        self.diameter_x = self.center_x + self.radius
        self.diameter_y = self.center_y + self.radius

        self.create_oval(self.pos_x, self.pos_y, self.diameter_x, self.diameter_y,outline="gray", width=2)

        self.arc = self.create_arc(self.pos_x, self.pos_y, self.diameter_x, self.diameter_y, start=0, extent=0, outline="gray", width=3, style=tk.ARC)
        
        self.after(50, self.update)


    def update(self):
        self.angle += self.speed
        if self.angle > 360:
            self.angle = 0
        self.draw_arc()
        self.after(50, self.update)


    def draw_arc(self):
        self.itemconfig(self.arc, extent=self.angle, outline="blue" if self.angle <= 300 else "red")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Circl")
    root.config(padx=10, pady=10)
    progress = CircularProgress(root, width=300, height=300)
    progress.pack()

    root.mainloop()