import tkinter as tk 

class Shape:
    def __init__(self, main = None):
        self.main = main
         
        # Calls create method of class Shape
        self.create()
     
    def create(self):
         
        # Creates a object of class canvas
        # with the help of this we can create different shapes
        self.canvas = tk.Canvas(self.main)
 
        # Creates a circle of diameter 80
        self.canvas.create_oval(10, 10, 80, 80, 
                            outline = "black", fill = "white",
                            width = 2)
         
        # Creates an ellipse with H. diameter: 210 and V. diameter: 80
        self.canvas.create_oval(110, 10, 210, 80,
                            outline = "red", fill = "green",
                            width = 2)
         
        # Creates a rectangle of 60 x 50 (width x height)
        self.canvas.create_rectangle(230, 10, 
                                     290, # pos_x(230) + width(60)
                                      60, # pos_y(10) + height(50)
                                outline = "black", fill = "blue",
                                width = 2)
         
        # Creates an arc of 210 deg
        self.canvas.create_arc(30, 200, 90, 100, start = 0,
                          extent = 210, outline = "green",
                          fill = "red", width = 2)
         
        points = [150, 100, 200, 120, 240, 180,
                  210, 200, 150, 150, 100, 200]
         
        # Creates a polygon
        self.canvas.create_polygon(points, outline = "blue",
                              fill = "orange", width = 2)
        # Pack the canvas to the main window and make it expandable
        self.canvas.pack(fill = tk.BOTH, expand = 1)
 
if __name__ == "__main__":
     
    # object of class Tk, responsible for creating
    # a tkinter toplevel window
    root = tk.Tk()
    shape = Shape(root)
 
    # Sets the title to Shapes
    root.title("Shapes")
 
    # Sets the geometry and position
    # of window on the screen
    root.geometry("400x300")
 
    # Infinite loop breaks only by interrupt
    root.mainloop()