import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
from modules.module1_usage import start_monitor
from modules.module2_privacy import run_scanner
from modules.module3 import run_port_scanner
from modules.module4 import view_logs
from modules.module5_alerts import search_alert
from modules.module6_protect import protect_logs


# ----------------------------- Window -----------------------------

root = tk.Tk()
root.title("Behavioural Threat Monitor System")
root.geometry("1200x700")
root.configure(bg="#1b1b2f")

# ----------------------------- Colors -----------------------------

BG = "#1b1b2f"
SIDE = "#23233a"
GREEN = "#00ff88"

# ----------------------------- Sidebar -----------------------------

sidebar = tk.Frame(root, bg=SIDE, width=240)
sidebar.pack(side="left", fill="y")

# ----------------------------- Main Area -----------------------------

main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True)

# ----------------------------- Heading -----------------------------

heading = tk.Label(
    main,
    text="Behavioural Threat Monitor System",
    font=("Segoe UI", 22, "bold"),
    fg="white",
    bg=BG
)
heading.pack(pady=(20, 5))

subtitle = tk.Label(
    main,
    text="Cybersecurity Monitoring Console",
    font=("Segoe UI", 11),
    fg="lightgray",
    bg=BG
)
subtitle.pack()

# ----------------------------- Status -----------------------------

status = tk.Label(
    main,
    text="Status : Ready",
    fg=GREEN,
    bg=BG,
    font=("Segoe UI", 10, "bold")
)
status.pack(pady=15)

# ----------------------------- Target Input -----------------------------

target_frame = tk.Frame(main, bg=BG)
target_frame.pack(pady=5)

tk.Label(
    target_frame,
    text="Target IP / Domain :",
    bg=BG,
    fg="white",
    font=("Segoe UI", 10, "bold")
).pack(side="left", padx=5)

target_entry = tk.Entry(
    target_frame,
    width=35,
    font=("Segoe UI", 11)
)

target_entry.pack(side="left", padx=5)

# Default value for testing
target_entry.insert(0, "scanme.nmap.org")

# ----------------------------- Search Alert -----------------------------

search_frame = tk.Frame(main, bg=BG)
search_frame.pack(pady=5)

tk.Label(
    search_frame,
    text="Search Alert :",
    bg=BG,
    fg="white",
    font=("Segoe UI",10,"bold")
).pack(side="left", padx=5)

search_entry = tk.Entry(
    search_frame,
    width=35,
    font=("Segoe UI",11)
)

search_entry.pack(side="left", padx=5)

# ----------------------------- Output Box -----------------------------

output = ScrolledText(
    main,
    height=25,
    bg="black",
    fg="#00ff66",
    font=("Consolas", 11)
)

output.pack(fill="both", expand=True, padx=20, pady=10)

# ----------------------------- Log Function -----------------------------

def log(message):
    output.insert(tk.END, message + "\n")
    output.see(tk.END)

# ----------------------------- Usage Monitor -----------------------------

def run_usage():

    try:

        start_monitor(log)

    except Exception as e:

        log(f"\nERROR : {e}")

    status.config(text="Status : Ready")

def usage_monitor():

    output.delete("1.0", tk.END)

    status.config(text="Status : Usage Monitor Running")

    threading.Thread(
        target=run_usage,
        daemon=True
    ).start()

# ----------------------------- Placeholder Functions -----------------------------

def run_privacy():

    run_scanner(log)

    status.config(text="Status : Ready")


def privacy_scanner():

    output.delete("1.0", tk.END)

    status.config(text="Status : Privacy Scanner Running")

    threading.Thread(
        target=run_privacy,
        daemon=True
    ).start()

def run_ports():

    target = target_entry.get().strip()

    if target == "":
        log("Please enter a target IP or domain.")
        status.config(text="Status : Ready")
        return

    run_port_scanner(target, log)

    status.config(text="Status : Ready")


def port_scan():

    output.delete("1.0", tk.END)

    status.config(text="Status : Port Scanner Running")

    threading.Thread(
        target=run_ports,
        daemon=True
    ).start()
    
def run_logs():

    view_logs(log)

    status.config(text="Status : Ready")


def view_logs_btn():

    output.delete("1.0", tk.END)

    status.config(text="Status : Viewing Logs")

    threading.Thread(
        target=run_logs,
        daemon=True
    ).start()

import threading

def run_search():

    keyword = search_entry.get().strip()

    if keyword == "":
        log("Please enter a keyword.")
        return

    search_alert(keyword, log)

    status.config(text="Status : Ready")


def search_alerts():

    output.delete("1.0", tk.END)

    status.config(text="Status : Searching Alerts")

    threading.Thread(
        target=run_search,
        daemon=True
    ).start()

def run_protect():

    protect_logs(log)

    status.config(text="Status : Ready")


def protect_logs_btn():

    output.delete("1.0",tk.END)

    status.config(text="Status : Protecting Logs")

    threading.Thread(
        target=run_protect,
        daemon=True
    ).start()

def about():

    output.delete("1.0", tk.END)

    output.insert(
        tk.END,
"""
Behavioural Threat Monitor System

Features
--------------------------------
-> Usage Monitoring
-> Privacy Scanner
-> Port Scanner
-> Alert Detection
-> Log Protection

"""
    )

# ----------------------------- Sidebar -----------------------------

logo = tk.Label(
    sidebar,
    text="BTMS",
    bg=SIDE,
    fg="cyan",
    font=("Segoe UI", 22, "bold")
)

logo.pack(pady=25)

buttons = [

("Usage Monitor", usage_monitor),
("Privacy Scanner", privacy_scanner),
("Port Scanner", port_scan),
("View Logs",view_logs_btn),
("Search Alerts", search_alerts),
("Protect Logs",protect_logs_btn),
("About", about)

]

for text, command in buttons:

    tk.Button(
        sidebar,
        text=text,
        command=command,
        bg="#303050",
        fg="white",
        relief="flat",
        font=("Segoe UI", 11),
        width=20,
        pady=8
    ).pack(pady=8)

# ----------------------------- Exit -----------------------------

tk.Button(
    sidebar,
    text="Exit",
    command=root.destroy,
    bg="#d9534f",
    fg="white",
    relief="flat",
    font=("Segoe UI", 11),
    width=20,
    pady=8
).pack(side="bottom", pady=25)

# ----------------------------- Start GUI -----------------------------

root.mainloop()
