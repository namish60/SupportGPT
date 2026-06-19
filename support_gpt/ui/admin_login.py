import streamlit as st
import time

def show(on_login_success, on_back):
    """Admin login page"""
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
        '<p class="sub-title">Enterprise AI Support Administration Portal</p>',
        unsafe_allow_html=True
    )

    # -------------------------------------------------
    # Login Card
    # -------------------------------------------------

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        with st.container(border=True):

            st.markdown(
                '<p class="login-title">🛠️ Administrator Login</p>',
                unsafe_allow_html=True
            )

            st.write("")

            username = st.text_input(
                "Administrator Username",
                placeholder="Enter admin username",
                key="admin_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="admin_password"
            )

            remember = st.checkbox("Remember Me")

            st.write("")

            login = st.button(
                "Login",
                use_container_width=True,
                key="admin_login_btn"
            )

            if login:

                if username == "" or password == "":

                    st.error("Please enter both username and password.")

                elif username == "admin" and password == "admin123":

                    progress = st.progress(0)

                    status = st.empty()

                    steps = [
                        "🔐 Verifying administrator credentials...",
                        "🛡️ Loading administrator profile...",
                        "🤖 Connecting to SupportGPT Admin Console...",
                        "📊 Loading dashboard...",
                        "✅ Login Successful!"
                    ]

                    for i, step in enumerate(steps):
                        status.info(step)
                        progress.progress(int(((i + 1) / len(steps)) * 100))
                        time.sleep(0.6)

                    st.session_state.username = username
                    st.success("Welcome Administrator!")

                    time.sleep(1)
                    
                    on_login_success()
                    st.rerun()

                else:

                    st.error("Invalid Administrator Username or Password.")

            st.write("")

            if st.button(
                "⬅ Back to Home",
                use_container_width=True,
                key="admin_back_btn"
            ):
                on_back()
                st.rerun()

    # -------------------------------------------------
    # Footer
    # -------------------------------------------------

    st.write("")
    st.write("")
    st.caption("© 2026 SupportGPT | Administrator Portal")