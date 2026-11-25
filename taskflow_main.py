"""Taskflow is a software with gui to keep track of the tasks and their deadlines,
it provides urgency status, completion status,task name, deadline .
Date-25-11-2026, a day before my python sem exam for 3rd sem. Its just a 
fun project to make learning more engaging!"""


# Imports
import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import datetime as dt


# csv
filename = "tasks.csv"

if os.path.exists(filename):
    tasks = pd.read_csv(filename)
else:
    tasks = pd.DataFrame(columns=["Task ID", "Task Name", "Start Date", "Deadline", "Status"])
    tasks.to_csv(filename, index=False)


def add_task(task_name, start_date, deadline):
    global tasks

    if tasks.empty:
        task_id = 1
    else:
        task_id = int(tasks["Task ID"].max()) + 1

    task = {"Task ID": task_id,"Task Name": task_name,"Start Date": start_date,"Deadline": deadline,"Status": "Pending"}
    new_task = pd.DataFrame([task])
    tasks = pd.concat([tasks, new_task], ignore_index=True)
    tasks.to_csv(filename, index=False)


def delete_task(task_id):
    global tasks
    tasks = tasks[tasks["Task ID"] != task_id]
    tasks.to_csv(filename, index=False)


def task_status(task_id):
    global tasks
    tasks.loc[tasks["Task ID"] == task_id, "Status"] = "Completed"
    tasks.to_csv(filename, index=False)


def calculate_urgency(task_id):
    selected_task = tasks.loc[tasks["Task ID"] == task_id]
    if selected_task.empty:
        return "Unknown"
    status = selected_task["Status"].iloc[0]
    if status == "Completed":
        return "Completed"
    deadline = selected_task["Deadline"].iloc[0]
    deadline_date = dt.datetime.strptime(deadline, "%d-%m-%Y").date()
    today = dt.date.today()
    remaining = (deadline_date - today).days
    if remaining <= 1:
        return "Urgent"
    elif remaining <= 5:
        return "Soon"
    else:
        return "Later"


#gui callback functions

def refresh_tasks():
    task_list.delete(0, tk.END)

    for _ , row in tasks.iterrows():
        task_id = int(row["Task ID"])
        urgency = calculate_urgency(task_id)

        display = (f"{task_id} \t {row["Task Name"]} \t {row["Deadline"]} \t  {row["Status"]} \t {urgency}")
        task_list.insert(tk.END, display)


def add_task_gui():
    name = task_name.get().strip()
    start_date = Start_date.get().strip()
    deadline = DeadLine.get().strip()

    if not name or not start_date or not deadline:
        messagebox.showwarning("Missing Information", "Please fill in all fields.")
        return

    try:
        start = dt.datetime.strptime(start_date, "%d-%m-%Y").date()
        end = dt.datetime.strptime(deadline, "%d-%m-%Y").date()
    except ValueError:
        messagebox.showerror(
            "Invalid Date",
            "Enter dates in DD-MM-YYYY format."
        )
        return

    if end < start:
        messagebox.showerror(
            "Invalid Deadline",
            "Deadline cannot be earlier than the start date."
        )
        return

    add_task(name, start_date, deadline)

    task_name.set("")
    Start_date.set("")
    DeadLine.set("")

    refresh_tasks()


def get_selected_task_id():
    selection = task_list.curselection()

    if not selection:
        messagebox.showwarning("No Selection", "Please select a task first.")
        return None

    # Listbox position corresponds to dataframe row position
    index = selection[0]
    return int(tasks.iloc[index]["Task ID"])


def delete_selected_task():
    task_id = get_selected_task_id()

    if task_id is not None:
        delete_task(task_id)
        refresh_tasks()


def complete_selected_task():
    task_id = get_selected_task_id()

    if task_id is not None:
        task_status(task_id)
        refresh_tasks()


#gui


#screen
root = tk.Tk()
root.state("zoomed")
root.title("TaskFlow")

# Variables
task_name = tk.StringVar()
Start_date = tk.StringVar()
DeadLine = tk.StringVar()


# input frame
input_frame = tk.Frame(root,padx=20,pady=20)
input_frame.pack()

# task name
tk.Label(input_frame, text="Task Name").grid(row=0,column=0,padx=5)
tk.Entry(input_frame, textvariable=task_name, width=25).grid(row=0,column=1, padx=5)

# start date
tk.Label(input_frame, text="Start Date").grid(row=0,column=2, padx=5)
tk.Entry(input_frame, textvariable=Start_date, width=15).grid(row=0,column=3,padx=5)

# Deadline
tk.Label(input_frame, text="Deadline").grid(row=0, column=4,padx=5)
tk.Entry(input_frame, textvariable=DeadLine, width=15).grid(row=0,column=5,padx=5)

# add button
tk.Button(root,text="Add Task",command=add_task_gui).pack(pady=10)

# task display
tk.Label(root,text="YOUR TASKS",font=("Arial", 16, "bold")).pack(pady=10)

task_list = tk.Listbox(root, width=100, height=20, font=("Arial", 11))
task_list.pack(pady=10)

# action buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame,text="Mark Completed",command=complete_selected_task).grid(row=0, column=0, padx=10)

tk.Button(button_frame,text="Delete Task",command=delete_selected_task).grid(row=0, column=1, padx=10)

# load existing tasks when the application starts
refresh_tasks()

root.mainloop()
