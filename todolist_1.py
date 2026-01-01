import tkinter as tk
# import customtkinter as tk
from tkinter import messagebox
import mysql.connector

# Function to connect to the database
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Admin@2205',
        database='todo_db'
    )

# Function to add a new task
def add_task():
    task = task_entry.get()
    if task:
        cnx = create_connection()
        cursor = cnx.cursor()
        cursor.execute('INSERT INTO tasks (task) VALUES (%s)', (task,))
        cnx.commit()
        cursor.close()
        cnx.close()
        task_entry.delete(0, tk.END)
        populate_tasks()
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

# Function to populate tasks from the database
def populate_tasks():
    task_list.delete(0, tk.END)
    cnx = create_connection()
    cursor = cnx.cursor()
    cursor.execute('SELECT id, task FROM tasks WHERE completed = 0') 
    for task_id, task in cursor.fetchall():
        task_list.insert(tk.END, f'{task_id}: {task}')
    cursor.close()
    cnx.close()

def view_completed_tasks():
    completed_window = tk.Toplevel(root)
    completed_window.title("Completed Tasks")
    completed_window.geometry("300x300")
    completed_list = tk.Listbox(completed_window, width=50)
    completed_list.pack(pady=10)
    cnx = create_connection()
    cursor = cnx.cursor()
    cursor.execute('SELECT id, task FROM tasks WHERE completed = 1') 
    for task_id, task in cursor.fetchall():
        completed_list.insert(tk.END, f'{task_id}: {task}')
    cursor.close()
    cnx.close()


# Function to delete a task
def delete_task():
    selected_task = task_list.curselection()
    if selected_task:
        task_text = task_list.get(selected_task)
        task_id = task_text.split(':')[0]
        cnx = create_connection()
        cursor = cnx.cursor()
        cursor.execute('UPDATE tasks SET completed = 1 WHERE id = %s', (task_id,))        
        cnx.commit()
        cursor.close()
        cnx.close()
        populate_tasks()
    else:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

# Function to open the To-Do List App
def open_todo_app():
    welcome_window.destroy()  # Close welcome screen
    global root  # Define the main app window
    root = tk.Tk()
    root.title("To-Do List")
    root.geometry("500x400")
    root.configure(bg='#e6f2ff')

    # Entry field for a new task
    global task_entry
    task_entry = tk.Entry(root, width=50, bg='#ffffff', fg='#000000')
    task_entry.insert(0, "Enter your task here...")
    task_entry.bind("<FocusIn>", lambda event: task_entry.delete(0, tk.END) if task_entry.get() == "Enter your task here..." else None)
    task_entry.bind("<FocusOut>", lambda event: task_entry.insert(0, "Enter your task here...") if task_entry.get() == "" else None)
    task_entry.pack(pady=10)


    # Button to add a task
    add_task_button = tk.Button(root, text="Add Task", command=add_task, bg='#4CAF50', fg='white')
    add_task_button.pack(pady=10)

    #Completed Task Button
    view_completed_button = tk.Button(root, text="View Completed Tasks", command=view_completed_tasks, bg='#FFA500')
    view_completed_button.pack(pady=5)

    # Listbox to display tasks
    global task_list
    task_list = tk.Listbox(root, width=50)
    task_list.pack(pady=5)

    # Button to delete a task
    delete_task_button = tk.Button(root, text="Delete Task", command=delete_task)
    delete_task_button.pack(pady=5)

    # Populate tasks on startup
    populate_tasks()

    root.mainloop()

# Welcome Page
welcome_window = tk.Tk()
welcome_window.title("Welcome")
welcome_window.geometry("400x300")
# welcome_window.configure(bg="#ffcccb")

# Welcome Label
bg_image = tk.PhotoImage(file="Untitled design (2).png")  # Make sure it's a PNG file
bg_label = tk.Label(welcome_window, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Add a welcome label for text separately
welcome_label = tk.Label(welcome_window, text="Welcome to the To-Do List Application!", font=("Arial", 14,"bold"),bg="yellow")
welcome_label.pack(pady=20)
welcome_label2=tk.Label(welcome_window, text="""Description to use this:\n ➤Add a Task: Type your task and click "Add Task"To save it".\n ➤View Tasks: Your tasks will be listed below after adding.\n  ➤Delete a Task: Select a task and click "Delete Task" to remove it""")
welcome_label2.pack(pady=40)
#Operating To Do List


# Next Button to Open To-Do List App
next_button = tk.Button(welcome_window, text="Next", command=open_todo_app, bg="#4CAF50", fg="white")
next_button.pack(pady=20)

welcome_window.mainloop()
