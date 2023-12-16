import socket
import subprocess
from tkinter import messagebox

def check_internet():
    try:
        # Attempt to connect to a well-known host (google.com)
        socket.create_connection(("www.google.com", 80))
        # Execute the bash script when the internet is available
        subprocess.call(["bash", "src\db\export.sh"])
    except socket.error:
        messagebox.showwarning("Internet Status", "Device is not connected to the internet.")

# # Create the Tkinter window
# window = tk.Tk()
# window.title("Internet Check")
# window.geometry("200x100")

# # Create the button
# button = tk.Button(window, text="Internet Check ", command=check_internet)
# button.pack(pady=20)

# # Start the Tkinter event loop
# window.mainloop()
