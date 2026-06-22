import streamlit as st
import uuid
from datetime import datetime
from database import save_ticket, init_database

def show(on_logout):
    """Employee dashboard"""
    # Page Configuration
    # Page config already set in app.py

    # Custom Styling
    st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.main-title {
    text-align: center;
    font-size: 72px;
    font-weight: 900;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
    letter-spacing: 2px;
}
            
.sub-title {
    text-align: center;
    font-size: 20px;
    color: #555;
    margin-bottom: 30px;
    font-weight: 500;
}

.stContainer {
    background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,245,255,0.95) 100%);
    border-radius: 15px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

.stButton>button {
    width: 100%;
    height: 50px;
    font-size: 18px;
}
            
.stButton {
    display: flex;
    justify-content: center;
}

.stButton > button {
    width: 200px;
    height: 60px;
    font-size: 20px;
    font-weight: bold;
    border-radius: 10px;
    background: linear-gradient(135deg, #90EE90 0%, #76D776 100%);
    border: 2px solid #228B22;
    color: #1a5c1a;
    box-shadow: 0 4px 15px rgba(34, 139, 34, 0.3);
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #76D776 0%, #5cbb5c 100%);
    border: 3px solid #1a5c1a;
    box-shadow: 0 6px 20px rgba(34, 139, 34, 0.5);
    transform: translateY(-2px);
}

.stTextInput > div > div > input {
    border-radius: 8px;
    border: 2px solid #e0e0e0;
    font-size: 16px;
}

.stTextInput > div > div > input:focus {
    border: 2px solid #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.stSelectbox > div > div > select {
    border-radius: 8px;
    border: 2px solid #e0e0e0;
}

.stTextArea > div > div > textarea {
    border-radius: 8px;
    border: 2px solid #e0e0e0;
    font-size: 15px;
}

.stTextArea > div > div > textarea:focus {
    border: 2px solid #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.priority-badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 14px;
}

.ticket-id {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px 20px;
    border-radius: 10px;
    font-size: 18px;
    font-weight: bold;
    text-align: center;
    margin: 15px 0;
}

.helpdesk-footer {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border: 2px solid #667eea;
    border-radius: 12px;
    padding: 20px;
    margin-top: 30px;
    text-align: center;
}

.helpdesk-title {
    color: #667eea;
    font-weight: bold;
    font-size: 16px;
    margin-bottom: 10px;
}

.helpdesk-contact {
    color: #555;
    font-size: 14px;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

    # Header
    st.markdown(
        '<p class="main-title">🤖 Welcome to SupportGPT</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="sub-title">AI Powered Employee Support Assistant</p>',
        unsafe_allow_html=True
    )

    # Logout button in header
    col_logout = st.columns([8, 2])
    with col_logout[1]:
        if st.button("🚪 Logout", use_container_width=True, key="emp_logout_btn"):
            on_logout()

    # Card-like Container
    with st.container(border=True):

        st.subheader("📝 Raise a Support Ticket")
        
        # Display logged-in employee info
        st.info(f"👤 **Logged in as:** {st.session_state.emp_name} ({st.session_state.emp_id})")

        col1, col2 = st.columns(2)

        with col1:
            # Display employee name (read-only)
            st.text_input(
                "Employee Name",
                value=st.session_state.emp_name,
                disabled=True
            )

            # Display employee ID (read-only)
            st.text_input(
                "Employee ID",
                value=st.session_state.emp_id,
                disabled=True
            )

        with col2:
            # Display department (read-only)
            st.text_input(
                "Department",
                value=st.session_state.department,
                disabled=True
            )

            priority = st.selectbox(
                "Priority",
                [
                    "🟢 Low",
                    "🟡 Medium",
                    "🔶 High"
                ]
            )

        issue_description = st.text_area(
            "Describe Your Issue",
            height=150,
            placeholder="""
Example:
I am unable to connect to the VPN while working remotely.
"""
        )

        # Center the submit button at the bottom
        button_col1, button_col2, button_col3 = st.columns([1, 1, 1])
        with button_col2:
            submitted = st.button(" Submit Ticket")

    if submitted:

        if not issue_description:

            st.error("Please describe your issue.")

        else:
            with st.spinner("🔄 Processing your ticket..."):
                import time
                time.sleep(1)  # Simulate processing time

                # Generate unique ticket ID
                ticket_id = f"TKT-{str(uuid.uuid4())[:8].upper()}-{datetime.now().strftime('%Y%m%d')}"
                
                # Save ticket to database using session state values
                success = save_ticket(
                    ticket_id=ticket_id,
                    emp_name=st.session_state.emp_name,
                    emp_id=st.session_state.emp_id,
                    department=st.session_state.department,
                    priority=priority,
                    issue_description=issue_description
                )
            
            if success:
                st.success("✅ Ticket Submitted Successfully!")

                # Display Ticket ID
                st.markdown(f'<div class="ticket-id">🎫 Ticket ID: {ticket_id}</div>', unsafe_allow_html=True)

                st.write("### 📋 Ticket Summary")

                st.write(f"**Employee Name:** {st.session_state.emp_name}")
                st.write(f"**Employee ID:** {st.session_state.emp_id}")
                st.write(f"**Department:** {st.session_state.department}")
                st.write(f"**Priority:** {priority}")
                st.write(f"**Issue Description:** {issue_description}")
                st.write(f"**Submitted At:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                st.error("❌ Error saving ticket to database. Please try again.")

    # Help Desk Contact Info Footer
    st.markdown("""
<div class="helpdesk-footer">
    <div class="helpdesk-title">📞 Help Desk Contact Information</div>
    <div class="helpdesk-contact">📧 <strong>Email:</strong> support@company.com</div>
    <div class="helpdesk-contact">📱 <strong>Phone:</strong> +1 (555) 123-4567</div>
    <div class="helpdesk-contact">⏰ <strong>Hours:</strong> Monday - Friday, 9:00 AM - 6:00 PM</div>
    <div class="helpdesk-contact">🔗 <strong>Live Chat:</strong> Available during business hours</div>
</div>
""", unsafe_allow_html=True)