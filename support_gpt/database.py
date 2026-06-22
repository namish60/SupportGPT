import sqlite3
import os
from datetime import datetime
from pathlib import Path

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'tickets_db.sqlite')

def init_database():
    """Initialize the tickets database with the required schema"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            emp_id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            emp_name TEXT NOT NULL,
            email TEXT,
            department TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create tickets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            emp_name TEXT NOT NULL,
            emp_id TEXT NOT NULL,
            department TEXT NOT NULL,
            priority TEXT NOT NULL,
            issue_description TEXT NOT NULL,
            date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Open'
        )
    ''')
    
    conn.commit()
    conn.close()

def save_ticket(ticket_id, emp_name, emp_id, department, priority, issue_description):
    """Save a new ticket to the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tickets 
            (ticket_id, emp_name, emp_id, department, priority, issue_description, date_submitted, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ticket_id, emp_name, emp_id, department, priority, issue_description, datetime.now(), 'Open'))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Ticket ID already exists
        return False
    except Exception as e:
        print(f"Error saving ticket: {e}")
        return False

def get_all_tickets():
    """Retrieve all tickets from the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tickets ORDER BY date_submitted DESC')
        tickets = cursor.fetchall()
        
        conn.close()
        return tickets
    except Exception as e:
        print(f"Error retrieving tickets: {e}")
        return []

def get_tickets_by_employee(emp_id):
    """Retrieve tickets for a specific employee"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tickets WHERE emp_id = ? ORDER BY date_submitted DESC', (emp_id,))
        tickets = cursor.fetchall()
        
        conn.close()
        return tickets
    except Exception as e:
        print(f"Error retrieving employee tickets: {e}")
        return []

def get_ticket_by_id(ticket_id):
    """Retrieve a specific ticket by its ID"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tickets WHERE ticket_id = ?', (ticket_id,))
        ticket = cursor.fetchone()
        
        conn.close()
        return ticket
    except Exception as e:
        print(f"Error retrieving ticket: {e}")
        return None

def update_ticket_status(ticket_id, status):
    """Update the status of a ticket"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE tickets SET status = ? WHERE ticket_id = ?', (status, ticket_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating ticket status: {e}")
        return False

def get_ticket_count():
    """Get total number of tickets in the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM tickets')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    except Exception as e:
        print(f"Error getting ticket count: {e}")
        return 0

# ============================================================
# EMPLOYEE AUTHENTICATION FUNCTIONS
# ============================================================

def authenticate_employee(username, password):
    """Authenticate an employee and return their details"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM employees WHERE username = ? AND password = ?', (username, password))
        employee = cursor.fetchone()
        
        conn.close()
        return employee
    except Exception as e:
        print(f"Error authenticating employee: {e}")
        return None

def get_employee_by_username(username):
    """Get employee details by username"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM employees WHERE username = ?', (username,))
        employee = cursor.fetchone()
        
        conn.close()
        return employee
    except Exception as e:
        print(f"Error retrieving employee: {e}")
        return None

def get_employee_by_id(emp_id):
    """Get employee details by ID"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM employees WHERE emp_id = ?', (emp_id,))
        employee = cursor.fetchone()
        
        conn.close()
        return employee
    except Exception as e:
        print(f"Error retrieving employee: {e}")
        return None

def register_employee(emp_id, username, password, emp_name, email, department):
    """Register a new employee"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO employees 
            (emp_id, username, password, emp_name, email, department)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (emp_id, username, password, emp_name, email, department))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Username or emp_id already exists
        return False
    except Exception as e:
        print(f"Error registering employee: {e}")
        return False

def get_all_employees():
    """Get all employees"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM employees ORDER BY emp_name')
        employees = cursor.fetchall()
        
        conn.close()
        return employees
    except Exception as e:
        print(f"Error retrieving employees: {e}")
        return []

def update_employee_password(emp_id, new_password):
    """Update employee password"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE employees SET password = ? WHERE emp_id = ?', (new_password, emp_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating password: {e}")
        return False

# Initialize database when module is imported
init_database()
