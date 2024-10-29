import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Importing from Pillow
import urllib.parse
import requests


# Function to fetch directions
def get_directions():
    orig = start_entry.get()
    dest = end_entry.get()
    if orig == "" or dest == "":
        messagebox.showerror("Error", "Please enter both starting and destination locations.")
        return

    main_api = "https://www.mapquestapi.com/directions/v2/route?"
    key = "XlboADR9h2O15DJGzL9V2jXvWlSz13CQ"
    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        result_text.set(f"Directions from {orig} to {dest}\n"
                        f"Trip Duration: {json_data['route']['formattedTime']}\n"
                        f"Kilometers: {json_data['route']['distance'] * 1.61:.2f} km\n"
                        f"Fuel Used (Ltr): {json_data['route'].get('fuelUsed', 'None')}\n")
        directions = "\n".join([f"{each['narrative']} ({each['distance'] * 1.61:.2f} km)"
                                for each in json_data['route']['legs'][0]['maneuvers']])
        result_text.set(result_text.get() + "\n" + directions)
    else:
        messagebox.showerror("Error", f"Status Code: {json_status}. Something went wrong.")


# Function to reset the starting location field
def reset_start_field():
    start_entry.delete(0, tk.END)


# Function to reset the destination field
def reset_end_field():
    end_entry.delete(0, tk.END)


# Create the main window
root = tk.Tk()
root.title("Route Finder")

# Load and resize the image using Pillow
img = Image.open("assets/images/loc.png")
img = img.resize((150, 150), Image.Resampling.LANCZOS)  # Resizing the image (width, height)
img = ImageTk.PhotoImage(img)

# Place the image at the top and center it
img_label = tk.Label(root, image=img)
img_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Create and place the input fields and labels
tk.Label(root, text="Starting Location:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
start_entry = tk.Entry(root)
start_entry.grid(row=1, column=1, padx=10, pady=10)

# Button to reset the starting location field
tk.Button(root, text="Reset Starting Location", command=reset_start_field).grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Destination:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
end_entry = tk.Entry(root)
end_entry.grid(row=2, column=1, padx=10, pady=10)

# Button to reset the destination field
tk.Button(root, text="Reset Destination", command=reset_end_field).grid(row=2, column=2, padx=10, pady=10)

# Button to get directions
tk.Button(root, text="Get Directions", command=get_directions).grid(row=3, column=0, columnspan=3, pady=10)

# Text widget to display results
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, wraplength=400)
result_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
