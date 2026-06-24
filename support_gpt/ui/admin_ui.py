import streamlit as st
import pandas as pd
from database import get_all_tickets, get_ticket_by_id, update_ticket_status, get_ticket_count

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
    
    # Get tickets from database
    all_tickets = get_all_tickets()
    open_tickets = [t for t in all_tickets if t[7] == 'Open']  # status is at index 7
    closed_tickets = [t for t in all_tickets if t[7] == 'Closed']

    c1,c2,c3,c4=st.columns(4)

    with c1:
        st.metric(
            "Total Tickets",
            len(all_tickets),
            f"+{len(open_tickets)} open"
        )

    with c2:
        st.metric(
            "Open Tickets",
            len(open_tickets),
            "Pending Response"
        )

    with c3:
        st.metric(
            "Resolved Tickets",
            len(closed_tickets),
            "Completed"
        )

    with c4:
        st.metric(
            "System Status",
            "Operational",
            "✓ All Good"
        )

    st.divider()

    # ---------------------------------------------------
    # TABLE
    # ---------------------------------------------------

    st.subheader("📋 All Support Tickets")

    if all_tickets:
        # Prepare data for display
        table_data = []
        for ticket in all_tickets:
            table_data.append({
                "Ticket ID": ticket[0],
                "Employee Name": ticket[1],
                "Employee ID": ticket[2],
                "Department": ticket[3],
                "Priority": ticket[4],
                "Status": ticket[7],
                "Submitted": ticket[6]
            })

        df = pd.DataFrame(table_data)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No tickets found in the system yet.")

    st.divider()

    # ---------------------------------------------------
    # TICKET DETAILS & SELECTION
    # ---------------------------------------------------

    if all_tickets:
        st.subheader("🔍 Ticket Details Viewer")
        
        # Create a selectbox to choose a ticket
        ticket_options = {f"{t[0]} - {t[1]}": t[0] for t in all_tickets}
        selected_ticket_label = st.selectbox(
            "Select a ticket to view details:",
            list(ticket_options.keys())
        )
        
        selected_ticket_id = ticket_options[selected_ticket_label]
        selected_ticket = get_ticket_by_id(selected_ticket_id)
        
        if selected_ticket:
            left,right=st.columns([2,1])

            with left:

                with st.container(border=True):

                    st.subheader("🎫 Ticket Details")

                    st.write(f"**Ticket ID:** {selected_ticket[0]}")
                    st.write(f"**Employee Name:** {selected_ticket[1]}")
                    st.write(f"**Employee ID:** {selected_ticket[2]}")
                    st.write(f"**Department:** {selected_ticket[3]}")
                    st.write(f"**Priority:** {selected_ticket[4]}")
                    st.write(f"**Status:** {selected_ticket[7]}")
                    st.write(f"**Submitted Date:** {selected_ticket[6]}")

                    st.write("### 📝 Issue Description")

                    st.info(selected_ticket[5])

            with right:

                with st.container(border=True):

                    st.subheader("⚙️ Ticket Actions")

                    # Status update buttons
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("✅ Mark as Resolved", use_container_width=True):
                            if update_ticket_status(selected_ticket_id, 'Closed'):
                                st.success("Ticket marked as resolved!")
                                st.rerun()
                    
                    # with col2:
                    #     if st.button("🔄 Reopen Ticket", use_container_width=True):
                    #         if update_ticket_status(selected_ticket_id, 'Open'):
                    #             st.success("Ticket reopened!")
                    #             st.rerun()

                    with col2:

                        if st.button("🔄 Reopen Ticket", use_container_width=True):
                            if update_ticket_status(selected_ticket_id, 'Open'):
                                st.success("Ticket reopened!")
                                st.rerun()

                    # ==========================
                    # ASSIGN LLM BUTTON
                    # ==========================

                    st.divider()

                    st.subheader("🤖 LLM Assignment")

                    if st.button(
                        "🚀 Assign LLM",
                        use_container_width=True,
                        type="primary",
                        key=f"assign_llm_{selected_ticket_id}"
                    ):
                        st.session_state["page"] = "assign_llm"
                        st.session_state["selected_ticket"] = selected_ticket_id
                        st.rerun()
                        

                    st.divider()

                    st.subheader("📊 Stats")
                    st.write(f"**Current Status:** {selected_ticket[7]}")
                    st.write(f"**Priority Level:** {selected_ticket[4]}")

                    

            st.divider()

            # ---------------------------------------------------
            # ACTIONS
            # ---------------------------------------------------

            b1,b2,b3=st.columns(3)

            with b1:
                if st.button(
                    "✅ Approve Response",
                    use_container_width=True
                ):
                    st.success("Response approved!")

            with b2:
                if st.button(
                    "✏ Edit Response",
                    use_container_width=True
                ):
                    st.info("Edit mode would open here")

            with b3:
                if st.button(
                    "❌ Reject Response",
                    use_container_width=True
                ):
                    st.error("Response rejected")