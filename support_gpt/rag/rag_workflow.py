

# def run_rag_workflow(issue_description, llm_name):

#     print("Starting RAG workflow...")

#     # --------------------------------------------------
#     # STEP 1: RETRIEVE RELEVANT DOCUMENTS
#     # --------------------------------------------------

#     context = retrieve_documents(issue_description)

#     # --------------------------------------------------
#     # STEP 2: GENERATE RESPONSE USING SELECTED LLM
#     # --------------------------------------------------

#     answer = generate_response(
#         issue_description=issue_description,
#         context=context,
#         llm_name=llm_name
#     )

#     # --------------------------------------------------
#     # STEP 3: RETURN RESULT TO UI
#     # --------------------------------------------------

#     return {
#         "context": context,
#         "answer": answer
#     }


# # ======================================================
# # DOCUMENT RETRIEVAL
# # ======================================================

# def retrieve_documents(query):

#     """
#     This function will later contain:

#     1. Query embedding
#     2. Vector database search
#     3. Top-K relevant document chunks
#     """

#     # Temporary test context

#     context = """
#     VPN Troubleshooting Guide:

#     1. Verify that the employee has an active internet connection.

#     2. Restart the VPN client.

#     3. Verify the employee credentials.

#     4. If the problem continues, contact the IT Help Desk.
#     """

#     return context


# # ======================================================
# # LLM RESPONSE GENERATION
# # ======================================================

# def generate_response(
#     issue_description,
#     context,
#     llm_name
# ):

#     """
#     This function will later call the actual LLM API.
#     """

#     answer = f"""
# Based on the available company knowledge base:

# {context}

# Recommended solution for the issue:

# {issue_description}

# Please follow the troubleshooting steps mentioned
# in the knowledge base.

# LLM Used: {llm_name}
# """

#     return answer


import os

from dotenv import load_dotenv

from langchain_nvidia_ai_endpoints import ChatNVIDIA

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ======================================================
# LOAD ENVIRONMENT VARIABLES
# ======================================================

load_dotenv()


# ======================================================
# CONFIGURATION
# ======================================================

# NVIDIA API Key
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")


# NVIDIA model
NVIDIA_MODEL = "meta/llama-3.1-70b-instruct"


# Location of saved FAISS vector database
VECTOR_STORE_PATH = "rag/vector_store"


# ======================================================
# EMBEDDING MODEL
# ======================================================

print("Loading embedding model...")

embeddings = HuggingFaceEmbeddings(

    model_name="sentence-transformers/all-MiniLM-L6-v2"

)


# ======================================================
# LOAD VECTOR DATABASE
# ======================================================

print("Loading vector database...")

vectorstore = FAISS.load_local(

    VECTOR_STORE_PATH,

    embeddings,

    allow_dangerous_deserialization=True

)


print("Vector database loaded successfully.")


# ======================================================
# MAIN RAG WORKFLOW
# ======================================================

def run_rag_workflow(

    issue_description,

    llm_name

):

    """

    Complete RAG pipeline:

    1. Retrieve relevant knowledge
    2. Generate answer using NVIDIA LLM
    3. Return context and answer

    """


    print("Starting RAG workflow...")


    # --------------------------------------------------
    # STEP 1: RETRIEVE RELEVANT DOCUMENTS
    # --------------------------------------------------

    context = retrieve_documents(

        issue_description

    )


    # --------------------------------------------------
    # STEP 2: GENERATE RESPONSE
    # --------------------------------------------------

    answer = generate_response(

        issue_description=issue_description,

        context=context,

        llm_name=llm_name

    )


    # --------------------------------------------------
    # STEP 3: RETURN RESULT
    # --------------------------------------------------

    return {

        "context": context,

        "answer": answer

    }


# ======================================================
# DOCUMENT RETRIEVAL
# ======================================================

def retrieve_documents(

    query

):

    """

    Takes the employee's issue and searches
    the FAISS vector database.

    Returns the most relevant document chunks.

    """


    print(

        "Searching knowledge base for relevant documents..."

    )


    # Retrieve top 3 relevant chunks

    retrieved_documents = vectorstore.similarity_search(

        query,

        k=3

    )


    # --------------------------------------------------
    # HANDLE NO RESULTS
    # --------------------------------------------------

    if not retrieved_documents:

        return (

            "No relevant information was found "
            "in the company knowledge base."

        )


    # --------------------------------------------------
    # COMBINE DOCUMENT CHUNKS
    # --------------------------------------------------

    context_parts = []


    for index, document in enumerate(

        retrieved_documents,

        start=1

    ):


        source = document.metadata.get(

            "source",

            "Unknown source"

        )


        context_parts.append(

            f"""

--- Knowledge Chunk {index} ---
Source: {source}

{document.page_content}

"""

        )


    context = "\n".join(

        context_parts

    )


    print(

        f"Retrieved {len(retrieved_documents)} "
        "relevant document chunks."

    )


    return context


# ======================================================
# LLM RESPONSE GENERATION
# ======================================================

def generate_response(

    issue_description,

    context,

    llm_name

):

    """

    Sends the employee issue and retrieved knowledge
    to the NVIDIA 70B model.

    """


    print(

        f"Generating response using {llm_name}..."

    )


    # --------------------------------------------------
    # INITIALIZE NVIDIA LLM
    # --------------------------------------------------

    llm = ChatNVIDIA(

        model=NVIDIA_MODEL,

        api_key=NVIDIA_API_KEY,

        temperature=0.2,

        max_tokens=1024

    )


    # --------------------------------------------------
    # CREATE PROMPT
    # --------------------------------------------------

    prompt = f"""

You are SupportGPT, an internal enterprise IT support assistant.

Your task is to help employees resolve their technical issues.

You MUST follow these rules:

1. Use the provided company knowledge base as your primary source.

2. Do not invent company policies or troubleshooting procedures.

3. Give clear, practical, step-by-step instructions.

4. If the knowledge base does not contain enough information,
   clearly state that the issue requires human IT support.

5. Do not mention the internal RAG system, vector database,
   embeddings, or document retrieval process.

6. Be professional and concise.

7. If multiple troubleshooting steps exist, present them
   in a numbered list.

--------------------------------------------------

COMPANY KNOWLEDGE BASE:

{context}

--------------------------------------------------

EMPLOYEE ISSUE:

{issue_description}

--------------------------------------------------

Generate the support response.

Use this format:

Issue Understanding:
Briefly explain what you understand about the employee's problem.

Recommended Steps:
Provide the relevant troubleshooting steps.

Further Assistance:
Explain what the employee should do if the issue is not resolved.

"""


    # --------------------------------------------------
    # CALL NVIDIA MODEL
    # --------------------------------------------------

    response = llm.invoke(

        prompt

    )


    # --------------------------------------------------
    # EXTRACT RESPONSE TEXT
    # --------------------------------------------------

    answer = response.content


    return answer