import tkinter as tk
from tkinter import ttk

def dda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    x_inc = dx / steps
    y_inc = dy / steps

    x, y = x1, y1
    points = []
    for _ in range(steps + 1):
        points.append((round(x), round(y)))
        x += x_inc
        y += y_inc
    return points

def bresenham_line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1
    err = dx - dy

    x, y = x1, y1
    points = []
    while True:
        points.append((x, y))
        if x == x2 and y == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    return points

def bresenham_circle(xc, yc, r):
    x, y = 0, r
    d = 3 - 2 * r
    points = []

    while x <= y:
        points += [
            (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)
        ]
        if d <= 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1
    return points

class RasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритмы растеризации")
        self.root.geometry("1200x800")
        self.root.configure(bg="#ECEFF4")

        self.scale = 20
        self.offset_x = 0
        self.offset_y = 0

        self.canvas = tk.Canvas(root, bg="#FFFFFF", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.points = [] 

        self.control_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(self.control_frame, text="Координаты", font=("Helvetica", 14)).pack(anchor="w", pady=(0, 10))
        
        self.create_input_field("X1:", "x1_entry")
        self.create_input_field("Y1:", "y1_entry")
        self.create_input_field("X2:", "x2_entry")
        self.create_input_field("Y2:", "y2_entry")
        self.create_input_field("Радиус:", "radius_entry")

        ttk.Label(self.control_frame, text="Алгоритмы", font=("Helvetica", 14)).pack(anchor="w", pady=(20, 10))
        self.create_button("ЦДА", self.run_dda)
        self.create_button("Брезенхем (отрезок)", self.run_bresenham_line)
        self.create_button("Брезенхем (окружность)", self.run_bresenham_circle)
        self.create_button("Очистить", self.clear_canvas)

        ttk.Label(self.control_frame, text="Управление масштабом", font=("Helvetica", 14)).pack(anchor="w", pady=(20, 10))
        self.create_button("Приблизить", self.zoom_in)
        self.create_button("Отдалить", self.zoom_out)

        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.do_pan)

        self.redraw()

    def create_input_field(self, label_text, attribute_name):
        ttk.Label(self.control_frame, text=label_text, font=("Helvetica", 12)).pack(anchor="w", pady=(5, 0))
        setattr(self, attribute_name, ttk.Entry(self.control_frame))
        getattr(self, attribute_name).pack(fill=tk.X, pady=5)

    def create_button(self, text, command):
        ttk.Button(self.control_frame, text=text, command=command).pack(fill=tk.X, pady=5)

    def run_dda(self):
        try:
            x1 = int(self.x1_entry.get())
            y1 = int(self.y1_entry.get())
            x2 = int(self.x2_entry.get())
            y2 = int(self.y2_entry.get())
            points = dda(x1, y1, x2, y2)
            self.points.extend(points)
            self.redraw()
        except ValueError:
            print("Введите корректные координаты.")

    def run_bresenham_line(self):
        try:
            x1 = int(self.x1_entry.get())
            y1 = int(self.y1_entry.get())
            x2 = int(self.x2_entry.get())
            y2 = int(self.y2_entry.get())
            points = bresenham_line(x1, y1, x2, y2)
            self.points.extend(points)
            self.redraw()
        except ValueError:
            print("Введите корректные координаты.")

    def run_bresenham_circle(self):
        try:
            xc = int(self.x1_entry.get())
            yc = int(self.y1_entry.get())
            r = int(self.radius_entry.get())
            points = bresenham_circle(xc, yc, r)
            self.points.extend(points)
            self.redraw()
        except ValueError:
            print("Введите корректные координаты.")

    def draw_points(self):
        for x, y in self.points:
            x_scaled = (x * self.scale) + self.offset_x + self.canvas.winfo_width() // 2
            y_scaled = (y * self.scale) + self.offset_y + self.canvas.winfo_height() // 2
            self.canvas.create_oval(x_scaled - 2, y_scaled - 2, x_scaled + 2, y_scaled + 2, fill="black")

    def draw_axes(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        cx = width // 2 + self.offset_x
        cy = height // 2 + self.offset_y

        # Рисуем ось Y
        self.canvas.create_line(cx, 0, cx, height, fill="#E63946", width=2)
        # Рисуем ось X
        self.canvas.create_line(0, cy, width, cy, fill="#457B9D", width=2)

    def clear_canvas(self):
        self.points = []
        self.redraw()

    def redraw(self):
        self.canvas.delete("all")
        self.draw_axes() 
        self.draw_points()

    def start_pan(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def do_pan(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.offset_x += dx
        self.offset_y += dy
        self.start_x = event.x
        self.start_y = event.y
        self.redraw()

    def zoom(self, zoom_factor):
        new_scale = self.scale * zoom_factor
        self.scale = max(5, new_scale)
        self.redraw()

    def zoom_in(self):
        self.zoom(1.1)

    def zoom_out(self):
        self.zoom(0.9)

if __name__ == "__main__":
    root = tk.Tk()
    app = RasterApp(root)
    root.mainloop()