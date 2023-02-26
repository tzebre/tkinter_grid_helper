import tkinter as tk
import customtkinter as ctk
import random


def random_color(hex_val):
    for i in range(3):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        rgb = [r, g, b]
        if hex_val:
            return f"#{r:02x}{g:02x}{b:02x}"
        else:
            return rgb


class Customframe(tk.Frame):
    def __init__(self, master, row=None, col=None, debug=False, **kwargs):
        super().__init__(master)
        self.debug = debug
        self.row = row
        self.col = col
        self.dict_args = kwargs
        self.grid_config()

    def grid_config(self):
        for i, r in enumerate(self.row):
            self.grid_rowconfigure(i, weight=r)
        for i, c in enumerate(self.col):
            self.grid_columnconfigure(i, weight=c)
        if self.debug:
            for r_i, r in enumerate(self.row):
                for c_i, c in enumerate(self.col):
                    test = ctk.CTkFrame(master=self, fg_color=random_color(True), border_width=2, border_color="red")
                    test.grid(row=r_i, column=c_i, sticky="nsew")
                    test.grid_rowconfigure(0, weight=1)
                    test.grid_columnconfigure(0, weight=1)
                    txt = ctk.CTkLabel(master=test, text=f"r:{r_i}, rw:{r}, c:{c_i}, cw:{c}")
                    txt.grid(row=0, column=0)


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Debug")
        self.scale_value = {"row": {}, "col": {}}
        self.config()
        self.attributes("-topmost", True)

    def config(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.row_entry = ctk.CTkEntry(master=self, placeholder_text="Number of row")
        self.col_entry = ctk.CTkEntry(master=self, placeholder_text="Number of colmun")
        self.row_entry.grid(row=0, column=0)
        self.col_entry.grid(row=0, column=1)
        self.ok_btn = ctk.CTkButton(master=self, text="Validate", command=self.place_slider)
        self.ok_btn.grid(row=1, column=0, columnspan=2)

    def display(self):
        self.row = list(self.scale_value["row"].values())
        self.col = list(self.scale_value["col"].values())

    def scale_mvd(self, value, c, r):
        if c == 0:
            self.scale_value["row"][r] = int(value)
        else:
            self.scale_value["col"][r] = int(value)
        self.display()
        self.custom.row = self.row
        self.custom.col = self.col
        self.custom.grid_config()

    def place_slider(self):
        ok = False
        nb_col = 0
        nb_row = 0
        try:
            nb_row = int(self.row_entry.get())
            ok = True
        except ValueError as v:
            print(f"Please enter a valid integer for row: {v}")
            ok = False
        try:
            nb_col = int(self.col_entry.get())
            ok = True
        except ValueError as v:
            print(f"Please enter a valid integer for col: {v}")
            ok = False
        if ok:
            self.scale_value = {"row": {}, "col": {}}
            try:
                self.slider_frame_row.destroy
                self.slider_frame_col.destroy
            except AttributeError:
                print("slider already destroyed")
            self.slider_frame_row = ctk.CTkFrame(master=self)
            self.slider_frame_row.grid_columnconfigure(0, weight=1)
            self.slider_frame_row.grid(row=2, column=0, sticky="nsew")
            self.slider_frame_col = ctk.CTkFrame(master=self)
            self.slider_frame_col.grid_columnconfigure(0, weight=1)
            self.slider_frame_col.grid(row=2, column=1, sticky="nsew")
            frame = [self.slider_frame_row, self.slider_frame_col]
            for i, w in enumerate([nb_row, nb_col]):
                for line in range(w):
                    if i == 0:
                        self.scale_value["row"][line] = 1
                    else:
                        self.scale_value["col"][line] = 1
                    self.display()
                    frame[i].grid_rowconfigure(line, weight=1)
                    slider = tk.Scale(master=frame[i], from_=1, to=10, orient="horizontal", bd=0, sliderrelief=tk.FLAT,
                                      troughcolor='gray92', activebackground="#1F6AA5",
                                      command=lambda value, c=i, r=line: self.scale_mvd(value, c, r))
                    slider.grid(row=line, column=0, sticky="nsew", padx=3)
            display_btn = ctk.CTkButton(master=self, text="Validate", command=self.display)
            display_btn.grid(row=3, column=0, columnspan=2)
            self.create_toplevel()

    def create_toplevel(self):
        try:
            self.top_level.destroy()
        except:
            pass
        self.top_level = tk.Toplevel(self)
        self.top_level.lower(belowThis=self)
        self.top_level.geometry(
            "{}x{}+{}+{}".format(self.winfo_screenwidth(), self.winfo_screenheight(), int(0), int(0)))
        self.top_level.lower(belowThis=self)
        self.top_level.grid_columnconfigure(0, weight=1)
        self.top_level.grid_rowconfigure(0, weight=1)
        self.custom = Customframe(self.top_level, self.row, self.col, True)
        self.custom.grid(row=0, column=0, sticky="nsew")



app = Application()
app.mainloop()
