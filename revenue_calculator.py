import math
import tkinter as tk
from tkinter import messagebox
from typing import Any
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
    def __init__(self, root):
        self.root = root
        self.root.title("Revenue Calculator")

        center_on_monitor(self.root)
        self.root.focus_force()
        self.root.lift()
        self.root.resizable(width=0, height=0)
        self._build_ui()

        self.data_state = {}
        self.devices_frame_here = True #self.check
        self.math_frame_here = True


    def _build_ui(self):
        #region Mainframes: Parent, Left, Right
        self.parent_frame = tk.Frame(self.root, bd=20, relief="ridge")
        self.parent_frame.pack(fill="both", expand=True)

        self.left_frame = tk.Frame(self.parent_frame, bd=1, relief="sunken")
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = tk.Frame(self.parent_frame, width=50, bd=1, relief="sunken")
        self.right_frame.pack(side="right", fill="both", expand=True)
        #endregion

        #region Left_frame widgets
        self.header_frame_left = tk.Frame(self.left_frame, bd=8, relief="ridge", bg="#2c3e50")
        self.header_frame_left.pack(side="top", fill="x")

        self.description = tk.Label(self.header_frame_left, text="Display Devices: ", font=("Arial", 20, "bold"), bg="#2c3e50", fg="white", padx=3, pady=4, )
        self.description.pack(side="left", anchor="n", padx=5, pady=1)

        self.toggle_button = tk.Button(self.header_frame_left, text="★", command= self.initiate_devices_frame, font=("Arial", 20, "bold"), bg="#2c3e50", fg="red", pady=1, highlightcolor="black", highlightbackground="black", highlightthickness=2)
        self.toggle_button.pack(side="right", anchor="n", fill="x", expand=True, padx=5, pady=1)

        #ghost parts
        self.ghost_button = tk.Button(self.header_frame_left, text="★", command=self.hide_devices_frame, font=("Arial", 20, "bold"), bg="#2c3e50", fg="red", pady=1, highlightthickness=2, highlightbackground="black", highlightcolor="black")
        self.ghost_button.pack_forget()

        self.header_frame_left_2 = tk.Frame(self.left_frame, bd=8, bg="#2c3e50", relief="ridge")
        self.header_frame_left_2.pack_forget()

        self.ghost_device_buttons = []

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






    #region Callback functions

    def initiate_devices_frame(self) -> None:

        self.toggle_button.config(state="disabled") #just in case
        self.toggle_button.pack_forget()

        self.description.pack_forget() #Geometry behaved strangely if the new button was inserted while this was active

        self.ghost_button.pack(side="left", anchor="w", padx=1, pady=1, fill="x", expand=True)

        self.description.config(text="Available Devices: ")
        self.description.pack(side="left", anchor="n", padx=1, pady=1)

        if self.devices_frame_here:
            self.activate_devices_frame()
        else:
            pass

    def activate_devices_frame(self) -> None:

        self.header_frame_left_2.pack(side="left", fill="both", expand=True)

        self.devices_frame_here = False

        device_data: dict[str, Any] = Math(repairs).get_names()

        ghost_device_button_names = list(device_data.keys())

        for name in ghost_device_button_names:
            temp = tk.Button(self.header_frame_left_2, text=name, pady=2, bd=1, font=("Arial", 16), highlightcolor="black", highlightthickness=2, highlightbackground="black")
            temp.pack(side="top", fill="x", anchor="n", padx=3, pady=3)
            temp.config(command= lambda x=temp, y=device_data[name]: self.insert_data(x,y)) #temp has to be created before assigned, hence config
            self.ghost_device_buttons.append(temp)

    def insert_data(self, which_button, single_dict):
        if which_button["highlightcolor"] == "black" and which_button["highlightbackground"] == "black":
            which_button.config(highlightcolor="red", highlightbackground="yellow")
            self.data_state[which_button] = single_dict
        else:
            which_button.config(highlightcolor="black", highlightbackground="black")
            self.data_state.pop(which_button, None)

        # button_object: {"device": "PS2", "cost": 80, "time": 60, "success": True}

    def hide_devices_frame(self) -> None:
        self.ghost_button.pack_forget()
        self.description.pack_forget()
        self.description.config(text="Display Devices:")
        self.description.pack(side="left", anchor="n", padx=5, pady=1)
        self.toggle_button.config(state="normal")
        self.toggle_button.pack(side="left", anchor="n", padx=5, pady=1, fill="x", expand=True)
        for button in self.ghost_device_buttons:
            button.pack_forget()
        self.devices_frame_here = True
        self.header_frame_left_2.pack_forget()
        self.data_state = {}

    def toggle_math_frame(self):
        if self.math_frame_here:
            self.math_frame.place_forget()
            self.math_frame_here = False
        else:
            self.math_frame.place(relx=0, rely=0.12, relwidth=1, relheight=0.385)
            self.math_frame_here = True
            self.math_frame.lift()
            self.math_frame.update_idletasks()  #Process all pending idle tasks right now.
    #endregion

    #region Callback functions + Math
     #Still need division of responsibility.
    def show_cost(self):

        cost_list = []  # if nothing is inside, python returns 0!

        # data_format: { button_object: {"device": "PS2", "cost": 80}, button_object: {"device": "PS2", "cost" : 80}

        for repair_dict in self.data_state.values():
            cost = int(repair_dict["cost"])
            cost_list.append(cost)

        result = sum(cost_list)
        self.result_label.config(text=str(result) + "$")

        # example: {"device": "PS2", "cost": 80, "time": 60, "success": True}
        # okay, we stopped here but found a bug: if we hide our devices, the selected buttons cost value is saved and not removable anymore!
        # made add into the star buttons hide function a way to clear cost_list #fixed today.

    def show_time(self):
        # data_format: { button_object: {"device": "PS2", "cost": 80}, button_object: {"device": "PS2", "cost" : 80}
        total_time = []

        for repair_dict in self.data_state.values():
            time = int(repair_dict["time"])
            total_time.append(time)

        result = sum(total_time)
        self.result_label.config(text=str(result) + "\n mins")

    def show_success(self):
        # data_format: { button_object: {"device": "PS2", "cost": 80}, button_object: {"device": "PS2", "cost" : 80}

        success: bool | None = None

        for i, repair_dict in enumerate(self.data_state.values()):
            temp_success = repair_dict["success"]
            if i > 0:
                messagebox.showinfo("Bad selection", "Success info can be applied to one device only", parent=self.root)
                return
            success = temp_success

        result = success
        self.result_label.config(text=str(result))

    def show_most_profit(self):
        just_times = []

        if not self.data_state:
            self.result_label.config(text="None \nselected", font=("Arial", 20))
            return

        for repair_dict in self.data_state.values():
            if repair_dict["success"] is False:
                continue
            try:
                just_times.append(int(repair_dict["time"]))
            except (KeyError, TypeError, ValueError):
                pass

        common_base = math.lcm(*just_times)  # expects separate integer arguments, not one list
        # * -> unpacks the list into separate arguments

        # cost * common base // time
        true_costs = []

        for repair_dict in self.data_state.values():
            if repair_dict["success"] is False:
                continue
            quotient = common_base // repair_dict["time"]
            true_cost = repair_dict["cost"] * quotient
            true_costs.append((repair_dict["device"], true_cost, quotient))

        most_profitable = ("None", 0, 1)

        for device, price, _ in true_costs:
            if price > most_profitable[1]:
                most_profitable = device, price, _
            else:
                continue

        return_to_normal_price = int(most_profitable[1]) // int(most_profitable[2])
        result = (most_profitable[0], return_to_normal_price)

        if result == ("None", 0):
            self.result_label.config(text=" Device did \nnot sell", font=("Arial", 20))
        else:
            self.result_label.config(text=f"{str(result[0])} \nwith {str(result[1])}$", font=("Arial", 17))

    #endregion


class Math:
    def __init__(self, data):
        self.data: list[dict] = data

    def get_names(self) -> dict[str, Any]:
        aggregate_by_device = {}
        for one_dict in self.data:
            base_key = one_dict["device"]
            key_new = base_key
            counter = 2

            while key_new in aggregate_by_device:
                key_new = f"{self._number_to_ordinal(counter)} {base_key}"
                counter += 1

            aggregate_by_device[key_new] = one_dict

        return aggregate_by_device

    @staticmethod
    def _number_to_ordinal(n: int) -> str:
        ordinals = {2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth", 6: "Sixth", 7: "Seventh"}
        return ordinals.get(n, str(n))


















#region Main

def main():
    root = tk.Tk()
    one_instance = App(root)
    one_instance.root.mainloop()

if "__main__" == __name__:
    main()

#endregion