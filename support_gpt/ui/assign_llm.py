# import streamlit as st

# def show():

#     ticket_id = st.session_state.get("selected_ticket")

#     st.title("🤖 LLM Assignment Center")

#     st.write(f"### Ticket ID: {ticket_id}")

#     st.divider()

#     llms = [
#         {
#             "name": "GPT-4o",
#             "status": "🟢 Available",
#             "load": "2 Tickets"
#         },
#         {
#             "name": "Claude 4 Sonnet",
#             "status": "🟢 Available",
#             "load": "1 Ticket"
#         },
#         {
#             "name": "Gemini 2.5 Pro",
#             "status": "🟡 Busy",
#             "load": "5 Tickets"
#         },
#         {
#             "name": "Llama 3.3 70B",
#             "status": "🔴 Offline",
#             "load": "N/A"
#         }
#     ]

#     for llm in llms:

#         with st.container(border=True):

#             c1, c2, c3, c4 = st.columns([3,2,2,2])

#             with c1:
#                 st.subheader(llm["name"])

#             with c2:
#                 st.write(llm["status"])

#             with c3:
#                 st.write(llm["load"])

#             with c4:
#                 st.button(
#                     "Assign",
#                     key=f"assign_{llm['name']}"
#                 )

#     st.divider()

#     if st.button("⬅ Back to Admin"):
#         st.session_state["page"] = "admin_dashboard"
#         st.rerun()

import streamlit as st

from database import get_ticket_by_id

# Import your RAG workflow
from rag.rag_workflow import run_rag_workflow


def show():

    ticket_id = st.session_state.get("selected_ticket")

    st.title("🤖 LLM Assignment Center")

    st.write(f"### Ticket ID: `{ticket_id}`")

    st.divider()

    # --------------------------------------------------
    # FETCH TICKET DETAILS
    # --------------------------------------------------

    ticket = get_ticket_by_id(ticket_id)

    if not ticket:

        st.error("Ticket not found.")

        if st.button(
            "⬅ Back to Admin",
            key="back_admin_not_found"
        ):
            st.session_state["page"] = "admin_dashboard"
            st.rerun()

        return

    # Based on your database structure
    issue_description = ticket[5]

    st.info(
        f"📝 **Issue:** {issue_description}"
    )

    st.divider()

    # --------------------------------------------------
    # LLM
    # --------------------------------------------------

    st.subheader("🤖 Available LLM")

    llm_name = "GPT-4o"

    with st.container(border=True):

        c1, c2, c3, c4 = st.columns([3, 2, 2, 2])

        with c1:
            st.subheader("GPT-4o")

        with c2:
            st.write("🟢 Available")

        with c3:
            st.write("Load: Ready")

        with c4:

            assign_clicked = st.button(
                "🚀 Assign",
                key="assign_gpt4o",
                width="stretch"
            )

            if assign_clicked:

                # Store selected LLM
                st.session_state["assigned_llm"] = llm_name

                # --------------------------------------------------
                # START RAG WORKFLOW
                # --------------------------------------------------

                with st.spinner(
                    "🤖 GPT-4o is processing the ticket..."
                ):

                    result = run_rag_workflow(

                        issue_description=issue_description,

                        llm_name=llm_name

                    )

                # Store result
                st.session_state["rag_result"] = result

                st.success(
                    "✅ GPT-4o assigned successfully!"
                )

                st.rerun()

    # --------------------------------------------------
    # RAG RESULT
    # --------------------------------------------------

    if "rag_result" in st.session_state:

        result = st.session_state["rag_result"]

        st.divider()

        st.header("🧠 RAG Workflow Result")

        # --------------------------------------------------
        # SELECTED LLM
        # --------------------------------------------------

        st.subheader("🤖 Assigned LLM")

        st.success(
            st.session_state["assigned_llm"]
        )

        # --------------------------------------------------
        # RETRIEVED DOCUMENT CONTEXT
        # --------------------------------------------------

        st.subheader("📚 Retrieved Knowledge")

        with st.expander(
            "View Retrieved Document Chunks",
            expanded=True
        ):

            st.write(
                result["context"]
            )

        # --------------------------------------------------
        # FINAL AI RESPONSE
        # --------------------------------------------------

        st.subheader("💬 AI Generated Response")

        with st.container(border=True):

            st.write(
                result["answer"]
            )

    # --------------------------------------------------
    # BACK BUTTON
    # --------------------------------------------------

    st.divider()

    if st.button(
        "⬅ Back to Admin",
        key="back_to_admin"
    ):

        # Clear previous result
        st.session_state.pop(
            "rag_result",
            None
        )

        st.session_state.pop(
            "assigned_llm",
            None
        )

        st.session_state["page"] = "admin_dashboard"

        st.rerun()