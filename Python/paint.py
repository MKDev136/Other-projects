import tkinter as tk
from tkinter import *
from PIL import ImageGrab

class PaintApp:
    def __init__(self):
        self.w = tk.Tk()
        self.w.title("Paint")
        self.w.geometry("500x500")
        self.w.resizable(False, False)

        self.actual_x, self.actual_y = 0, 0
        self.draw_mode = "draw"  
        self.color = "black"
        self.width_line = 1
        self.temp_circle = None
        self.saved = False

        self.create_ui()
        self.bind_events()

        self.w.mainloop()

    def create_ui(self):
        self.frame_btn = Frame(self.w, bg="purple", width=500, height=25)
        self.frame_btn.pack(side=TOP, fill=X)

        self.name_file = Entry(self.frame_btn)
        self.name_file.place(x=0, y=0)

        self.btn_save = Button(self.frame_btn, text="Save", command=self.save_image)
        self.btn_save.place(x=125, y=0)

        self.btn_close = Button(self.frame_btn, text="Close", command=self.confirm_exit)
        self.btn_close.place(x=375, y=0)

        self.title = Label(self.w, text="Paint", bg="black", fg="white", width=75, height=2, font=50)
        self.title.pack()

        self.frame_canvas = Frame(self.w)
        self.frame_canvas.pack()
        self.canvas = Canvas(self.frame_canvas, bg="grey", width=450, height=300)
        self.canvas.pack(side=RIGHT, anchor="n")

        self.btn_clear = Button(self.w, text="Clear", command=self.clear, bg="white", fg="black")
        self.btn_clear.pack(side=RIGHT, anchor="n")

        self.btn_width = Scale(self.w, from_=1, to=20, orient=HORIZONTAL, bg="burlywood4", fg="white")
        self.btn_width.pack(side=TOP, anchor="w")

        self.line_ex_width = Canvas(self.w, bg="grey", width=50, height=50, highlightbackground="black", highlightthickness=1)
        self.line_ex_width.pack(side=LEFT, anchor="n")
        self.line_ex_width.create_line(0, 25, 55, 25, fill="white", width=self.width_line)

        self.btn_draw = Button(self.w, text="Draw", command=lambda: self.set_mode("draw"))
        self.btn_draw.pack(anchor="e")
        self.btn_square = Button(self.w, text="Square", command=lambda: self.set_mode("square"))
        self.btn_square.pack(anchor="e")
        self.btn_circle = Button(self.w, text="Circle", command=lambda: self.set_mode("circle"))
        self.btn_circle.pack(anchor="e")

        colors = ["white", "brown", "red", "orange", 'yellow', "green", "blue", "pink", "violet", 'black', 'grey']
        funcs = [self.set_white, self.set_brown, self.set_red, self.set_orange, self.set_yellow, self.set_green,
                 self.set_blue, self.set_pink, self.set_violet, self.set_black, self.set_eraser]
        for c, f in zip(colors, funcs):
            btn = Button(self.frame_canvas, bg=c, width=4, command=f)
            btn.pack(anchor="w")

    def bind_events(self):
        self.canvas.bind('<Button-1>', self.start_draw)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.finalize_circle)
        self.btn_width.bind('<Leave>', self.update_line_preview)

    def set_white(self): self.color = "white"
    def set_red(self): self.color = "red"
    def set_pink(self): self.color = "pink"
    def set_violet(self): self.color = "violet"
    def set_green(self): self.color = "green"
    def set_black(self): self.color = "black"
    def set_blue(self): self.color = "blue"
    def set_orange(self): self.color = "orange"
    def set_yellow(self): self.color = "yellow"
    def set_brown(self): self.color = "brown"
    def set_eraser(self): self.color = "grey"

    def set_mode(self, mode):
        self.draw_mode = mode

    def start_draw(self, event):
        self.actual_x, self.actual_y = event.x, event.y

    def draw(self, event):
        w = self.width_line
        if self.draw_mode == "draw":
            self.canvas.create_line(self.actual_x, self.actual_y, event.x, event.y, fill=self.color, width=w)
            self.actual_x, self.actual_y = event.x, event.y
        elif self.draw_mode == "square":
            self.canvas.create_rectangle(self.actual_x, self.actual_y, event.x, event.y, fill=self.color, width=2, outline=self.color)
        elif self.draw_mode == "circle":
            if self.temp_circle:
                self.canvas.delete(self.temp_circle)
            dx = event.x - self.actual_x
            dy = event.y - self.actual_y
            r = min(abs(dx), abs(dy))
            x2 = self.actual_x + r * (1 if dx >= 0 else -1)
            y2 = self.actual_y + r * (1 if dy >= 0 else -1)
            self.temp_circle = self.canvas.create_oval(self.actual_x, self.actual_y, x2, y2, outline=self.color, width=2)

    def finalize_circle(self, event):
        self.temp_circle = None

    def clear(self):
        self.canvas.delete("all")

    def update_line_preview(self, event):
        self.width_line = self.btn_width.get()
        self.line_ex_width.delete("all")
        self.line_ex_width.create_line(0, 25, 55, 25, fill="white", width=self.width_line)

    def confirm_exit(self):
        if not self.saved:
            popup = tk.Toplevel(self.w)
            popup.geometry("300x100")
            popup.title("Confirm Exit")

            Label(popup, text="If you don't save, you will lose all your progress").pack()
            Button(popup, text="Yes", command=self.w.destroy).pack()
            Button(popup, text="No", command=popup.destroy).pack()
        else:
            self.w.destroy()

    def save_image(self):
        x = self.w.winfo_rootx()
        y = self.w.winfo_rooty() + 100
        filename = self.name_file.get()
        if filename == "":
            Label(self.w, text="PLEASE, NAME THE FILE IN THE ENTRY !!!", bg="grey", fg="white").place(y=400, x=150)
        else:
            ImageGrab.grab(bbox=(x, y, x + 800, y + 500)).save(f"{filename}.png")
            self.saved = True
