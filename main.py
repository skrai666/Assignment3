import sqlite3

conn = sqlite3.connect("Employee.db")

c = conn.cursor()


# Database class containing all database functions
class DBOperations:

    # Creates table
    @staticmethod
    def create_table():
        with conn:
            # check if table exists, if not create table
            list_of_tables = c.execute(
                """SELECT name FROM sqlite_master WHERE type='table'
                    AND name='employees'; """).fetchall()
            if not list_of_tables:
                c.execute("""CREATE TABLE IF NOT EXISTS employees (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            forename TEXT NOT NULL,
                            surname TEXT NOT NULL,
                            email TEXT NOT NULL,
                            salary REAL NOT NULL
                            )""")
                print("Table successfully created")
            else:
                print("Warning: Table already created")

    # Calls methods to insert data into database
    @staticmethod
    def insert_data():
        employee = DBOperations.create_employee()
        DBOperations.insert_employee(employee)

    # Intakes user input and creates employee instance using input
    @staticmethod
    def create_employee():
        id = None
        title = input("Employee title: ").lower()
        forename = input("Employee forename: ").lower().strip()
        surname = input("Employee surname: ").lower().strip()
        email = input("Employee email: ").lower().strip()
        salary = DBOperations.normalise_salary_type(input("Employee salary: "))
        employee = Employee(id, title, forename, surname, email, salary)
        return employee

    # Normalises salary
    # Converts salary to float and rounds salary to 2 decimal places
    # If user entry is not a number, i.e. cannot be converted, asks user to re-input salary
    @staticmethod
    def normalise_salary_type(salary):
        while True:
            try:
                salary = "{:.2f}".format(float(salary))
                break
            except ValueError:
                salary = input("Invalid entry. Please enter a number value: ")
                continue
        return salary

    # inserts employee into employee database
    @staticmethod
    def insert_employee(employee):
        with conn:
            c.execute("INSERT INTO employees VALUES (:id, :title, :forename, :surname, :email, :salary)",
                      {'id': None, 'title': employee.title, 'forename': employee.forename, 'surname': employee.surname,
                       'email': employee.email,
                       'salary': employee.salary})
            print("Employee added.")

    # Gets all data from the database and prints to console
    @staticmethod
    def view_all_data():
        with conn:
            c.execute("SELECT * FROM employees")
            employee_data = c.fetchall()
            if len(employee_data) > 0:
                DBOperations.print_data(employee_data)
            else:
                print("No records in database")

    # Updates data matching user input in the database and prints updated record to console
    @staticmethod
    def update_data():
        category_function = 'Select users to update'
        criteria_function = 'search criterion'
        update_category_function = 'Select a category to update'
        update_criteria_function = 'update value'
        search_category = DBOperations.get_category(category_function)
        search_category = DBOperations.str_category(search_category)
        search_criteria = DBOperations.get_criteria(criteria_function, search_category)
        returned_data = DBOperations.search_selected(search_category, search_criteria)
        print(len(returned_data))
        DBOperations.print_number_matching_update(returned_data)
        DBOperations.print_data(returned_data)
        if len(returned_data) == 0:
            return
        else:
            int_update_category = DBOperations.get_update_category(update_category_function)
            update_category = DBOperations.str_update_category(int_update_category)
            update_criteria = DBOperations.get_criteria(update_criteria_function, update_category)
            if DBOperations.confirm():
                DBOperations.update_selected(search_category, search_criteria, update_category, update_criteria)
                print("Employee(s) successfully updated.")
            else:
                return

    # Confirms with user if update should continue
    @staticmethod
    def confirm():
        while True:
            try:
                user_confirmation = int(input("""
                Enter 1 to continue
                Enter 2 to cancel: \n"""))
            except ValueError:
                print("Invalid input")
                continue
            if user_confirmation == 1:
                return True
            elif user_confirmation == 2:
                return False
            else:
                print("Invalid choice")
                continue

    # Prints heading stating the number of employees to be updated
    @staticmethod
    def print_number_matching_update(data_to_update):
        if len(data_to_update) == 0:
            print("\nNo employees match the update criteria.\n")
        elif len(data_to_update) == 1:
            print("\n", len(data_to_update), "employee will be updated. Employee: \n")
        else:
            print("\n", len(data_to_update), "employees will be updated. Employees: \n")

    # Searches the database for employees matching the search category and criteria
    @staticmethod
    def update_selected(search_category, search_criteria, update_category, update_criteria):
        with conn:
            c.execute(
                "UPDATE employees SET " + update_category + " = :update_criteria WHERE " + search_category +
                " = :search_criteria",
                {'search_criteria': search_criteria, 'update_criteria': update_criteria})
        return c.fetchall()

    # Searches for data matching user input in the database and prints to console
    @staticmethod
    def search_data():
        category_function = 'Search'
        criteria_function = 'search criterion'
        search_category = DBOperations.get_category(category_function)
        search_category = DBOperations.str_category(search_category)
        search_criteria = DBOperations.get_criteria(criteria_function, search_category)
        returned_data = DBOperations.search_selected(search_category, search_criteria)
        DBOperations.print_number_matching_search(returned_data)
        DBOperations.print_data(returned_data)

    # Prints heading stating the number of employees to be updated
    @staticmethod
    def print_number_matching_search(returned_data):
        if len(returned_data) == 0:
            print("No employees match the search criteria.")
        elif len(returned_data) == 1:
            print(len(returned_data), "employee has been found:")
        else:
            print(len(returned_data), "employees have been found:")

    # Gets user category to update the database
    @staticmethod
    def get_update_category(category_function):
        while True:
            print(category_function + " using the following categories:")
            print("""
                1. Title
                2. Forename
                3. Surname
                4. Email
                5. Salary
                """)
            try:
                category = int(input("Enter the number corresponding to your choice: "))
            except ValueError:
                print("Invalid input. Please enter a number input.")
                continue
            if category not in range(0, 6):
                print("Invalid Choice. Please re-enter your choice. ")
                continue
            else:
                break
        return category

    # Converts update category number to variable name
    @staticmethod
    def str_update_category(int_category):
        if int_category == 1:
            category = str('title')
        elif int_category == 2:
            category = str('forename')
        elif int_category == 3:
            category = str('surname')
        elif int_category == 4:
            category = str('email')
        elif int_category == 5:
            category = str('salary')
        return category

    # Gets user category to search the database
    @staticmethod
    def get_category(category_function):
        while True:
            print(category_function + " using the following categories:")
            print("""
                1. ID
                2. Title
                3. Forename
                4. Surname
                5. Email
                6. Salary
                """)
            try:
                category = int(input("Enter the number corresponding to your choice: "))
            except ValueError:
                print("Invalid input. Please enter a number input.")
                continue
            if category not in range(0, 7):
                print("Invalid Choice. Please re-enter your choice. ")
                continue
            else:
                break
        return category

    # Converts search category number to variable name
    @staticmethod
    def str_category(int_category):
        if int_category == 1:
            category = str('id')
        elif int_category == 2:
            category = str('title')
        elif int_category == 3:
            category = str('forename')
        elif int_category == 4:
            category = str('surname')
        elif int_category == 5:
            category = str('email')
        elif int_category == 6:
            category = str('salary')
        return category

    # Gets user criteria to search the database
    @staticmethod
    def get_criteria(criteria_function, category):
        while True:
            if category == 'id':
                try:
                    criteria = int(input("Please enter your " + criteria_function + ": "))
                    break
                except ValueError:
                    print("Invalid " + criteria_function + ".")
                    continue
            elif category == 'salary':
                try:
                    criteria = float(input("Please enter your " + criteria_function + ": "))
                    criteria = "{:.2f}".format(criteria)
                    break
                except ValueError:
                    print("Invalid " + criteria_function + ".")
                    continue
            else:
                criteria = input("Please enter your " + criteria_function + ": ").lower().strip()
                break
        return criteria

    # Prints employee data to the console
    @staticmethod
    def print_data(employee_data):
        for employee in employee_data:
            print("Employee ID: ", employee[0])
            print("Name: ", employee[1].title() + ' ' + employee[2].title() + ' ' + employee[3].title())
            print("Email: ", employee[4])
            print("Salary: £", employee[5])
            print("\n")

    # Searches the database for employees matching the search category and criteria
    @staticmethod
    def search_selected(search_category, search_criteria):
        with conn:
            c.execute("SELECT * FROM employees WHERE " + search_category + " = :search_criteria",
                      {'search_criteria': search_criteria})
        return c.fetchall()

    # Deletes data from the database
    @staticmethod
    def delete_data():
        user_delete_input = DBOperations.delete_menu()
        if user_delete_input == 1:
            DBOperations.delete_all()
        elif user_delete_input == 2:
            DBOperations.delete_employee()
        elif user_delete_input == 3:
            return

    # Prints delete menu and intakes user choice
    @staticmethod
    def delete_menu():
        while True:
            print("""Please choose from the following delete options: 
               1. Delete all employees 
               2. Delete selected employees
               3. Exit delete menu
               """)
            try:
                user_delete_input = int(input("Please enter the number corresponding to your selection: "))
                if user_delete_input not in range(0, 4):
                    print("Invalid input")
                    continue
                else:
                    break
            except ValueError:
                print("Invalid input")
                continue
        return user_delete_input

    # Deletes all employees from the database
    @staticmethod
    def delete_all():
        with conn:
            while True:
                if DBOperations.confirm():
                    c.execute("DELETE FROM employees")
                    print("All", c.rowcount, "records have been deleted.")
                    print("No data remains.")
                    return
                else:
                    return

    # Calls functions to get user input delete category and criteria from the database and deletes matching employees
    @staticmethod
    def delete_employee():
        category_function = 'Delete'
        criteria_function = 'delete criterion'
        delete_category = DBOperations.get_category(category_function)
        delete_category = DBOperations.str_category(delete_category)
        delete_criteria = DBOperations.get_criteria(criteria_function, delete_category)
        returned_data = DBOperations.search_selected(delete_category, delete_criteria)
        if len(returned_data) != 0:
            if DBOperations.confirm():
                DBOperations.print_employees_to_delete(returned_data)
                DBOperations.delete_selected_employees(delete_category, delete_criteria)
                print("Employee(s) successfully deleted")
            else:
                return
        else:
            print("No matching employee.")
            return

    # Prints employees to be deleted
    @staticmethod
    def print_employees_to_delete(returned_data):
        if len(returned_data) == 0:
            print("No employees match the delete criteria.")
        else:
            print("The following", str(len(returned_data)), "employee/s will be deleted: ")
        DBOperations.print_data(returned_data)

    # Deletes matching employees
    @staticmethod
    def delete_selected_employees(delete_category, delete_criteria):
        with conn:
            c.execute("DELETE from employees WHERE " + delete_category + " = :delete_criteria",
                      {'delete_criteria': delete_criteria})

    # Closes connection and commits changes
    @staticmethod
    def close_conn():
        conn.commit()
        conn.close()


# Employee class
class Employee:

    def __init__(self, id, title, forename, surname, email, salary):
        self.id = id
        self.title = title
        self.forename = forename
        self.surname = surname
        self.email = email
        self.salary = salary


# The main function will parse arguments.
# These arguments will be defined by the users on the console.
# The user will select a choice from the menu to interact with the database.

# Prints options available to the user
while True:
    print("\nThe following menu options can be used to access and edit the employee database:")
    print(" 1. Create employee table")
    print(" 2. Add employee")
    print(" 3. View all employees")
    print(" 4. Search employee(s)")
    print(" 5. Update employee(s)")
    print(" 6. Delete employee(s)")
    print(" 7. Exit\n")

    # Takes in user input
    db_ops = DBOperations()
    try:
        __choose_menu = int(input("Enter the number corresponding to your choice: "))
    except ValueError:
        __choose_menu = 0
        pass
    if __choose_menu == 1:
        db_ops.create_table()
    elif __choose_menu == 2:
        db_ops.insert_data()
    elif __choose_menu == 3:
        db_ops.view_all_data()
    elif __choose_menu == 4:
        db_ops.search_data()
    elif __choose_menu == 5:
        db_ops.update_data()
    elif __choose_menu == 6:
        db_ops.delete_data()
    elif __choose_menu == 7:
        db_ops.close_conn()
        exit(0)
    else:
        print("Invalid choice")
    input("Press the enter key to go back to the main menu.")
