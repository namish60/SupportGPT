import streamlit as st
import time

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
    # Login Card
    # -------------------------------------------------

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        with st.container(border=True):

            st.markdown(
                '<p class="login-title">👨‍💼 Employee Login</p>',
                unsafe_allow_html=True
            )

            st.write("")

            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="emp_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="emp_password"
            )

            remember = st.checkbox("Remember Me")

            st.write("")

            login = st.button(
                "Login",
                use_container_width=True,
                key="emp_login_btn"
            )

            if login:

                if username == "" or password == "":

                    st.error("Please enter both username and password.")

                elif username == "employee" and password == "employee123":

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

                    st.session_state.username = username
                    st.success("Welcome to SupportGPT!")

                    time.sleep(1)
                    
                    on_login_success()
                    st.rerun()

                else:

                    st.error("Invalid Username or Password.")

            st.write("")

            if st.button(
                "⬅ Back to Home",
                use_container_width=True,
                key="emp_back_btn"
            ):
                on_back()
                st.rerun()

    # -------------------------------------------------
    # Footer
    # -------------------------------------------------

    st.write("")
    st.write("")
    st.caption("© 2026 SupportGPT | Employee Portal")