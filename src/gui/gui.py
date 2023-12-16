import tkinter as tk
import map
import exportDB
import vlc

class GUI:
    def __init__(self,topics,client):
        self.topics = topics
        self.client=client
        self.window= tk.Tk()
        self.instance = vlc.Instance("--no-xlib","--video-filter=transform", "--transform-type=180")
        self.player = self.instance.media_player_new()

    def send_forward(self, event):
        self.client.publish(self.topics.commands['motor']['manual_controls'], "forward")

    def send_backward(self, event):
        self.client.publish(self.topics.commands['motor']['manual_controls'], "backward")

    def send_left(self, event):
        self.client.publish(self.topics.commands['motor']['manual_controls'], "left")

    def send_right(self, event):
        self.client.publish(self.topics.commands['motor']['manual_controls'], "right")

    def send_stop(self, event):
        self.client.publish(self.topics.commands['motor']['manual_controls'], "stop")


    def show_control_screen(self):
        manual_frame.pack(side=tk.BOTTOM, pady=10)
        map_frame.pack_forget()
        camera_frame.pack_forget()

    def show_map_screen(self):
        manual_frame.pack_forget()
        map_frame.pack()
        camera_frame.pack_forget()
        map_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        # Create an instance of the ZoomableWindow class and pass the map_frame as the parent frame
        


    def show_camera_screen(self):
        manual_frame.pack_forget()
        map_frame.pack_forget()
        camera_frame.pack()

    def on_closing(self):
        self.player.stop()
        self.window.destroy()

    def create_window(self):
        global manual_frame, map_frame, camera_frame
        self.window.title("Disaster Bot")
        self.window.geometry("1000x600")
        self.window.configure(bg="#E6E6E6")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        button_style = {
            "font": ("Arial", 11),
            "width": 10,
            "height": 2,
            "bd": 0,
            "padx": 5,
            "pady": 5,
            "bg": "#333333",
            "fg": "white",
            "activebackground": "#CCCCCC",
            "highlightbackground": "#CCCCCC",
            "highlightcolor": "#CCCCCC",
            "highlightthickness": 2,
            "relief": "solid",
            "borderwidth": 0,
        }

        manual_frame = tk.Frame(self.window, bg="#E6E6E6")
        map_frame = tk.Frame(self.window, bg="#E6E6E6")
        camera_frame = tk.Frame(self.window, bg="#E6E6E6")
        
        self.window.bind('<Left>', self.send_left)
        self.window.bind('<Right>', self.send_right)
        self.window.bind('<Up>', self.send_forward)
        self.window.bind('<Down>', self.send_backward)
        self.window.bind('<space>', self.send_stop)

        # Header
        header_frame = tk.Frame(self.window, bg="#222222", pady=10)
        header_frame.pack(side=tk.TOP, fill=tk.X)

        label = tk.Label(header_frame, text="Res Q Bot", fg="white", font=("Arial", 20), bg="#222222")
        map_button = tk.Button(header_frame, text="Map", **button_style, command=self.show_map_screen)
        camera_button = tk.Button(header_frame, text="Camera", **button_style, command=self.show_camera_screen)
        manual_control_button = tk.Button(
            header_frame, text="Manual Control", **button_style, command=self.show_control_screen
        )

        label.pack(side=tk.LEFT, padx=5, pady=5)
        map_button.pack(side=tk.RIGHT, padx=5)
        camera_button.pack(side=tk.RIGHT, padx=5)
        manual_control_button.pack(side=tk.RIGHT, padx=5)

        # Main frame

        # Manual control frame
        manual_frame.pack(side=tk.BOTTOM, pady=10)

        forward_button = tk.Button(manual_frame, text="Forward", **button_style)
        forward_button.bind("<ButtonPress>", self.send_forward)
        forward_button.bind("<ButtonRelease>", self.send_stop)

        backward_button = tk.Button(manual_frame, text="Backward", **button_style)
        backward_button.bind("<ButtonPress>", self.send_backward)
        backward_button.bind("<ButtonRelease>", self.send_stop)

        left_button = tk.Button(manual_frame, text="Left", **button_style)
        left_button.bind("<ButtonPress>", self.send_left)
        left_button.bind("<ButtonRelease>", self.send_stop)

        right_button = tk.Button(manual_frame, text="Right", **button_style)
        right_button.bind("<ButtonPress>", self.send_right)
        right_button.bind("<ButtonRelease>", self.send_stop)

        # Grid layout configuration
        forward_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        left_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        backward_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        right_button.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

        # Grid row configuration
        manual_frame.grid_rowconfigure(0, weight=1)
        manual_frame.grid_rowconfigure(1, weight=1)

        #map
        Zoomable_Window=map.ZoomableWindow(map_frame)
        #db exporting to ec2
        export_db = tk.Button(map_frame, text="Export data",command=exportDB.check_internet)
        export_db.pack(side="bottom", pady=10, padx=5)

        #text-to-speech
        text_box = tk.Text(camera_frame, width=50, height=2)
        text_box.grid(row=1, column=1, padx=5, pady=10)

        save_button = tk.Button(camera_frame, text="Send Text", command=lambda: self.client.publish(self.topics.commands['text']['tts'],text_box.get("1.0", "end-1c") ),**button_style)
        save_button.grid(row=1, column=2, padx=5, pady=10)

        


        # Calculate the position to center the frame
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        frame_width = 1000
        frame_height = 600
        x = (screen_width - frame_width) // 2
        y = (screen_height - frame_height) // 2
        camera_frame = tk.Frame(width=frame_width, height=frame_height)
        media = self.instance.media_new("tcp/h264://192.168.45.2:8888/")
        self.player.set_media(media)
        self.player.set_hwnd(camera_frame.winfo_id())
        self.player.play()
        self.window.mainloop()

