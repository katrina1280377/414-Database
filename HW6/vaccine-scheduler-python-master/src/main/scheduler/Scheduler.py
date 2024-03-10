from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime


'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None


def create_patient(tokens):
    # create_patient <username> <password>
    # Create a new patient with the provided username and password: create_patient <username> <password>
    if len(tokens) != 3:
        print("Create patient failed.")
        return

    username = tokens[1]
    password = tokens[2]
	
    # Check if the username is already taken
    if username_exists_patient(username):
        print("Username taken, try again!")
        return
	
	 # Generate salt and hash password
    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # Create a new patient object
    patient = Patient(username, salt=salt, hash=hash)

    # Save patient information to the database
    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Create patient failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Create patient failed")
        print(e)
        return
    print("Created patient ", username)
    pass


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)

def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False

def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):
    # login_patient <username> <password>
    # Log in a patient with the provided username and password.
    if len(tokens) != 3:
        print("Login patient failed")
        return
    
    global current_patient
    
    # Check if a patient is already logged in
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in, try again")
        return

    username = tokens[1]
    password = tokens[2]
    
	# Retrieve patient information from the database
    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login patient failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login patient failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if patient is None:
        print("Login patient failed.")
    else:
        print("Logged in as: " + username)
        current_patient = patient
    pass


def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if caregiver is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    # Check if a user is logged in
    if current_patient is None and current_caregiver is None:
        print("Please login first")
        return

    # Check if the date is provided
    if len(tokens) != 2:
        print("Please provide a date")
        return

    date = tokens[1]

    cm = ConnectionManager()
    conn = cm.create_connection()

    try:
        get_caregivers_query = "SELECT Username FROM Availabilities WHERE Time = %s ORDER BY Username"
        cursor = conn.cursor()
        cursor.execute(get_caregivers_query, date)
        for row in cursor:
            print(row[0])
        name_doses = "SELECT Name, Doses FROM Vaccines"
        cursor.execute(name_doses)
        for row in cursor:
            print(row[0]+" "+str(row[1]))
    except:
        print("Please try again")
    finally:
        cm.close_connection()



def reserve(tokens):
    if current_patient is None and current_caregiver is None:
        print("Please login first")
        return
    elif current_caregiver is not None:
        print("Please login as patient")
        return

    # Check if the necessary arguments are provided
    if len(tokens) != 3:
        print("Please provide a date and a vaccine")
        return

    date = tokens[1]
    vaccine_name = tokens[2]

    # Check for available caregivers
    cm = ConnectionManager()
    conn = cm.create_connection()

    try:
        # Check if the caregiver is available for the given date
        check_availability_query = "SELECT Username FROM Availabilities WHERE Time = %s order by Username"
        cursor = conn.cursor()
        cursor.execute(check_availability_query, date)
        count = cursor.fetchone()

        if count is None:
            print("No Caregiver is available")
            return

        # Check available vaccine doses
        check_vaccine_query = "SELECT Doses FROM Vaccines WHERE Name = %s"
        cursor.execute(check_vaccine_query, vaccine_name)
        available_doses = cursor.fetchone()

        if available_doses is None or count[0]==0:
            print("Not enough available doses")
            return

        # Reserve appointment
        caregiver_first = count[0]
        reserve_appointment_query = "INSERT INTO Appointments VALUES (%s, %s, %s, %s)"
        cursor.execute(reserve_appointment_query, (caregiver_first, current_patient.username, vaccine_name, date))
        conn.commit()
        id = cursor.lastrowid
        delete = "DELETE FROM Availabilities WHERE Username = %s AND Time = %s"
        cursor.execute(delete, (caregiver_first, date))
        conn.commit()
        print("Appointment ID: "+str(id)+", Caregiver username: "+caregiver_first)
        
    except pymssql.Error:
        print("Please try again")
    finally:
        cm.close_connection()

def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    try:
        d = datetime.datetime(year, month, day)
        current_caregiver.upload_availability(d)
    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        return
    print("Availability uploaded!")


def cancel(tokens):
    global current_patient, current_caregiver

    # Check if a user is logged in
    if current_patient is None and current_caregiver is None:
        print("Please login first")
        return

    # Check if the necessary arguments are provided
    if len(tokens) != 2:
        print("Please provide an appointment ID to cancel")
        return

    appointment_id = tokens[1]

    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor()

    try:
        # Check if the appointment exists
        check_appointment_query = "SELECT * FROM Appointments WHERE AppointmentID = %s"
        cursor.execute(check_appointment_query, appointment_id)
        appointment = cursor.fetchone()

        if appointment is None:
            print("Appointment not found")
            return

        # Check if the user is authorized to cancel the appointment
        if current_patient is not None and appointment[2] != current_patient.get_username():
            print("You are not authorized to cancel this appointment")
            return

        if current_caregiver is not None and appointment[1] != current_caregiver.get_username():
            print("You are not authorized to cancel this appointment")
            return

        # Delete the appointment
        delete_appointment_query = "DELETE FROM Appointments WHERE AppointmentID = %s"
        cursor.execute(delete_appointment_query, appointment_id)
        conn.commit()

        print("Appointment successfully canceled")

    except pymssql.Error:
        print("Please try again")
    finally:
        cm.close_connection()


def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        vaccine = Vaccine(vaccine_name, doses).get()
    except pymssql.Error as e:
        print("Error occurred when adding doses")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when adding doses")
        print("Error:", e)
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    print("Doses updated!")


def show_appointments(tokens):
    global current_patient, current_caregiver

    # Check if a user is logged in
    if current_patient is None and current_caregiver is None:
        print("Please login first")
        return
        
    cm = ConnectionManager()
    conn = cm.create_connection()
    
    try:
        # Get appointments for the current user
        if current_caregiver is not None:
            care_schedule = "SELECT AppointmentID, Vaccine, Time, Patient FROM Appointments WHERE Caregiver = %s ORDER BY AppointmentID"
            cursor = conn.cursor(as_dict=True)
            cursor.execute(care_schedule, current_caregiver.username)
            for row in cursor:
                print(str(row['AppointmentID'])+" "+row['Vaccine']+" "+str(row['Time'])+" "+row['Patient'])

        if current_patient is not None:
            pat_schedule = "SELECT AppointmentID, Vaccine, Time, Caregiver FROM Appointments WHERE Patient = %s ORDER BY AppointmentID"
            cursor = conn.cursor(as_dict=True)
            cursor.execute(pat_schedule, current_patient.username)
            for row in cursor:
                print(str(row['AppointmentID'])+" "+row['Vaccine']+" "+str(row['Time'])+" "+row['Caregiver'])
    except pymssql.Error:
        print("Please try again")
    finally:
        cm.close_connection()



def logout(tokens):
    global current_patient, current_caregiver
    
    # Check if a user is logged in
    if current_patient is None and current_caregiver is None:
        print("Please login first")
        return
    try:
        print("Successfully logged out!")
        current_patient = None
        current_caregiver = None
    except:
        print("Please try again!")


def start():
    stop = False
    print()
    print(" *** Please enter one of the following commands *** ")
    print("> create_patient <username> <password>")  # //TODO: implement create_patient (Part 1)
    print("> create_caregiver <username> <password>")
    print("> login_patient <username> <password>")  # // TODO: implement login_patient (Part 1)
    print("> login_caregiver <username> <password>")
    print("> search_caregiver_schedule <date>")  # // TODO: implement search_caregiver_schedule (Part 2)
    print("> reserve <date> <vaccine>")  # // TODO: implement reserve (Part 2)
    print("> upload_availability <date>")
    print("> cancel <appointment_id>")  # // TODO: implement cancel (extra credit)
    print("> add_doses <vaccine> <number>")
    print("> show_appointments")  # // TODO: implement show_appointments (Part 2)
    print("> logout")  # // TODO: implement logout (Part 2)
    print("> Quit")
    print()
    while not stop:
        response = ""
        print("> ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Please try again!")
            break

        response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Please try again!")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == "cancel":
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Bye!")
            stop = True
        else:
            print("Invalid operation name!")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()
