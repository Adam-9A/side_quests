import math
import tkinter as tk
from tkinter import messagebox
from screeninfo import get_monitors

#region Variables + Functions
repairs = [ {"device": "GameBoy", "cost": 45, "time": 30, "success": True},
            {"device": "PS2", "cost": 80, "time": 60, "success": True},
            {"device": "iPod", "cost": 30, "time": 20, "success": False},
            {"device": "PSP", "cost": 70, "time": 45, "success": True},
            {"device": "GameBoy", "cost": 50, "time": 40, "success": True} ]

#endregion

#region Window Configuration

def center_on_monitor(root, monitor_index=1, width=500, height=500)->None:
    monitors = get_monitors()

    if monitor_index >= len(monitors):
        monitor_index = 0

    monitor = monitors[monitor_index]

    # Inverted logic because this function is for a second monitor
    if monitor_index != 0:
        x = monitor.x + (monitor.width - width-30)
        y = monitor.y + (monitor.height - height)//2+500
    else:
        x = monitor.x
        y = monitor.y

    root.geometry(f"{width}x{height}+{x}+{y}") #Since root is the reference to our object, we mutate instead of returning

#endregion

class App:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.root.title("Revenue Calculator")
        center_on_monitor(self.root)
        self.root.focus_force()
        self.root.lift()
        self.root.resizeable(width=0, height=0)
        self._build_ui()
        self.expand_view_toggle = True #self.check
        self.math_frame_toggle = True
        self.data_state = {}

    def _build_ui(self):
        #region Mainframes: Parent, Left, Right
        self.parent_frame = tk.Frame(self.root, bd=20, relief="ridge")
        self.parent_frame.pack(fill="both", expand=True)

        self.left_frame = tk.Frame(self.parent_frame, bd=1, relief="sunken")
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = tk.Frame(self.parent_frame, bd=1, relief="sunken")
        self.right_frame.pack(side="right", fill="both", expand=True)
        #endregion

        #region Left_frame widgets
        self.header_frame_left = tk.Frame(self.left_frame, bd=8, relief="ridge", bg="#2c3e50")
        self.header_frame_left.pack(side="top", fill="x")

        self.description = tk.Label(self.header_frame_left, text="Display Devices: ", font=("Arial", 20, "bold"), bg="#2c3e50", fg="white", padx=3, pady=4, )
        self.description.pack(side="left", anchor="n", padx=5, pady=1)

        self.toggle_button = tk.Button(self.header_frame_left, text="★", command= self.showcase_devides, font=("Arial", 20, "bold"), bg="#2c3e50", fg="red", pady=1, highlightcolor="black", highlightbackground="black", highlightthickness=2)
        self.toggle_button.pack(side="right", anchor="n", fill="x", expand=True, padx=5, pady=1)
        #endregion

        #region Right_frame widgets
        self.header_frame_right = tk.Frame(self.right_frame, bd=8, relief="ridge", bg="#2c3e50")
        self.header_frame_right.place(relx=0, rely=0, relheight=0.12, relwidth=1, anchor="nw")

        self.math_frame = tk.Frame(self.right_frame, bd=8, relief="ridge", bg="#2c3e40")
        self.math_frame.place(relx=0, rely=0.12, relheight=0.385, relwidth=1)

        self.display_frame = tk.Frame(self.right_frame, bd=8, relief="sunken", bg="#2c3e00")
        self.display_frame.place(relx=0, rely=0.515, relheight=0.245, relwidth=1)

        self.control_frame = tk.Frame(self.right_frame, bd=8, relief="ridge", bg="#3c3e50")
        self.control_frame.place(relx=0, rely=0.76, relheight=0.245, relwidth=1)

        #header_frame widget
        symbol_button = tk.Button(self.header_frame_right, text="★", command = self.toggle_math_frame, font=("Arial", 20, "bold"), bg="#2c3e50", fg="red", bd=3, relief="ridge", pady=1, highlightthickness=2, highlightbackground="black", highlightcolor="black")
        symbol_button.pack(fill="both", expand=True)

        #math_frame widgets
        cost_button = tk.Button(self.math_frame, text="Show cost", command=self.show_cost, font=("Arial", 17, "bold"), bd=1, highlightthickness=2, highlightbackground="black", highlightcolor="black", pady=2)
        cost_button.pack(side="top", fill="x", expand=False, pady=(0, 4))

        time_button = tk.Button(self.math_frame, text="Show time", command=self.show_time, pady=2, font=("Arial", 17, "bold"), bd=1, highlightthickness=2, highlightbackground="black", highlightcolor="black")
        time_button.pack(side="top", fill="x", expand=False, pady=4)

        success_button = tk.Button(self.math_frame, text="Success?", command=self.show_success, pady=2, font=("Arial", 17, "bold"), bd=1, highlightthickness=2, highlightbackground="black", highlightcolor="black")
        success_button.pack(side="top", fill="x", expand=False, pady=4)

        button_calc = tk.Button(self.math_frame, text="Most Profit", command=self.show_most_profit, pady=2, font=("Arial", 17, "bold"), bd=1, highlightthickness=2, highlightbackground="black", highlightcolor="black")
        button_calc.pack(side="top", fill="x", expand=False, pady=(4, 0))

        # display_frame widget
        self.result_label = tk.Label(self.display_frame, text="", font=("Arial", 30, "bold"))
        self.result_label.pack(anchor="center", fill="both", expand=True)

        #control_frame widgets
        button_iconify = tk.Button(self.control_frame, text="Iconify", command=lambda: self.root.iconify(), cursor="watch", font="Arial, 20", padx=1)
        button_iconify.pack(side="top", fill="both", expand=True)

        button_exit = tk.Button(self.control_frame, text="Exit", command=lambda: self.root.destroy(), padx=1, pady=1, font="Arial, 20")
        button_exit.pack(side="top", fill="both", expand=True)

        #endregion


        #for tomorrow: restructure the rest of the program. Left off with ghost button.












#region Main

def main():
    root = tk.Tk()
    one_instance = App(root, repairs)
    one_instance.root.mainloop()

if "__main__" == __name__:
    main()

#endregion