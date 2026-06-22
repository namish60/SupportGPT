import streamlit as st
import time
from database import authenticate_employee, register_employee, get_employee_by_username

def show(on_login_success, on_back):

    # -------------------------------------------------
    # CSS
    # -------------------------------------------------

    st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#2563EB;
}

.sub-title{
    text-align:center;
    color:gray;
    font-size:18px;
    margin-bottom:30px;
}

.login-title{
    text-align:center;
    font-size:28px;
    font-weight:bold;
}

.stButton>button{
    width:100%;
    height:48px;
    border-radius:10px;
    font-size:17px;
    font-weight:bold;
}

.divider-text {
    text-align: center;
    color: gray;
    margin: 20px 0;
}

</style>
""", unsafe_allow_html=True)

    # -------------------------------------------------
    # Header
    # -------------------------------------------------

    st.markdown(
        '<p class="main-title">🤖 SupportGPT</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="sub-title">AI Powered Enterprise Support Assistant</p>',
        unsafe_allow_html=True
    )

    # -------------------------------------------------
    # Login / Register Tabs
    # -------------------------------------------------

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

        # ========== LOGIN TAB ==========
        with tab1:

            with st.container(border=True):

                st.markdown(
                    '<p class="login-title">👨‍💼 Employee Login</p>',
                    unsafe_allow_html=True
                )

                st.write("")

                username = st.text_input(
                    "Username",
                    placeholder="Enter your username",
                    key="emp_username_login"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    key="emp_password_login"
                )

                st.write("")

                login = st.button(
                    "Login",
                    use_container_width=True,
                    key="emp_login_btn"
                )

                if login:

                    if username == "" or password == "":

                        st.error("Please enter both username and password.")

                    else:
                        # Authenticate employee credentials
                        employee = authenticate_employee(username, password)
                        
                        if employee:
                            # Login successful
                            progress = st.progress(0)

                            status = st.empty()

                            steps = [
                                "🔐 Authenticating credentials...",
                                "👤 Loading employee profile...",
                                "🤖 Connecting to SupportGPT...",
                                "✅ Login Successful!"
                            ]

                            for i in range(4):
                                status.info(steps[i])
                                progress.progress((i+1)*25)
                                time.sleep(0.6)

                            # Store employee details in session state
                            st.session_state.username = employee[1]
                            st.session_state.emp_id = employee[0]
                            st.session_state.emp_name = employee[3]
                            st.session_state.email = employee[4]
                            st.session_state.department = employee[5]
                            
                            st.success("Welcome to SupportGPT!")

                            time.sleep(1)
                            
                            on_login_success()
                            st.rerun()

                        else:

                            st.error("❌ Invalid Username or Password.")

                st.write("")

                if st.button(
                    "⬅ Back to Home",
                    use_container_width=True,
                    key="emp_back_btn_login"
                ):
                    on_back()
                    st.rerun()

        # ========== REGISTER TAB ==========
        with tab2:

            with st.container(border=True):

                st.markdown(
                    '<p class="login-title">📝 Create Account</p>',
                    unsafe_allow_html=True
                )

                st.write("")

                emp_id = st.text_input(
                    "Employee ID *",
                    placeholder="e.g., EMP001",
                    key="emp_id_register"
                )

                emp_name = st.text_input(
                    "Full Name *",
                    placeholder="John Doe",
                    key="emp_name_register"
                )

                col1_reg, col2_reg = st.columns(2)

                with col1_reg:
                    username_reg = st.text_input(
                        "Username *",
                        placeholder="john_doe",
                        key="emp_username_register"
                    )

                with col2_reg:
                    password_reg = st.text_input(
                        "Password * (min 6 chars)",
                        type="password",
                        placeholder="Create a password",
                        key="emp_password_register"
                    )

                col3_reg, col4_reg = st.columns(2)

                with col3_reg:
                    email = st.text_input(
                        "Email",
                        placeholder="john@company.com",
                        key="emp_email_register"
                    )

                with col4_reg:
                    department = st.text_input(
                        "Department *",
                        placeholder="Engineering",
                        key="emp_dept_register"
                    )

                st.write("")

                register = st.button(
                    "Create Account & Login",
                    use_container_width=True,
                    key="emp_register_btn"
                )

                if register:

                    # Validation
                    if not emp_id or not emp_name or not username_reg or not password_reg or not department:
                        st.error("❌ Please fill all required fields (marked with *).")

                    elif len(password_reg) < 6:
                        st.error("❌ Password must be at least 6 characters long.")

                    else:
                        # Check if username already exists
                        existing_user = get_employee_by_username(username_reg)

                        if existing_user:
                            st.error("❌ Username already exists. Please choose a different one.")

                        else:
                            # Register new employee
                            success = register_employee(
                                emp_id=emp_id,
                                username=username_reg,
                                password=password_reg,
                                emp_name=emp_name,
                                email=email,
                                department=department
                            )

                            if success:
                                # Registration successful - auto login
                                progress = st.progress(0)

                                status = st.empty()

                                steps = [
                                    "✅ Account created successfully!",
                                    "🔐 Authenticating...",
                                    "👤 Loading your profile...",
                                    "🤖 Connecting to SupportGPT..."
                                ]

                                for i in range(4):
                                    status.info(steps[i])
                                    progress.progress((i+1)*25)
                                    time.sleep(0.6)

                                # Auto-login
                                st.session_state.username = username_reg
                                st.session_state.emp_id = emp_id
                                st.session_state.emp_name = emp_name
                                st.session_state.email = email
                                st.session_state.department = department

                                st.success(f"🎉 Welcome {emp_name}!")

                                time.sleep(1)
                                
                                on_login_success()
                                st.rerun()

                            else:
                                st.error("❌ Registration failed. Employee ID might already exist.")

                st.write("")

                if st.button(
                    "⬅ Back to Home",
                    use_container_width=True,
                    key="emp_back_btn_register"
                ):
                    on_back()
                    st.rerun()

    # -------------------------------------------------
    # Footer
    # -------------------------------------------------

    st.write("")
    st.write("")
    st.caption("© 2026 SupportGPT | Employee Portal")