import streamlit as st

def show():

    ticket_id = st.session_state.get("selected_ticket")

    st.title("🤖 LLM Assignment Center")

    st.write(f"### Ticket ID: {ticket_id}")

    st.divider()

    llms = [
        {
            "name": "GPT-4o",
            "status": "🟢 Available",
            "load": "2 Tickets"
        },
        {
            "name": "Claude 4 Sonnet",
            "status": "🟢 Available",
            "load": "1 Ticket"
        },
        {
            "name": "Gemini 2.5 Pro",
            "status": "🟡 Busy",
            "load": "5 Tickets"
        },
        {
            "name": "Llama 3.3 70B",
            "status": "🔴 Offline",
            "load": "N/A"
        }
    ]

    for llm in llms:

        with st.container(border=True):

            c1, c2, c3, c4 = st.columns([3,2,2,2])

            with c1:
                st.subheader(llm["name"])

            with c2:
                st.write(llm["status"])

            with c3:
                st.write(llm["load"])

            with c4:
                st.button(
                    "Assign",
                    key=f"assign_{llm['name']}"
                )

    st.divider()

    if st.button("⬅ Back to Admin"):
        st.session_state["page"] = "admin_dashboard"
        st.rerun()