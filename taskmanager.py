import os 
import datetime
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
                if line.strip():  # Checks if the line is not empty
                    task_data = line.strip().split(";")
                    logging.debug("Task data read from file: %s", task_data)
                    task = {
                        "username": task_data[0],
                        "task_name": task_data[1],
                        "assigned_to": task_data[2],
                        "start_date": datetime.datetime.strptime(task_data[3], "%Y-%m-%d"),
                        "due_date": datetime.datetime.strptime(task_data[4], "%Y-%m-%d"),
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
    elif username == 'admin' and password == 'password':  # Adding condition for admin login
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

        users = load_users()  # Loading existing users
        if username in users:
            print("Username already exists. Please try a different username.")
            continue

        # If the username is unique, add the user to the file
        with open("user.txt", "a") as user_file:
            user_file.write(f"{username};{password}\n")
        print("User registered successfully.")
        break


def add_task(logged_in_user):
    """
    Add a new task to the tasks file.
    """
    task_name = input("Enter task name: ")
    
    if logged_in_user == "admin":
        assigned_to = input("Enter the username of the user to whom this task is assigned: ")
    else:
        assigned_to = logged_in_user
        
    due_date = input("Enter due date for the task (YYYY-MM-DD): ")
    
    try:
        datetime.datetime.strptime(due_date, "%Y-%m-%d")  # Validate due date format
        with open("tasks.txt", "a") as tasks_file:
            tasks_file.write(f"{logged_in_user};{task_name};{assigned_to};{due_date};{datetime.datetime.now().strftime('%Y-%m-%d')};No\n")
        print("Task added successfully.")

    except ValueError:
        print("Invalid due date format. Please use YYYY-MM-DD.")

def view_all():
    """
    Function to display all tasks.
    Loads tasks from the file and prints each task in a user-friendly format.
    """
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
    else:
        # Determining the maximum length of the task name for formatting
        max_task_name_length = max(len(task["task_name"]) for task in tasks)

        # Print header
        print("Task ID\tTask Name".ljust(max_task_name_length + 10), "Assigned To".ljust(20), "Due Date".ljust(12), "Date Added".ljust(12), "Completed")
        
        for index, task in enumerate(tasks, start=1):
            task_id = f"Task-{index}"
            task_name = task["task_name"]
            assigned_to = task["assigned_to"]
            due_date = task["due_date"].strftime("%Y-%m-%d")
            date_added = task["start_date"].strftime("%Y-%m-%d")
            completed = task["completed"]
            
            # Formatting the task details
            formatted_task = f"{task_id.ljust(8)}{task_name.ljust(max_task_name_length + 5)}{assigned_to.ljust(20)}{due_date.ljust(12)}{date_added.ljust(12)}{completed}"
            
            print(formatted_task)

def view_mine(username):
    """
    Function to display tasks assigned to the current user.
    param username: The username of the current user.
    """
    with open("tasks.txt", "r") as file:
        tasks = file.readlines()

    print("\nYour Tasks:")
    tasks_assigned_to_user = []  # Store tasks assigned to the current user
    
    for index, task in enumerate(tasks, start=1):
        task_details = task.strip().split(";")
        
        # Checks if the task is assigned to the current user
        if task_details[0] == username or task_details[2] == username:
            tasks_assigned_to_user.append((index, task_details))  # Store task index and details
        else:
            print(f"Task {index} is assigned to {task_details[2]}, not to {username}")

    if not tasks_assigned_to_user:
        print("You have no tasks assigned.")
    else:
        for index, task_details in tasks_assigned_to_user:
            print(f"{index}. Task details:")
            print(f"   - Assigned to: {task_details[2]}")  # Ensure the correct index is used for assigned user's username
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
            task_details = tasks_assigned_to_user[task_index][1]  # Retrieve task details
            if task_details[-1] == "Yes":
                print("This task has already been completed and cannot be edited.")
                return

            edit_choice = input("Do you want to mark this task as complete (Y/N) or edit (E)? ").strip().lower()
            if edit_choice == 'y':
                task_details[-1] = "Yes"
                tasks_assigned_to_user[task_index] = (index, task_details)  # Update task details
                tasks[task_index] = ";".join(task_details) + "\n"  # Update tasks list
                with open("tasks.txt", "w") as file:
                    file.writelines(tasks)
                print("Task marked as complete.")
            elif edit_choice == 'e':
                new_due_date = input("Enter the new due date for the task (format: YYYY-MM-DD): ").strip()
                task_details[3] = new_due_date
                tasks_assigned_to_user[task_index] = (index, task_details)  # Update task details
                tasks[task_index] = ";".join(task_details) + "\n"  # Update tasks list
                with open("tasks.txt", "w") as file:
                    file.writelines(tasks)
                print("Task edited successfully.")
            else:
                print("Invalid choice.")

        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid task number.")



def generate_task_overview(username):
    """
    Function to generate an overview of tasks.
    param username: The username of the current user.
    """
    tasks = load_tasks()

    if username != "admin":
        print("You don't have permission to generate task overview.")
        return

    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["completed"] == "Yes")
    uncompleted_tasks = total_tasks - completed_tasks

    # Calculate overdue tasks
    today = datetime.datetime.now().date()
    overdue_tasks = sum(1 for task in tasks if task["due_date"].date() < today and task["completed"] == "No")

    # Calculate percentages
    if total_tasks != 0:
        percentage_completed = (completed_tasks / total_tasks) * 100
        percentage_uncompleted = (uncompleted_tasks / total_tasks) * 100
        percentage_overdue = (overdue_tasks / total_tasks) * 100
    else:
        percentage_completed = percentage_uncompleted = percentage_overdue = 0

    # Write overview to file
    with open("task_overview.txt", "w") as file:
        file.write("Task Overview:\n")
        file.write(f"Total tasks: {total_tasks}\n")
        file.write(f"Completed tasks: {completed_tasks}\n")
        file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        file.write(f"Overdue tasks: {overdue_tasks}\n")
        file.write(f"Percentage of completed tasks: {percentage_completed:.2f}%\n")
        file.write(f"Percentage of uncompleted tasks: {percentage_uncompleted:.2f}%\n")
        file.write(f"Percentage of overdue tasks: {percentage_overdue:.2f}%\n")

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



def generate_reports(username, tasks):
    """
    Generate task overview, user overview, and statistics reports.
    """
    
    tasks = load_tasks()

    generate_task_overview(username)
    generate_user_overview(username)
    
    display_statistics(username, is_admin=True)  # Passing the username and is_admin flag to display_statistics



def display_statistics(username, is_admin):
    """
    Display statistics related to tasks and users.

    This function displays statistics such as task overview and user overview,
    based on the provided username and whether the user is an admin or not.

    Parameters:
    - username (str): The username of the current user.
    - is_admin (bool): A boolean flag indicating whether the user is an admin or not.

    Returns:
    - None

    If the user is an admin, both task overview and user overview are displayed.
    If the user is not an admin, only task overview is displayed.

    This function reads the task overview and user overview from text files if they exist.
    If the files don't exist, it generates new reports before displaying the statistics.

    """
    if not os.path.exists("task_overview.txt"):
        generate_task_overview(username)

    if is_admin:
        # Read and display statistics for both tasks and users
        if not os.path.exists("user_overview.txt"):
            generate_user_overview(username)

        with open("task_overview.txt", "r") as file:
            task_overview = file.read()
            print("Task Overview:")
            print(task_overview)

        with open("user_overview.txt", "r") as file:
            user_overview = file.read()
            print("\nUser Overview:")
            print(user_overview)
    else:
        # Read and display statistics for tasks
        with open("task_overview.txt", "r") as file:
            task_overview = file.read()
            print("Task Overview:")
            print(task_overview)

def login(users):
    """
    Function to authenticate users.
    """
    while True:
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        if username == 'admin' and password == 'password':
            print("Login successful. Welcome, admin!")
            return 'admin'
        elif username in users and users[username] == password:
            print(f"Login successful. Welcome, {username}!")
            return username
        else:
            print("Invalid username or password. Please try again.")



def display_user_task_overview(username):
    """
    Generate and display task overview for the specific user.
    param username: The username of the user for whom the task overview is generated.
    """
    tasks = load_tasks()  # Loading existing tasks
    user_tasks = [task for task in tasks if task["assigned_to"] == username]  # Filter tasks for the specific user

    if not user_tasks:
        print("No tasks found for this user.")
        return

    completed_tasks = sum(1 for task in user_tasks if task["completed"] == "Yes")
    uncompleted_tasks = len(user_tasks) - completed_tasks

    # Calculating overdue tasks
    today = datetime.datetime.now().date()
    overdue_tasks = sum(1 for task in user_tasks if task["due_date"].date() < today and task["completed"] == "No")

    # Calculating percentages
    total_tasks = len(user_tasks)
    percentage_completed = (completed_tasks / total_tasks) * 100 if total_tasks != 0 else 0
    percentage_uncompleted = (uncompleted_tasks / total_tasks) * 100 if total_tasks != 0 else 0
    percentage_overdue = (overdue_tasks / total_tasks) * 100 if total_tasks != 0 else 0

    # Display task overview
    print("Task Overview:")
    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_tasks}")
    print(f"Uncompleted tasks: {uncompleted_tasks}")
    print(f"Overdue tasks: {overdue_tasks}")
    print(f"Percentage of completed tasks: {percentage_completed:.2f}%")
    print(f"Percentage of uncompleted tasks: {percentage_uncompleted:.2f}%")
    print(f"Percentage of overdue tasks: {percentage_overdue:.2f}%")


def user_menu(username, tasks):
    """
    Function to display the user menu.
    param username: The username of the current user.
    param tasks: List of tasks.
    """

    while True:
        print("\nUser Menu:")
        print("r.Register user")
        print("a. Add Task") 
        print("va. View All Tasks")
        print("vm. View My Tasks")
        print("ds. Display Statistics")
        print("e. Exit")
        choice = input("Enter your choice: ").lower()

        if choice == 'a':  # Add Task
            add_task(username)
        elif choice == 'va':  # View All Tasks
            view_all()
        elif choice == 'vm':  # View My Tasks
            view_mine(username)
        elif choice == 'ds':  # Display Statistics
            if username == 'admin':
                display_statistics(username, tasks)
            else:
                display_user_task_overview(username)
        elif choice == 'r':
            print("Sorry, only admin can register new users.")
        elif choice == 'e':  # Exit
            return
        else:
            print("Invalid choice. Please try again.")

def admin_menu(username,users,tasks):
    """
    Function to display the admin menu.
    param username: The username of the current user.
    param users: List of all users.
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
            add_task(username)  # Passing the logged-in username
        elif choice == 'r':  # Register User
            if username == 'admin':  # Check if the user is admin
                reg_user(username)  # Passing the username to register user function
            else:
                print("Only admin can register new users.")  # Inform the user that only admin can register users    
        elif choice == 'va':  # View All Tasks
            view_all()
        elif choice == 'vm':  # View My Tasks
            view_mine(username)
        elif choice == 'gr':  # Generate Reports
            generate_reports(username,tasks)
        elif choice == 'ds':  # Display Statistics
            display_statistics(username, tasks)  
        elif choice == 'e':  # Exit
            return
        else:
            print("Invalid choice. Please try again.")
def main():
    """
    Main function to run the task manager program.
    """
    users = load_users()  # Loading existing users
    tasks = load_tasks()  # Loading existing tasks

    while True:
        print("\nMain Menu:")
        print("l. Login")
        print("e. Exit")
        choice = input("Enter your choice: ").strip().lower()  # Ensures uniformity in input handling
        print("DEBUG: User input:", choice)  # Debug print statement

        if choice == 'l':  # Login
            username = authenticate_user(users)
            if username:
                global current_user  # Using the global variable
                current_user = username  # Updating the global variable
                print(f"Welcome, {username}!")
                # Present extended menu if logged in successfully
                if username == 'admin':
                    admin_menu(username, users, tasks)  # Calling admin menu with the necessary arguments
                else:
                    user_menu(username, tasks)  # Calling user menu with the necessary arguments
        
        elif choice == 'e':  # Exit
            exit()
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
     main()