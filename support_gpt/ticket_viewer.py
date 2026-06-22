import sqlite3
import os
from tabulate import tabulate

DB_PATH = os.path.join(os.path.dirname(__file__), 'tickets_db.sqlite')

def display_all_tickets():
    """Display all tickets in a formatted table"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ticket_id, emp_name, emp_id, department, priority, status, date_submitted 
            FROM tickets 
            ORDER BY date_submitted DESC
        ''')
        
        tickets = cursor.fetchall()
        conn.close()
        
        if tickets:
            headers = ['Ticket ID', 'Employee Name', 'Emp ID', 'Department', 'Priority', 'Status', 'Submitted Date']
            print("\n" + "="*150)
            print("ALL TICKETS")
            print("="*150)
            print(tabulate(tickets, headers=headers, tablefmt='grid'))
            print(f"\nTotal Tickets: {len(tickets)}\n")
        else:
            print("\nNo tickets found in the database.\n")
            
    except Exception as e:
        print(f"Error displaying tickets: {e}")

def display_tickets_by_status(status):
    """Display tickets filtered by status"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ticket_id, emp_name, emp_id, department, priority, status, date_submitted 
            FROM tickets 
            WHERE status = ?
            ORDER BY date_submitted DESC
        ''', (status,))
        
        tickets = cursor.fetchall()
        conn.close()
        
        if tickets:
            headers = ['Ticket ID', 'Employee Name', 'Emp ID', 'Department', 'Priority', 'Status', 'Submitted Date']
            print("\n" + "="*150)
            print(f"TICKETS WITH STATUS: {status.upper()}")
            print("="*150)
            print(tabulate(tickets, headers=headers, tablefmt='grid'))
            print(f"\nTotal {status.lower()} Tickets: {len(tickets)}\n")
        else:
            print(f"\nNo {status.lower()} tickets found.\n")
            
    except Exception as e:
        print(f"Error displaying tickets: {e}")

def display_ticket_details(ticket_id):
    """Display detailed information for a specific ticket"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tickets WHERE ticket_id = ?', (ticket_id,))
        ticket = cursor.fetchone()
        conn.close()
        
        if ticket:
            print("\n" + "="*80)
            print(f"TICKET DETAILS - {ticket_id}")
            print("="*80)
            print(f"Ticket ID:           {ticket[0]}")
            print(f"Employee Name:       {ticket[1]}")
            print(f"Employee ID:         {ticket[2]}")
            print(f"Department:          {ticket[3]}")
            print(f"Priority:            {ticket[4]}")
            print(f"Status:              {ticket[7]}")
            print(f"Date Submitted:      {ticket[6]}")
            print(f"\nIssue Description:\n{ticket[5]}")
            print("="*80 + "\n")
        else:
            print(f"\nTicket {ticket_id} not found.\n")
            
    except Exception as e:
        print(f"Error displaying ticket: {e}")

if __name__ == "__main__":
    print("\n🎫 TICKET VIEWER UTILITY")
    print("\nOptions:")
    print("1. View all tickets")
    print("2. View open tickets")
    print("3. View closed tickets")
    print("4. View ticket details")
    print("5. View database statistics")
    
    choice = input("\nSelect an option (1-5): ").strip()
    
    if choice == "1":
        display_all_tickets()
    elif choice == "2":
        display_tickets_by_status("Open")
    elif choice == "3":
        display_tickets_by_status("Closed")
    elif choice == "4":
        ticket_id = input("Enter Ticket ID: ").strip()
        display_ticket_details(ticket_id)
    elif choice == "5":
        from database import get_ticket_count
        total = get_ticket_count()
        print(f"\nTotal Tickets in Database: {total}\n")
    else:
        print("\nInvalid option. Please try again.\n")
