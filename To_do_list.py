import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading
import time

# Set up the main app window
root = tk.Tk()
root.title("To-Do List")
root.geometry("400x600")
root.configure(bg="#1E1E1E")  # Dark background

tasks = []
reminders = {}

# Load tasks from file
def load_tasks():
    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                tasks.append(line.strip())
    except FileNotFoundError:
        pass

# Save tasks to file
def save_tasks():
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(task + "\n")

# Add a new task
def add_task():
    task = entry.get()
    if task:
        tasks.append(task)
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

# Delete selected task
def delete_task():
    try:
        task_index = listbox.curselection()[0]
        tasks.pop(task_index)
        listbox.delete(task_index)
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to delete.")

# Mark task as done
def mark_done():
    try:
        task_index = listbox.curselection()[0]
        task = tasks[task_index]
        tasks[task_index] = task + " ✔" if "✔" not in task else task.replace(" ✔", "")
        listbox.delete(task_index)
        listbox.insert(task_index, tasks[task_index])
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to mark as done.")

# Clear all completed tasks
def clear_completed():
    global tasks
    tasks = [task for task in tasks if "✔" not in task]
    listbox.delete(0, tk.END)
    for task in tasks:
        listbox.insert(tk.END, task)
    save_tasks()

# Sort tasks, moving completed tasks to the bottom
def sort_tasks():
    tasks.sort(key=lambda x: "✔" in x)
    listbox.delete(0, tk.END)
    for task in tasks:
        listbox.insert(tk.END, task)
    save_tasks()

# Set a reminder for a specific task
def set_reminder():
    try:
        task_index = listbox.curselection()[0]
        task = tasks[task_index]
        date_str = date_entry.get()
        time_str = time_entry.get()
        
        # Convert the date and time to a datetime object
        try:
            reminder_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            reminders[task] = reminder_dt
            date_entry.delete(0, tk.END)
            time_entry.delete(0, tk.END)
            messagebox.showinfo("Reminder Set", f"Reminder set for {task} at {reminder_dt}")
        except ValueError:
            messagebox.showwarning("Invalid Format", "Enter date as YYYY-MM-DD and time as HH:MM")
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to set a reminder.")

# Check reminders every minute
def check_reminders():
    while True:
        now = datetime.now()
        for task, reminder_time in list(reminders.items()):
            if now >= reminder_time:
                messagebox.showinfo("Reminder", f"Reminder: {task}")
                del reminders[task]
        time.sleep(60)

# Start the reminder thread
reminder_thread = threading.Thread(target=check_reminders, daemon=True)
reminder_thread.start()

# UI setup
frame = tk.Frame(root, bg="#1E1E1E")
frame.pack(pady=10)

# Title label
title = tk.Label(frame, text="Tasks", font=("Arial", 24), bg="#1E1E1E", fg="blue")
title.pack(pady=10)

# Listbox to display tasks
listbox = tk.Listbox(frame, width=40, height=15, font=("Arial", 14), bg="#252526", fg="white", selectbackground="#3B3B3B", bd=0)
listbox.pack(pady=10)

# Entry field for adding new tasks
entry_label = tk.Label(root, text="Add an activity:", font=("Arial", 12), bg="#1E1E1E", fg="white")
entry_label.pack(pady=(10, 0))
entry = tk.Entry(root, width=35, font=("Arial", 14), bg="#252526", fg="white", insertbackground="white", bd=0)
entry.pack(pady=5)

# Labels and entries for date and time
date_label = tk.Label(root, text="Reminder Date (YYYY-MM-DD)", font=("Arial", 12), bg="#1E1E1E", fg="white")
date_label.pack(pady=(10, 0))
date_entry = tk.Entry(root, width=35, font=("Arial", 14), bg="#252526", fg="white", insertbackground="white", bd=0)
date_entry.pack(pady=5)

time_label = tk.Label(root, text="Reminder Time (HH:MM)", font=("Arial", 12), bg="#1E1E1E", fg="white")
time_label.pack(pady=(10, 0))
time_entry = tk.Entry(root, width=35, font=("Arial", 14), bg="#252526", fg="white", insertbackground="white", bd=0)
time_entry.pack(pady=5)

# Define styles for ttk buttons
style = ttk.Style()
style.theme_use("default")
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("Add.TButton", background="#FFFFFF", foreground="#000000")
style.configure("Done.TButton", background="#00FF00", foreground="#000000")
style.configure("Delete.TButton", background="#FF0000", foreground="#000000")

# Buttons for task actions
button_frame = tk.Frame(root, bg="#1E1E1E")
button_frame.pack(pady=5)

add_button = ttk.Button(button_frame, text="Add Task", style="Add.TButton", command=add_task)
add_button.grid(row=0, column=0, padx=5)

done_button = ttk.Button(button_frame, text="Mark Done", style="Done.TButton", command=mark_done)
done_button.grid(row=0, column=1, padx=5)

delete_button = ttk.Button(button_frame, text="Delete Task", style="Delete.TButton", command=delete_task)
delete_button.grid(row=0, column=2, padx=5)

# Frame for "Clear Completed", "Sort Tasks", and "Set Reminder" on the same row
bottom_button_frame = tk.Frame(root, bg="#1E1E1E")
bottom_button_frame.pack(pady=10)

clear_button = ttk.Button(bottom_button_frame, text="Clear Completed", style="TButton", command=clear_completed)
clear_button.grid(row=0, column=0, padx=10)

sort_button = ttk.Button(bottom_button_frame, text="Sort Tasks", style="TButton", command=sort_tasks)
sort_button.grid(row=0, column=1, padx=10)

reminder_button = ttk.Button(bottom_button_frame, text="Set Reminder", style="TButton", command=set_reminder)
reminder_button.grid(row=0, column=2, padx=10)

# Load tasks and populate the listbox
load_tasks()
for task in tasks:
    listbox.insert(tk.END, task)

root.mainloop()
