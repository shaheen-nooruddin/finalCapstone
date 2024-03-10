import os 
from datetime import datetime
import logging

def load_tasks():
    """
    Load tasks from the tasks file and return them as a list of dictionaries.

    Returns:
        list: A list of dictionaries containing task information.
    """
    tasks = []

    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                if line.strip():  # Check if the line is not empty
                    task_data = line.strip().split(";")
                    logging.debug("Task data read from file: %s", task_data)
                    task = {
                        "username": task_data[0],
                        "description": task_data[1],
                        "assigned_to": task_data[2],
                        "due_date": datetime.strptime(task_data[3], "%Y-%m-%d"),
                        "date_assigned": datetime.strptime(task_data[4], "%Y-%m-%d"),
                        "completed": task_data[5]
                    }
                    tasks.append(task)
    except FileNotFoundError:
        logging.error("Tasks file not found.")
    except Exception as e:
        logging.error("Error loading tasks: %s", e)

    return tasks

def load_users():
    """
    Load users from the user file and return them as a dictionary of usernames and passwords.
    
    Returns:
        dict: A dictionary containing usernames as keys and passwords as values.
    """
    users = {}
    try:
        with open("user.txt", "r") as user_file:
            for line in user_file:
                # Skip empty lines
                if not line.strip():
                    continue

                # Split the line by semicolon (;) and expect two values
                parts = line.strip().split(';')
                if len(parts) == 2:
                    username, password = parts
                    users[username] = password
                else:
                    print(f"Ignoring line: {line.strip()}. Expected format: username;password")
    except FileNotFoundError:
        print("User file not found.")
    except Exception as e:
        print("Error loading users:", e)
    return users


def authenticate_user(users):
    """
    Authenticate users by prompting for username and password.

    Args:
        users (dict): A dictionary containing usernames and passwords.

    Returns:
        str: The authenticated username if successful, None otherwise.
    """
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username in users and users[username] == password:
        return username
    elif username == 'admin' and password == 'password':  # Add condition for admin login
        return 'admin'
    else:
        print("Invalid username or password.")
        return None


def generate_files():
    """
    Checks if task and user files exist and create them if not.
    """
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as tasks_file:
            # Write initial content if needed
            pass

    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as user_file:
            # Write initial content if needed
            pass


def reg_user(current_user):
    """
    Register a new user by providing a username and password.
    param current_user: The username of the current user. Only 'admin' can register new users.
    """
    if current_user != 'admin':  # Check if the current user is not admin
        print("Only admin can register new users.")
        return

    while True:
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        if username == '' or password == '':
            print("Username and password cannot be empty. Please try again.")
            continue

        users = load_users()  # Load existing users
        if username in users:
            print("Username already exists. Please try a different username.")
            continue

        # If the username is unique, add the user to the file
        with open("user.txt", "a") as user_file:
            user_file.write(f"{username};{password}\n")
        print("User registered successfully.")
        break


def add_task():
    """
    Add a new task to the tasks file.
    """
    username = input("Enter username: ")
    description = input("Enter task description: ")
    assigned_to = input("Enter assigned user: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    try:
        datetime.strptime(due_date, "%Y-%m-%d")  # Validate due date format
        with open("tasks.txt", "a") as tasks_file:
            tasks_file.write(f"{username};{description};{assigned_to};{due_date};{datetime.now().strftime('%Y-%m-%d')};No\n")
        print("Task added successfully.")
    except ValueError:
        print("Invalid due date format. Please use YYYY-MM-DD.")


def view_all():
    """
    Function to display all tasks.
    Loads tasks from the file and prints each task.
    """
    tasks = load_tasks()
    for task in tasks:
        print(task)


def view_mine(username):
    """
    Function to display tasks assigned to the current user.
    param username: The username of the current user.
    """
    with open("tasks.txt", "r") as file:
        tasks = file.readlines()

    print("\nYour Tasks:")
    
    for index, task in enumerate(tasks, start=1):
        task_details = task.strip().split(";")
        print("Task details:", task_details)
        
        if task_details[0] == username:
            print(f"{index}. Task details:")
            print(f"   - Assigned to: {task_details[2]}")
            print(f"   - Description: {task_details[1]}")
            print(f"   - Start Date: {task_details[3]}")
            print(f"   - Due Date: {task_details[4]}")
            print(f"   - Completed: {task_details[5]}")
                      
    task_index = input("\nEnter the number of the task to edit or mark as complete (-1 to return): ").strip()

    try:
        task_index = int(task_index)
        if task_index == -1:
            return

        task_index -= 1
        task_details = tasks[task_index].strip().split(";")
        if task_details[-1] == "Yes":
            print("This task has already been completed and cannot be edited.")
            return

        edit_choice = input("Do you want to mark this task as complete (Y/N) or edit (E)? ").strip().lower()
        if edit_choice == 'y':
            task_details[-1] = "Yes"
            tasks[task_index] = ";".join(task_details) + "\n"
            with open("tasks.txt", "w") as file:
                file.writelines(tasks)
            print("Task marked as complete.")
        elif edit_choice == 'e':
            new_username = input("Enter the new username for the task: ").strip()
            new_due_date = input("Enter the new due date for the task (format: YYYY-MM-DD): ").strip()
            task_details[0] = new_username
            task_details[3] = new_due_date
            tasks[task_index] = ";".join(task_details) + "\n"
            with open("tasks.txt", "w") as file:
                file.writelines(tasks)
            print("Task edited successfully.")
        else:
            print("Invalid choice.")

    except ValueError:
        print("Invalid input. Please enter a valid task number.")


def generate_task_overview(username):
    """
    Function to generate an overview of tasks.
    param username: The username of the current user.
    """
    if username != "admin":
        print("You are not authorized to access this function.")
        return

    tasks = load_tasks()
    total_tasks = len(tasks)
    if total_tasks == 0:
        print("No tasks found.")
        return

    completed_tasks = sum(1 for task in tasks if task["completed"] == "Yes")
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in tasks if task["due_date"] < datetime.datetime.now() and task["completed"] == "No")

    with open("task_overview.txt", "w") as file:  # Open file for writing
        file.write("Task Overview:\n")
        file.write(f"Total tasks: {total_tasks}\n")
        file.write(f"Completed tasks: {completed_tasks}\n")
        file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        file.write(f"Overdue tasks: {overdue_tasks}\n")
        file.write(f"Percentage of completed tasks: {(completed_tasks / total_tasks) * 100:.2f}%\n")
        file.write(f"Percentage of uncompleted tasks: {(uncompleted_tasks / total_tasks) * 100:.2f}%\n")
        file.write(f"Percentage of overdue tasks: {(overdue_tasks / total_tasks) * 100:.2f}%\n")

    print("Task overview generated and saved successfully.")


def generate_user_overview(username):
    """
    Function to generate an overview of users.
    param username: The username of the current user.
    """

    if username != "admin":
        print("You are not authorized to access this function.")
        return

    tasks = load_tasks()
    users = load_users()
    total_users = len(users)
    total_tasks = len(tasks)
    user_tasks = {username: sum(1 for task in tasks if task["assigned_to"] == username) for username in users}
    user_completed_tasks = {username: sum(1 for task in tasks if task["assigned_to"] == username and task["completed"] == "Yes") for username in users}
    user_incomplete_tasks = {username: user_tasks[username] - user_completed_tasks.get(username, 0) for username in users}
    user_overdue_tasks = {username: sum(1 for task in tasks if task["assigned_to"] == username and task["due_date"] < datetime.datetime.now() and task["completed"] == "No") for username in users}

    with open("user_overview.txt", "w") as file:  # Open file for writing
        file.write("User Overview:\n")
        file.write(f"Total users: {total_users}\n")
        file.write(f"Total tasks: {total_tasks}\n")
        for username in users:     # Iterating through username in users
            total_user_tasks = user_tasks.get(username, 0)
            if total_user_tasks == 0:
                file.write(f"User: {username}\n")
                file.write("No tasks assigned to this user.\n")
                continue
            file.write(f"User: {username}\n")
            file.write(f"Total tasks assigned: {total_user_tasks}\n")
            file.write(f"Percentage of total tasks assigned: {(total_user_tasks / total_tasks) * 100:.2f}%\n")
            file.write(f"Percentage of completed tasks: {(user_completed_tasks.get(username, 0) / total_user_tasks) * 100:.2f}%\n")
            file.write(f"Percentage of incomplete tasks: {(user_incomplete_tasks.get(username, 0) / total_user_tasks) * 100:.2f}%\n")
            file.write(f"Percentage of overdue tasks: {(user_overdue_tasks.get(username, 0) / total_user_tasks) * 100:.2f}%\n")

    print("User overview generated and saved successfully.")



def generate_reports(username):
    
    # Code to generate tasks.txt and user.txt

    print("Generating reports...")
    with open("tasks.txt", "w") as tasks_file:
        tasks_file.write("admin;Add functionality to task manager;Add additional options and refactor the code.;2022-12-01;2022-11-22;No\n")
        tasks_file.write("admin;working on lists;Lizzy;2024-02-14;2024-03-01;Yes\n")
        tasks_file.write("admin;working on strings;Jack;2024-02-17;2024-03-01;Yes\n")
        tasks_file.write("admin;workin on dicts;Charlie;2024-02-19;2024-03-01;Yes\n")
        tasks_file.write("admin;working on math functions;Bob;2024-02-29;2024-03-06;No\n")
        tasks_file.write("admin;working on tuples;Jenny;2024-02-11;2024-03-06;Yes\n")
        tasks_file.write("admin;working on string manipulations;Sophie;2024-02-10;2024-03-06;No\n")
        tasks_file.write("Bob;working on quadrants;Sophie;2024-02-03;2024-03-07;No\n")
        tasks_file.write("admin;working on error handling;Sam;2024-02-05;2024-03-07;Yes\n")

def display_statistics(username, is_admin):
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports()
    
    if is_admin:
        # Read and display statistics
        with open("task_overview.txt", "r") as tasks_file:
            tasks_data = tasks_file.readlines()
        
        
        # Display statistics
        print("Tasks data:")
        for task in tasks_data:
            print(task.strip())
        
        with open("user_overview.txt", "r") as tasks_file:
            tasks_data = tasks_file.readlines() 
        
        print("Users data:")
        for task in tasks_data:
            print(task.strip())       
    else:
        print("You don't have permission to view statistics.")

# Example usage:
username = "admin"
is_admin = True  # Assuming the user is an admin

display_statistics(username, is_admin)

def parse_task(task_str):
    """
    Function to parse a task string into a dictionary.
    param task_str: String representing a task.
    return: Dictionary representing the task.
    """
    task_fields = task_str.strip().split(';')
    return {
        'task_name': task_fields[1],
        'completed': task_fields[-1] == 'Yes'
    }

    
def main():

    """
    Main function to run the task manager program.
    """
    users = load_users()  # Load existing users
    tasks = load_tasks()  # Load existing tasks

    while True:
        print("\nMain Menu:")
        print("l. Login")
        print("e. Exit")
        choice = input("Enter your choice: ").strip().lower()  # Ensures uniformity in input handling
        print("DEBUG: User input:", choice)  # Debug print statement

        if choice == 'l':  # Login
            username = authenticate_user(users)
            if username:
                print(f"Welcome, {username}!")
                # Present extended menu if logged in successfully
                if username == 'admin':
                    admin_menu(username,users, tasks)  # Pass tasks to admin menu
                else:
                    user_menu(username, tasks)  # Pass tasks to user menu
        
        elif choice == 'e':  # Exit
            exit()
        else:
            print("Invalid choice. Please try again.")


def user_menu(username, tasks):   # Accept tasks parameter
    
    """
    Function to display the user menu.
    param username: The username of the current user.
    param tasks: List of tasks.
    """
      
    while True:
        print("\nUser Menu:")
        print("r. Register User")
        print("a. Add Task")
        print("va. View All Tasks")
        print("vm. View My Tasks")
        print("ds. Display Statistics")  
        print("e. Exit")
        choice = input("Enter your choice: ").lower()

        if choice == 'r':  # Register (Only for Admin)
            print("Sorry, only admin can register new users.")
        elif choice == 'a':  # Add Task
            add_task()
        elif choice == 'va':  # View All Tasks
            view_all()
        elif choice == 'vm':  # View My Tasks
            view_mine(username)
        elif choice == 'ds':  # Display Statistics
            display_statistics(username,tasks)  
        elif choice == 'e':  # Exit
            return
        else:
            print("Invalid choice. Please try again.")

def admin_menu(username,users,tasks): # Accept tasks parameter
    
    """
    Function to display the admin menu.
    param users: List of all users.
    param username: The username of the current user.
    param tasks: List of tasks.
    """                                          
    while True:
        print("\nAdmin Menu:")
        print("a. Add Task")
        print("r. Register User") 
        print("va. View All Tasks")
        print("vm. View My Tasks")
        print("gr. Generate Reports")
        print("ds. Display Statistics")
        print("e. Exit")
        choice = input("Enter your choice: ").lower()

        if choice == 'a':  # Add Task
            add_task()
        elif choice == 'r':  # Register User
            if username == 'admin':  # Check if the user is admin
                reg_user(username)  # Pass the username to register user function
            else:
                print("Only admin can register new users.")  # Pass users to register user function    
        elif choice == 'va':  # View All Tasks
            view_all()
        elif choice == 'vm':  # View My Tasks
            view_mine(username)
        elif choice == 'gr':  # Generate Reports
            generate_reports(username)
        elif choice == 'ds':  # Display Statistics
            display_statistics(username,tasks)  
        elif choice == 'e':  # Exit
            return
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
     main()