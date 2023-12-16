import tkinter as tk
from PIL import Image, ImageTk
import psycopg2

class ZoomableWindow:
    def __init__(self, parent_frame):
        self.frame = tk.Frame(parent_frame)
        self.frame.pack(fill=tk.BOTH, expand=True)
        #,bg="#9BABB8"
        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image = None
        self.original_width = 0
        self.original_height = 0
        self.zoom_level = 1.0

        self.points = []

        self.canvas.bind("<Configure>", self.resize_window)
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<Button-3>", self.add_point)
        self.canvas.bind("<MouseWheel>", self.zoom)

        self.drag_data = {"x": 0, "y": 0, "item": None}

        self.fetch_data()
        self.show_points()
    

    def fetch_data(self):
        try:
            connection = psycopg2.connect(
                host="localhost",
                database="resQBot",
                user="postgres",
                port="69",
                password="0000"
            )
            cursor = connection.cursor()

            # Define the tables and their associated colors
            tables = [
                ("survivor_locations", "red"),
                ("bot", "blue"),
                ("obstacles", "black"),
                ("bot_current_location", "green")
            ]

            for table, color in tables:
                cursor.execute(f"SELECT * FROM {table};")
                rows = cursor.fetchall()

                for row in rows:
                    x, y = row[1], row[2]  # Assuming coordinates are in column 1 and 2
                    self.points.append((x, y, color))  # Add the color information to each point

            cursor.close()
            connection.close()

        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL database:", e)

    def show_points(self):
        self.canvas.delete("points")
        bot_points = []
        bot_current_location_points = []
        obstacles = []
        survivor_locations =[]

        for point in self.points:
            if len(point) >= 3 and point[2] == "green":
                bot_current_location_points.append(point)
            elif len(point) >= 3 and point[2] == "black":
                obstacles.append(point)
                # Ignore points with color "black" (obstacles)
                continue
            elif len(point) >= 3 and point[2] == "blue":
                bot_current_location_points.append(point)
                bot_points.append(point)
            elif len(point) >= 3 and point[2] == "red":
                survivor_locations.append(point)
                x = point[0] * self.zoom_level + self.canvas.winfo_width() / 2
                y = point[1] * self.zoom_level + self.canvas.winfo_height() / 2
                color = point[2] if len(point) >= 3 else "red"
                
                oval = self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, tags="points")
                self.canvas.tag_bind(oval, "<Button-1>", lambda event, p=point: self.point_clicked(p))
                if len(point) >= 3 and point[2] == "green":
                    bot_points.append(point)

        # Draw the line for bot_current_location points
        if len(bot_current_location_points) >= 2:
            line_points = []
            for point in bot_current_location_points:
                x = point[0] * self.zoom_level + self.canvas.winfo_width() / 2
                y = point[1] * self.zoom_level + self.canvas.winfo_height() / 2
                line_points.append((x, y))

            self.canvas.create_line(line_points, fill="green", width=2, tags="points")

        for point in obstacles:
            x = point[0] * self.zoom_level + self.canvas.winfo_width() / 2
            y = point[1] * self.zoom_level + self.canvas.winfo_height() / 2
            oval = self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black", tags="points")
            self.canvas.tag_bind(oval, "<Button-1>", lambda event, p=point: self.point_clicked(p))


        for point in bot_points:
            x = point[0] * self.zoom_level + self.canvas.winfo_width() / 2
            y = point[1] * self.zoom_level + self.canvas.winfo_height() / 2
            oval = self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="green", tags="points")
            self.canvas.tag_bind(oval, "<Button-1>", lambda event, p=point: self.point_clicked(p))
        for point in survivor_locations:
            x = point[0] * self.zoom_level + self.canvas.winfo_width() / 2
            y = point[1] * self.zoom_level + self.canvas.winfo_height() / 2
            oval = self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red", tags="points")
            self.canvas.tag_bind(oval, "<Button-1>", lambda event, p=point: self.point_clicked(p))

    # def show_popup(self, point):
    #     popup = tk.Toplevel(self.frame)
    #     popup.title("Point Details")

    #     x, y, color = point

    #     if color == "blue":
    #         bot_data = None
    #         for data_point in self.points:
    #             if data_point[:3] == point:  # Compare the x, y, and color
    #                 bot_data = data_point
    #                 break

    #         if bot_data:
    #             label = tk.Label(popup, text=f"Bot Data:\nID: {bot_data[0]}\nX: {bot_data[1]}\nY: {bot_data[2]}")
    #             label.pack(padx=10, pady=10)
    #         else:
    #             label = tk.Label(popup, text="No data available for this point.")
    #             label.pack(padx=10, pady=10)

    #     elif color == "black":
    #         obstacle_data = None
    #         for data_point in self.points:
    #             if data_point[:3] == point:  # Compare the x, y, and color
    #                 obstacle_data = data_point
    #                 break

    #         if obstacle_data:
    #             label = tk.Label(popup, text=f"Obstacle Data:\nID: {obstacle_data[0]}\nRobot ID: {obstacle_data[1]}\nX: {obstacle_data[2]}\nY: {obstacle_data[3]}")
    #             label.pack(padx=10, pady=10)
    #         else:
    #             label = tk.Label(popup, text="No data available for this point.")
    #             label.pack(padx=10, pady=10)

    #     else:
    #         label = tk.Label(popup, text="Unknown point color.")
    #         label.pack(padx=10, pady=10)
    def show_popup(self, point):
        popup = tk.Toplevel(self.frame)
        popup.title("Point Details")

        x, y, color = point

        try:
            connection = psycopg2.connect(
                host="localhost",
                database="resQBot",
                user="postgres",
                port="69",
                password="0000"
            )
            cursor = connection.cursor()

            if color == "blue":
                # Fetch data from the "bot" table based on the clicked point's coordinates
                cursor.execute(f"SELECT * FROM bot WHERE cordx = {x} AND cordy = {y};")
                data = cursor.fetchone()
                if data:
                    label = tk.Label(popup, text=f"Bot Data:\nID: {data[0]}\nX: {data[1]}\nY: {data[2]}")
                    label.pack(padx=10, pady=10)
                else:
                    label = tk.Label(popup, text="No data available for this point.")
                    label.pack(padx=10, pady=10)
            elif color == "red":
                cursor.execute(f"SELECT * FROM survivor_locations WHERE cordx = {x} AND cordy = {y};")
                data = cursor.fetchone()
                if data:
                    label = tk.Label(popup, text=f"Survivor Data:\nID: {data[0]} \nrobotid: {data[1]} \nX: {data[2]}\nY: {data[3]} \n found at: {data[4]}")
                    label.pack(padx=10, pady=10)
                else:
                    label = tk.Label(popup, text="No data available for this point.")
                    label.pack(padx=10, pady=10)
            elif color == "black":
                cursor.execute(f"SELECT * FROM obstacles WHERE cordx = {x} AND cordy = {y};")
                data = cursor.fetchone()
                print(data)
                if data:
                    label = tk.Label(popup, text=f"Obstacle Data:\nID: {data[0]}\n robotid:{data[1]} \nX: {data[2]}\nY: {data[3]}")
                    label.pack(padx=10, pady=10)
                else:
                    label = tk.Label(popup, text="No data available for this point.")
                    label.pack(padx=10, pady=10)
            else:
                label = tk.Label(popup, text="Unknown point color.")
                label.pack(padx=10, pady=10)

        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL database:", e)

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


    def point_clicked(self, point):
        self.show_popup(point)
        print("Clicked point:", point)
        # Add your custom logic here for what should happen when a point is clicked


    def resize_window(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def drag(self, event):
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        self.canvas.move("all", delta_x, delta_y)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def add_point(self, event):
        x = (event.x - self.canvas.winfo_width() / 2) / self.zoom_level
        y = (event.y - self.canvas.winfo_height() / 2) / self.zoom_level
        self.points.append((x, y))
        self.show_points()

    def zoom(self, event):
        if event.delta > 0:
            self.zoom_level *= 1.1
        else:
            self.zoom_level /= 1.1

        self.canvas.scale("all", event.x, event.y, self.zoom_level, self.zoom_level)
        self.show_points()
        self.resize_window(None)

# Usage
root = tk.Tk()

# Create a frame to contain the zoomable window
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Create the zoomable window inside the frame
zoomable_window = ZoomableWindow(frame)

root.mainloop()