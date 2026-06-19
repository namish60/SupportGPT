import streamlit as st
import pandas as pd

def show(on_logout):
    """Admin dashboard"""
    # Page config already set in app.py

    # ---------------------------------------------------
    # CSS
    # ---------------------------------------------------

    st.markdown("""
    <style>

    .main-title{
        font-size:38px;
        font-weight:bold;
        color:#2563EB;
    }

    .sub-title{
        color:gray;
        font-size:17px;
    }

    .metric-card{
        text-align:center;
        font-size:22px;
        font-weight:bold;
    }

    .response-box{
        background-color:#F8F9FA;
        padding:20px;
        border-radius:10px;
        border:1px solid #E5E7EB;
    }

    </style>
    """,unsafe_allow_html=True)

        # ---------------------------------------------------
        # HEADER
        # ---------------------------------------------------

    col1,col2=st.columns([8,2])

    with col1:

        st.markdown(
            '<p class="main-title">🤖 SupportGPT</p>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<p class="sub-title">Enterprise AI Support Management Dashboard</p>',
            unsafe_allow_html=True
        )

    with col2:

        st.write("")
        st.write("")

        st.success("👤 Admin")

        if st.button("🚪 Logout", use_container_width=True, key="admin_logout_btn"):
            on_logout()

    st.divider()

    # ---------------------------------------------------
    # METRICS
    # ---------------------------------------------------

    c1,c2,c3,c4=st.columns(4)

    with c1:
        st.metric(
            "Pending Tickets",
            "14",
            "+2"
        )

    with c2:
        st.metric(
            "Approved Today",
            "8",
            "+3"
        )

    with c3:
        st.metric(
            "Rejected",
            "2",
            "-1"
        )

    with c4:
        st.metric(
            "AI Accuracy",
            "96%",
            "+1%"
        )

    st.divider()

    # ---------------------------------------------------
    # TABLE
    # ---------------------------------------------------

    st.subheader("📋 Pending Support Tickets")

    df=pd.DataFrame({

    "Ticket ID":[101,102,103],

    "Employee":["John","Rahul","Priya"],

    "Category":["VPN","Payroll","Password"],

    "Priority":["High","Medium","Low"],

    "Status":["Pending","Pending","Pending"]

    })

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ---------------------------------------------------
    # TICKET DETAILS
    # ---------------------------------------------------

    left,right=st.columns([2,1])

    with left:

        with st.container(border=True):

            st.subheader("🎫 Ticket Details")

            st.write("**Employee Name:** John Smith")

            st.write("**Employee ID:** EMP1023")

            st.write("**Department:** Engineering")

            st.write("**Issue Category:** VPN Issue")

            st.write("**Priority:** High")

            st.write("### Issue Description")

            st.info("""
Unable to connect to the company VPN after
changing my password.
Error Code : 720
Tried restarting laptop but issue persists.
""")

            st.write("")

            st.subheader("🤖 AI Generated Response")

            st.success("""
Hello John,

Based on the retrieved knowledge base,
please restart your VPN client and login again
using your updated password.

If the issue still exists,
please reinstall the VPN client or contact
Network Support.

Regards,
SupportGPT
""")

    with right:

        with st.container(border=True):

            st.subheader("📚 Retrieved Documents")

            st.success("vpn_troubleshooting.md")

            st.success("password_reset.md")

            st.success("network_access.md")

            st.write("")

            st.subheader("🛡 Guardrail Validation")

            st.success("✓ Hallucination Check Passed")

            st.success("✓ Sensitive Data Check Passed")

            st.success("✓ Company Policy Passed")

            st.success("✓ Confidence : 94%")

    st.divider()

    # ---------------------------------------------------
    # ACTIONS
    # ---------------------------------------------------

    b1,b2,b3=st.columns(3)

    with b1:

        st.button(
            "✅ Approve Response",
            use_container_width=True
        )

    with b2:

        st.button(
            "✏ Edit Response",
            use_container_width=True
        )

    with b3:

        st.button(
            "❌ Reject Response",
            use_container_width=True
        )