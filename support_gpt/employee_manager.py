"""
Employee Management Utility
Helps you manage employee accounts in the SupportGPT system
"""

import sqlite3
from database import register_employee, get_all_employees, authenticate_employee
from tabulate import tabulate

def add_employee():
    """Add a new employee to the system"""
    print("\n" + "="*60)
    print("ADD NEW EMPLOYEE")
    print("="*60)
    
    emp_id = input("Employee ID (e.g., EMP001): ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    emp_name = input("Full Name: ").strip()
    email = input("Email (optional): ").strip()
    department = input("Department (e.g., IT, HR, Finance): ").strip()
    
    if not emp_id or not username or not password or not emp_name or not department:
        print("\n❌ Error: All fields except email are required!\n")
        return
    
    success = register_employee(emp_id, username, password, emp_name, email, department)
    
    if success:
        print(f"\n✅ Employee '{emp_name}' registered successfully!")
        print(f"   Username: {username}")
        print(f"   Employee ID: {emp_id}\n")
    else:
        print("\n❌ Error: Username or Employee ID already exists!\n")

def view_all_employees():
    """View all registered employees"""
    employees = get_all_employees()
    
    if employees:
        headers = ['Employee ID', 'Username', 'Full Name', 'Email', 'Department', 'Created At']
        
        # Format the data (exclude password)
        data = []
        for emp in employees:
            data.append([emp[0], emp[1], emp[3], emp[4], emp[5], emp[6]])
        
        print("\n" + "="*120)
        print("ALL EMPLOYEES")
        print("="*120)
        print(tabulate(data, headers=headers, tablefmt='grid'))
        print(f"\nTotal Employees: {len(employees)}\n")
    else:
        print("\n❌ No employees found in the system.\n")

def test_login():
    """Test employee login credentials"""
    print("\n" + "="*60)
    print("TEST EMPLOYEE LOGIN")
    print("="*60)
    
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    employee = authenticate_employee(username, password)
    
    if employee:
        print(f"\n✅ Login Successful!")
        print(f"   Employee ID: {employee[0]}")
        print(f"   Name: {employee[3]}")
        print(f"   Department: {employee[5]}\n")
    else:
        print(f"\n❌ Login Failed! Invalid credentials.\n")

def setup_demo_employees():
    """Setup demo employees for testing"""
    print("\n" + "="*60)
    print("SETTING UP DEMO EMPLOYEES")
    print("="*60)
    
    demo_employees = [
        ("EMP001", "john_doe", "john123", "John Doe", "john@company.com", "Engineering"),
        ("EMP002", "sarah_smith", "sarah123", "Sarah Smith", "sarah@company.com", "Human Resources"),
        ("EMP003", "mike_johnson", "mike123", "Mike Johnson", "mike@company.com", "Finance"),
        ("EMP004", "emma_wilson", "emma123", "Emma Wilson", "emma@company.com", "Marketing"),
        ("EMP005", "alex_kumar", "alex123", "Alex Kumar", "alex@company.com", "IT Support"),
    ]
    
    added = 0
    for emp_id, username, password, emp_name, email, department in demo_employees:
        success = register_employee(emp_id, username, password, emp_name, email, department)
        if success:
            print(f"✅ Added: {emp_name} ({username})")
            added += 1
        else:
            print(f"⚠️  Skipped: {emp_name} (already exists)")
    
    print(f"\n{added} employee(s) added successfully!\n")
    print("Demo Login Credentials:")
    print("-" * 60)
    for emp_id, username, password, emp_name, email, department in demo_employees:
        print(f"  Username: {username:20} | Password: {password}")
    print()

if __name__ == "__main__":
    while True:
        print("\n" + "="*60)
        print("🤖 SupportGPT - EMPLOYEE MANAGEMENT")
        print("="*60)
        print("\nOptions:")
        print("1. Add new employee")
        print("2. View all employees")
        print("3. Test login credentials")
        print("4. Setup demo employees")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ").strip()
        
        if choice == "1":
            add_employee()
        elif choice == "2":
            view_all_employees()
        elif choice == "3":
            test_login()
        elif choice == "4":
            setup_demo_employees()
        elif choice == "5":
            print("\n✅ Goodbye!\n")
            break
        else:
            print("\n❌ Invalid option. Please try again.\n")
