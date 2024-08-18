import tkinter as tk
from tkinter import ttk
import random as rd
import math


class Draw_app():
    
    def __init__(self) -> None:
        # Default
        self.angle = 0
        self.time_interval = 0

        self.reps = 0
        self.count_up = 0
        self.count_up_list = []

        self.canvas = None
        self.drawtime_entry = None
        self.timer = None

        # help to know when to switch countdown display
        self.is_break = False 

        # when to skip the draw timer
        self.is_skip = False

        # keep track if countdown is active or not
        self.start_countdown = False
        self.is_count_finished = False

        self.count_dwn = 0 # keep track of count for pause/play

        self.root = tk.Tk()

        self.root.title("Draw Timer")
        # self.root.geometry("400x400") # draw window
        self.root.config(padx=20, pady=20)

        # Title label
        self.title_label = tk.Label(self.root, text="Draw Timer", font=("Arial", 20))
        self.title_label.grid(row=0, column=0, columnspan=3, sticky="NSEW")
        
        # MENU UI
        self.create_menu_UI()
        # TIMER UI
        self.create_timer_UI()
        # LIST UI
        self.create_durationList_UI()
        ### =================DRAW MENU ===================== ###

        # main loop
        self.root.mainloop()

    def create_menu_UI(self):
        ### ================= MENU FRAME =================== ### 
        # Options Menu Frame
        self.menu_frame = tk.LabelFrame(self.root, text="Menu", padx=10, pady=10)
        self.menu_frame.grid(row=1, column=0, sticky="NSEW")

        # Radio Button to display time select
                # Radio Button ==============>
        def radio_action():
            print(radio_state.get())
            self.drawtime_entry.delete(0, tk.END)
            self.drawtime_entry.insert(tk.END,radio_state.get())

        # variable to hold which value is checked
        radio_state = tk.IntVar()

        self.radiobtn1 = tk.Radiobutton(self.menu_frame, text="30 sec", value=30, variable=radio_state, command=radio_action)
        self.radiobtn2 = tk.Radiobutton(self.menu_frame, text="60 sec", value=60, variable=radio_state, command=radio_action)
        self.radiobtn3 = tk.Radiobutton(self.menu_frame, text="2 mins", value=60*2, variable=radio_state, command=radio_action)
        self.radiobtn4 = tk.Radiobutton(self.menu_frame, text="3 mins", value=60*3, variable=radio_state, command=radio_action)
        self.radiobtn5 = tk.Radiobutton(self.menu_frame, text="5 mins", value=60*5, variable=radio_state, command=radio_action)
        self.radiobtn6 = tk.Radiobutton(self.menu_frame, text="10 mins", value=60*10, variable=radio_state, command=radio_action)
        
        self.radiobtn1.grid(row=0, column=0)
        self.radiobtn2.grid(row=0, column=1)
        self.radiobtn3.grid(row=1, column=0)
        self.radiobtn4.grid(row=1, column=1)
        self.radiobtn5.grid(row=2, column=0)
        self.radiobtn6.grid(row=2, column=1)

        # Display the time for the drawing interval
        self.drawtime_label = tk.Label(self.menu_frame, text="Time(sec)")

        self.drawtime_entry = tk.Entry(self.menu_frame, width=8)
        self.drawtime_entry.insert(tk.END, string="15")

        self.warning_label = tk.Label(self.menu_frame, text="", fg="red", font=("Arial", 10, "italic"))
        self.drawtime_label.grid(row=3, column=0)
        self.drawtime_entry.grid(row=3, column=1)
        self.warning_label.grid(row=4, column=0, columnspan=2)

        # break time between each drawing 
        self.break_val = tk.IntVar()
        self.break_slider = tk.Scale(self.menu_frame, from_=0, to=15, variable=self.break_val, orient=tk.HORIZONTAL)
        self.break_label = ttk.Label(self.menu_frame, text="breaks (sec)" )
        self.break_label.grid(row=5, column=0, columnspan=2)
        self.break_slider.grid(row=6, column=0, columnspan=2)

        ### ================ PLAYBACK - FRAME ===================== ###
        # playback Frame
        self.playback_frame = tk.LabelFrame(self.root)
        self.playback_frame.config(padx=10, pady=10)
        
        self.playback_frame.grid(row=2, column=0, sticky="NSEW")
        self.playback_frame.columnconfigure(0, weight=1)

        # Start, Pause and Reset Button
        # --------------------------- USING PACK()
        # self.start_btn = tk.Button(self.playback_frame, text="START").pack(fill=tk.BOTH)
   
        self.start_btn = tk.Button(self.playback_frame, text="START", command=self.start_timer)
        self.start_btn.grid(row=0, column=0, sticky="NSEW")
        self.pause_btn = tk.Button(self.playback_frame, text="PAUSE", command=self.play_pause)
        self.pause_btn.grid(row=1, column=0, sticky="NSEW")
        self.reset_btn = tk.Button(self.playback_frame, text="RESET", command=self.reset_timer)
        self.reset_btn.grid(row=2, column=0, sticky="NSEW")

    def create_durationList_UI(self ):
        ### ================ ELAPSED TIME FRAME ============ ###
        self.elap_time_frame = tk.LabelFrame(self.root, text="Elapsed Time", padx=10, pady=10)
        self.elap_time_frame.grid(row=1, column=2, rowspan=3, sticky='NS')
        tk.Grid.rowconfigure(self.elap_time_frame, 0, weight=1)

        # Display list of Elapsed time
        self.time_scrollbar = tk.Scrollbar(self.elap_time_frame)
        self.time_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.timelist = tk.Listbox(self.elap_time_frame, yscrollcommand=self.time_scrollbar.set)
        self.timelist.config(width=10, font=("Cursive", 18,"bold"))
        # for i in range(20):
        #     self.timelist.insert(tk.END, f" {i+1:02d} - {rd.randint(1,60):02d}:{rd.randint(1,60):02d}")

        self.timelist.pack(side=tk.LEFT, fill=tk.BOTH)
        self.time_scrollbar.config(command=self.timelist.yview)

    def create_timer_UI(self):
        self.timer_frame_label = tk.LabelFrame(self.root, text="Timer")
        self.timer_frame_label.grid(row=1, column=1, rowspan=2, sticky="NSEW")

        # TIMER LABEL
       # create canvas 
        self.canvas = tk.Canvas(self.timer_frame_label, 
                                width=240, height=240,
                                 highlightthickness=0)
        
        self.canvas.config(bg="#f7f5dd", highlightthickness=0)
        self.canvas.grid(row=1, column=1)

        self.canvas_text()
        self.canvas_circular_progress()

        # Skip Label
        self.skip_button = tk.Button(self.timer_frame_label, text="SKIP TO NEXT", command=self.skip_countdown)
        self.skip_button.grid(row=2, column=1, sticky="S", padx=20, pady=20)

    def canvas_text(self):
        self.timer_text = self.canvas.create_text(120, 120, text="00:00", fill="brown", font=("Courier", 50, "bold" ))
        
    def canvas_circular_progress(self):
        self.width = self.canvas.winfo_reqwidth()
        self.height = self.canvas.winfo_reqheight()
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.radius = min(self.center_x, self.center_y) - 5

        self.pos_x = self.center_x - self.radius
        self.pos_y = self.center_y - self.radius
        self.diameter_x = self.center_x + self.radius
        self.diameter_y = self.center_y + self.radius
        self.canvas.create_oval(self.pos_x, self.pos_y, self.diameter_x, self.diameter_y,
                                outline="gray", width=5)

        self.arc = self.canvas.create_arc(self.pos_x, self.pos_y, self.diameter_x, self.diameter_y, 
                                          start=0, extent=0, outline="gray", 
                                          width=5, style=tk.ARC)
        
    def get_and_validate_drawtime(self):
        '''
        Check if the draw time is valid value or through 
        Valuerror warning if failed
        @return int value
        '''
        default_entry = 30
        try:
            entry_value = self.drawtime_entry.get()

            if(entry_value == ""): 
                self.warning_label.config(text = "Time is empty, will use default")
                return default_entry
             
            entry_value = int(float(entry_value))

            if(entry_value == 0): 
                self.warning_label.config(text = "Zero value, will use default")
                return default_entry

        except ValueError:
            self.warning_label.config(text = "Invalid Input, will use default")
            return default_entry

        # All is good, Reset the warning label,
        self.warning_label.config(text = "")

        return entry_value 

    def start_timer(self):

        # set the initial time interval conversion

        if(self.time_interval < 0):
            self.warning_label.config(text = "Time to small")
            return

        # clear warning
        self.warning_label.config(text = "")

        # start first countdown
        self.start_countdown = True
        self.count_down()

    '''============= Count down timer ===================== '''
    def count_down(self):

        # get the value assigned to slider
        self.short_break_sec = self.break_val.get()
        self.draw_time_min = self.get_and_validate_drawtime()
        self.reps += 1

        # switch between `initial time interval` and `break time interval`
        if self.reps %2 == 0 and self.short_break_sec != 0:
            self.is_break = True
            self.time_interval = self.short_break_sec
            self.update_timer(self.time_interval, 0)

        else :
            self.is_break = False
            self.time_interval = self.draw_time_min
            self.update_timer(self.time_interval, 0)
        
    def min_sec(self, count):
        return count // 60, count % 60

    def update_count_up(self, c):
        self.count_up_list.append(c)
        self.timelist.insert(tk.END, f" {len(self.count_up_list):02d} - {self.min_sec(c)[0]:02d}:{self.min_sec(c)[1]:02d}")
        self.count_up = 0

    '''============ update timer ==========='''
    def update_timer(self, count_dwn, count_up):


        # check if to start countdown
        if self.start_countdown or self.is_break: 

            # disable Start button to avoid multiple countdown
            self.start_btn.config(state=tk.DISABLED)

            # update timer text
            self.min, self.sec = self.min_sec(count_dwn)

            # update count up
            self.count_up = count_up

            # update canvas circle
            self.angle = math.floor((count_dwn/self.time_interval)*359)
            # print(self.angle)
            if self.angle < 0: self.angle = 360 # Reset if completed circle
            self.canvas.itemconfig(self.arc, extent=self.angle, outline="blue" if self.angle >= 30 else "red")



            if not self.is_break:
                # Update canvas text normal interval
                self.count_dwn = count_dwn
                self.canvas.itemconfig(self.timer_text, text=f"{self.min:02d}:{self.sec:02d}" )
                self.pause_btn.config(state=tk.NORMAL)
                self.reset_btn.config(state=tk.NORMAL)
                 
            else:    
                # break time countdown display
                self.canvas.itemconfig(self.timer_text, text=f"{self.sec}" )
                self.canvas.itemconfig(self.arc, outline="#999922")
                # prohibit clicking of pause btn
                self.pause_btn.config(state=tk.DISABLED)
                self.reset_btn.config(state=tk.DISABLED)
                
            # Count only positive values,
            if count_dwn > 0:
                    self.timer = self.root.after(1000, self.update_timer, count_dwn - 1, count_up + 1)
        
            else: # Count has finished restart count

                # Store and Display the count_up value 
                if not self.is_break:
                    self.update_count_up(count_up)

                # start countdown again
                self.count_down()

    '''============ Reset and Pause ==============='''

    def play_pause(self):

        if not self.is_count_finished: # not done
            self.start_countdown = not self.start_countdown # stop count

            # continue countdown
            if self.count_dwn > 0 and self.start_countdown:
                self.pause_btn.config(text="PAUSE")
                self.update_timer(self.count_dwn, self.count_up)
            else:
                self.pause_btn.config(text="PLAY")
                self.canvas.itemconfig(self.arc, outline="#00ddee")

    # ---------------------------- TIMER RESET ------------------------------- # 
    def reset_timer(self):
        self.is_break = False
        self.start_countdown = False
        self.reps = 0
        self.count_dwn = 0
        self.root.after_cancel(self.timer)
        self.canvas.itemconfig(self.timer_text , text="00:00")
        self.canvas.itemconfig(self.arc, extent=360, outline="gray")
        self.start_btn.config(state=tk.NORMAL)
            
    # --------------------- SKIP TIMER --------------------------#############
    def skip_countdown(self):
        # update timelist
        self.update_count_up(self.count_up)
        self.reset_timer()
        self.start_timer()



if __name__ == "__main__":
    Draw_app()


    

