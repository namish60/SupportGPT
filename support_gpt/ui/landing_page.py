import streamlit as st

def show(on_employee_login, on_admin_login):
    # -------------------------------------------------
    # Custom CSS
    # -------------------------------------------------

    st.markdown("""
    <style>

    .main-title{
        text-align:center;
        font-size:48px;
        font-weight:bold;
        color:#2563EB;
    }

    .subtitle{
        text-align:center;
        font-size:20px;
        color:gray;
        margin-bottom:30px;
    }

    .description{
        text-align:center;
        font-size:17px;
        color:#666666;
        margin-bottom:40px;
    }

    .portal-title{
        text-align:center;
        font-size:26px;
        font-weight:bold;
        color:#1f2937;
    }

    .portal-text{
        font-size:16px;
        color:#555555;
    }

    .stButton>button{
        width:100%;
        height:50px;
        font-size:18px;
        font-weight:bold;
        border-radius:10px;
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
        '<p class="subtitle">AI Powered Enterprise Support Assistant</p>',
        unsafe_allow_html=True
    )

    st.markdown(
    """
    <div class="description">
    Get instant AI assistance for IT, HR, Finance, Operations and Workplace related issues.
    </div>
    """,
    unsafe_allow_html=True
    )

    st.divider()

    # -------------------------------------------------
    # Two Portal Cards
    # -------------------------------------------------

    left, right = st.columns(2, gap="large")

    # ================= Employee =====================

    with left:

        with st.container(border=True):

            st.markdown(
                "<h1 style='text-align:center;'>👨‍💼</h1>",
                unsafe_allow_html=True
            )

            st.markdown(
                '<p class="portal-title">Employee Portal</p>',
                unsafe_allow_html=True
            )

            st.write("")

            st.markdown("""
    ✔ Raise Support Tickets

    ✔ Get AI Powered Assistance

    ✔ Track Ticket Status

    ✔ View Approved Responses

    ✔ 24 × 7 Employee Support
    """)

            st.write("")
            st.write("")

            if st.button(
                "Employee Login",
                use_container_width=True,
                key="emp_login_btn"
            ):
                on_employee_login()
                st.rerun()

    # ================= Admin =====================

    with right:

        with st.container(border=True):

            st.markdown(
                "<h1 style='text-align:center;'>🛠️</h1>",
                unsafe_allow_html=True
            )

            st.markdown(
                '<p class="portal-title">Administrator Portal</p>',
                unsafe_allow_html=True
            )

            st.write("")

            st.markdown("""
    ✔ Review AI Generated Responses

    ✔ Approve / Reject Tickets

    ✔ Manage Knowledge Base

    ✔ Monitor Support Analytics

    ✔ Human-in-the-loop Validation
    """)

            st.write("")
            st.write("")

            if st.button(
                "Administrator Login",
                use_container_width=True,
                key="admin_login_btn"
            ):
                on_admin_login()
                st.rerun()

    st.divider()

    st.caption("© 2026 SupportGPT | Enterprise AI Support Platform")