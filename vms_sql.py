import sqlite3
import random
import string
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the database by creating the tables
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Volunteers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS volunteers (
        volunteer_id TEXT PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        mobile TEXT NOT NULL UNIQUE,
        course TEXT NOT NULL,
        semester TEXT NOT NULL
    );
    ''')
    
    # Create Volunteers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        event_id TEXT PRIMARY KEY,
        event_name TEXT NOT NULL,
        description TEXT NOT NULL,
        start_datetime TEXT NOT NULL,
        end_datetime TEXT NOT NULL,
        address TEXT NOT NULL
    );
    ''')
    
    # Create Event_Volunteer table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS event_volunteer (
    event_id INT NOT NULL,
    volunteer_id INT NOT NULL,
    role TEXT,
    certificate BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (volunteer_id) REFERENCES volunteers(volunteer_id) ON DELETE CASCADE
    );
    ''')

    # Create Admins table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin (
        admin_id TEXT PRIMARY KEY,
        password TEXT NOT NULL
    );
    ''')

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('vms.db')  # Path to your SQLite DB
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn
    
# Function to insert a new volunteer and generate a unique volunteer_id
def insert_volunteer(first_name, last_name, email, password, mobile, course, semester):
    # Generate a unique volunteer_id in the format KRMU_VMS_XXXXXX
    volunteer_id = generate_volunteer_id()

    conn = get_db_connection()
    cursor = conn.cursor()
    
    hashed_password = generate_password_hash(password)
    
    # Insert volunteer data into the database
    cursor.execute('''
    INSERT INTO volunteers (volunteer_id, first_name, last_name, email, password, mobile, course, semester)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (volunteer_id, first_name, last_name, email, hashed_password, mobile, course, semester))

    conn.commit()
    conn.close()
    
    return volunteer_id  # Return the generated volunteer_id

# Check if a volunteer with the given email or mobile already exists
def check_existing_user(email, mobile):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT COUNT(*) FROM volunteers WHERE email = ? OR mobile = ?
    ''', (email, mobile))

    exists = cursor.fetchone()[0]
    conn.close()
    
    return exists > 0

# Check if admin credentials are valid
def check_admin(admin_id, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the hashed password from the database
    cursor.execute('''
        SELECT password FROM admin WHERE admin_id = ?
    ''', (admin_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        hashed_password = row['password']
        return check_password_hash(hashed_password, password)
    else:
        return False

# Insert a default admin into the database (used when setting up the system)
def insert_admin(admin_id, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    hashed_password = generate_password_hash(password)
    
    cursor.execute('''
    INSERT INTO admin (admin_id, password) VALUES (?, ?)
    ''', (admin_id, hashed_password))

    conn.commit()
    conn.close()

# Generate a unique volunteer ID in the format KRMU_VMS_XXXXXX
def generate_volunteer_id():
    # Ensure unique 6-digit random number
    while True:
        volunteer_id = 'KRMU_VMS_' + ''.join(random.choices(string.digits, k=6))
        if not is_volunteer_id_exists(volunteer_id):
            return volunteer_id

# Check if the generated Volunteer ID already exists in the database
def is_volunteer_id_exists(volunteer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(1) FROM volunteers WHERE volunteer_id = ?", (volunteer_id,))
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists
    
def insert_event(event_name, description, start_datetime, end_datetime, address):
    event_id = generate_event_id()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert event data into the database
    cursor.execute('''
    INSERT INTO events (event_id, event_name, description, start_datetime, end_datetime, address)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (event_id, event_name, description, start_datetime, end_datetime, address))

    conn.commit()
    conn.close()

    return event_id  # Return the generated event_id
    
def generate_event_id():
    # Ensure unique 6-digit random number
    while True:
        event_id = 'KRMU_EVENT_' + ''.join(random.choices(string.digits, k=6))
        if not is_event_id_exists(event_id):
            return event_id

# Check if the generated Volunteer ID already exists in the database
def is_event_id_exists(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(1) FROM events WHERE event_id = ?", (event_id,))
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists  

def get_all_events():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT event_id, event_name, description, start_datetime, end_datetime, address
        FROM events
        ORDER BY start_datetime DESC
    ''')

    events = cursor.fetchall()
    conn.close()

    # Convert rows to list of dicts
    event_list = [dict(event) for event in events]
    return event_list
    
    
def get_event_by_id(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM events WHERE event_id = ?', (event_id,))
    event = cursor.fetchone()
    conn.close()
    return event

def update_event_by_id(event_id, event_name, description, start_datetime, end_datetime, address):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE events
        SET event_name = ?, description = ?, start_datetime = ?, end_datetime = ?, address = ?
        WHERE event_id = ?
    ''', (event_name, description, start_datetime, end_datetime, address, event_id))

    conn.commit()
    conn.close()    
    
def delete_event(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM events WHERE event_id = ?', (event_id,))

    if cursor.rowcount == 0:
        raise Exception("Event not found.")

    conn.commit()
    conn.close()    
    
def get_all_volunteers():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT volunteer_id, first_name, last_name, email, mobile, course, semester FROM volunteers')
    volunteers = cursor.fetchall()

    conn.close()
    
    return [dict(row) for row in volunteers]    
    
def get_volunteer_by_id(volunteer_id):
    conn = get_db_connection()
    volunteer = conn.execute('SELECT * FROM volunteers WHERE volunteer_id = ?', (volunteer_id,)).fetchone()
    conn.close()
    return volunteer


def update_volunteer(volunteer_id, data):
    conn = get_db_connection()
    conn.execute('''
        UPDATE volunteers 
        SET first_name = ?, last_name = ?, mobile = ?, course = ?, semester = ?
        WHERE volunteer_id = ?
    ''', (data['first_name'], data['last_name'], data['mobile'], data['course'], data['semester'], volunteer_id))
    conn.commit()
    conn.close()


def delete_volunteer(volunteer_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM volunteers WHERE volunteer_id = ?', (volunteer_id,))
    conn.commit()
    conn.close()
    
def get_registered_events(volunteer_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT e.event_id, e.event_name, e.description, e.start_datetime, e.end_datetime, e.address, ev.role
            FROM events e
            JOIN event_volunteer ev ON e.event_id = ev.event_id
            WHERE ev.volunteer_id = ?
            ORDER BY datetime(e.start_datetime) DESC
        ''', (volunteer_id,))
        events = cursor.fetchall()
        conn.close()
        return {
            'success': True,
            'message': 'Events retrieved.',
            'data': events
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error: {str(e)}',
            'data': []
        }

def unregister_from_event(volunteer_id, event_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM event_volunteer WHERE volunteer_id = ? AND event_id = ?', (volunteer_id, event_id))
        conn.commit()
        conn.close()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}
    