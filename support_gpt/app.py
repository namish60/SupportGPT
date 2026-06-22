import streamlit as st

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="SupportGPT",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------------------------
# Session State Initialization
# -------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_type" not in st.session_state:
    st.session_state.user_type = None  # "employee" or "admin"

if "username" not in st.session_state:
    st.session_state.username = None

# Employee-specific session state
if "emp_id" not in st.session_state:
    st.session_state.emp_id = None

if "emp_name" not in st.session_state:
    st.session_state.emp_name = None

if "email" not in st.session_state:
    st.session_state.email = None

if "department" not in st.session_state:
    st.session_state.department = None

# -------------------------------------------------
# Navigation Functions
# -------------------------------------------------

def go_to_landing():
    """Navigate to landing page"""
    st.session_state.page = "landing"
    st.session_state.authenticated = False
    st.session_state.user_type = None
    st.session_state.username = None

def go_to_employee_login():
    """Navigate to employee login"""
    st.session_state.page = "emp_login"
    st.session_state.user_type = "employee"

def go_to_admin_login():
    """Navigate to admin login"""
    st.session_state.page = "admin_login"
    st.session_state.user_type = "admin"

def go_to_employee_dashboard():
    """Navigate to employee dashboard"""
    st.session_state.page = "emp_dashboard"
    st.session_state.authenticated = True

def go_to_admin_dashboard():
    """Navigate to admin dashboard"""
    st.session_state.page = "admin_dashboard"
    st.session_state.authenticated = True

def logout():
    """Logout and return to landing"""
    st.session_state.page = "landing"
    st.session_state.authenticated = False
    st.session_state.user_type = None
    st.session_state.username = None
    # Clear employee-specific session state
    st.session_state.emp_id = None
    st.session_state.emp_name = None
    st.session_state.email = None
    st.session_state.department = None
    st.rerun()

# -------------------------------------------------
# Page Routing Logic
# -------------------------------------------------

if st.session_state.page == "landing":
    from ui import landing_page
    landing_page.show(go_to_employee_login, go_to_admin_login)

elif st.session_state.page == "emp_login":
    from ui import emp_login
    emp_login.show(go_to_employee_dashboard, go_to_landing)

elif st.session_state.page == "admin_login":
    from ui import admin_login
    admin_login.show(go_to_admin_dashboard, go_to_landing)

elif st.session_state.page == "emp_dashboard":
    if st.session_state.authenticated:
        from ui import empoyee_ui
        empoyee_ui.show(logout)
    else:
        go_to_landing()
        st.rerun()

elif st.session_state.page == "admin_dashboard":
    if st.session_state.authenticated:
        from ui import admin_ui
        admin_ui.show(logout)
    else:
        go_to_landing()
        st.rerun()

else:
    go_to_landing()
    st.rerun()
