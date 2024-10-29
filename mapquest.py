import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import urllib.parse
import requests

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

def reset_start_field():
    start_entry.delete(0, tk.END)

def reset_end_field():
    end_entry.delete(0, tk.END)

def reset_route_details():
    start_entry.delete(0, tk.END)
    end_entry.delete(0, tk.END)
    result_text.set("")

root = tk.Tk()
root.title("Route Finder")

img = Image.open("assets/loc.png")
img = img.resize((150, 150), Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(img)

img_label = tk.Label(root, image=img)
img_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

title_label = tk.Label(root, text="Route Finder Application", font=("Arial", 16, "bold"))
title_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

tk.Label(root, text="Starting Location:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
start_entry = tk.Entry(root)
start_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Button(root, text="Delete Starting Location", command=reset_start_field).grid(row=2, column=2, padx=10, pady=10)

tk.Label(root, text="Destination:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
end_entry = tk.Entry(root)
end_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Button(root, text="Delete Destination", command=reset_end_field).grid(row=3, column=2, padx=10, pady=10)

tk.Button(root, text="Get Directions", command=get_directions).grid(row=4, column=0, columnspan=3, pady=10)

tk.Button(root, text="Reset", command=reset_route_details).grid(row=5, column=0, columnspan=3, pady=10)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, wraplength=400)
result_label.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
