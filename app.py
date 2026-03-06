# import os
# import tempfile
# import streamlit as st
# from dotenv import load_dotenv

# from rag import build_vectorstore, answer_question
# from agent import generate_business_model

# load_dotenv()

# def check_api_key():
#     key = os.environ.get("OPENAI_API_KEY")
#     return key is not None and key.strip() != ""

# def save_uploaded_file(uploaded_file) -> str:
#     suffix = uploaded_file.name
#     tmp = tempfile.NamedTemporaryFile(delete=False, suffix="_" + suffix)
#     tmp.write(uploaded_file.getbuffer())
#     tmp.flush()
#     tmp.close()
#     return tmp.name

# def display_conversation():
#     """Display conversation history as a chat."""
#     history = st.session_state.get("conversation_history", [])
#     for msg in history:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])

# def main():
#     st.set_page_config(page_title="Agentic AI RAG Q&A Agent")
#     st.title("Agentic AI RAG Q&A Agent")

#     if not check_api_key():
#         st.error("OPENAI_API_KEY not found. Set it in a .env file.")
#         st.stop()

#     # Initialize conversation history
#     if "conversation_history" not in st.session_state:
#         st.session_state["conversation_history"] = []

#     tab1, tab2 = st.tabs(["Q&A Chat", "Business Model Generator"])

#     with tab1:
#         uploaded = st.file_uploader("Upload a PDF file", type=["pdf"], key="qa_uploader")


#     # uploaded = st.file_uploader("Upload a PDF file", type=["pdf"])

#         if uploaded is not None:
#             st.info(f"Uploaded: {uploaded.name}")
#             pdf_path = save_uploaded_file(uploaded)

#             if st.button("Build Knowledge Base", key="build_kb"):
#                 try:
#                     with st.spinner("Building vector store..."):
#                         vectordb = build_vectorstore(pdf_path)
#                     st.success("Knowledge base built successfully!")
#                     st.session_state["vectordb"] = vectordb
#                     # Reset conversation on new PDF
#                     st.session_state["conversation_history"] = []
#                 except Exception as e:
#                     st.error(f"Error building knowledge base: {e}")

#         if "vectordb" in st.session_state:
#             st.markdown("---")
#             st.subheader("Chat with Document")
            
#             # Input for new question
#             question = st.chat_input("Ask a question about the document:")

#             if question:
#                 # add user message first so it's shown during processing
#                 st.session_state["conversation_history"].append({
#                     "role": "user",
#                     "content": question
#                 })

#                 try:
#                     with st.spinner("Thinking..."):
#                         vectordb = st.session_state["vectordb"]
#                         answer = answer_question(
#                             vectordb, 
#                             question,
#                             conversation_history=st.session_state["conversation_history"][:-1]  # Exclude current user msg
#                         )

#                     # add assistant response to history
#                     st.session_state["conversation_history"].append({
#                         "role": "assistant",
#                         "content": answer
#                     })

#                     # immediately display the assistant response as well
#                     with st.chat_message("assistant"):
#                         st.write(answer)

#                 except Exception as e:
#                     st.error(f"Error: {e}")
#                     # remove the user message if there was an error
#                     if st.session_state["conversation_history"]:
#                         st.session_state["conversation_history"].pop()

#         # now show the full conversation including new turn
#         display_conversation()
        
#         # Option to clear conversation
#         if st.session_state["conversation_history"]:
#             if st.button("Clear Conversation"):
#                 st.session_state["conversation_history"] = []
#                 # the page will rerun automatically on interaction

#         with tab2:
#             # New business model generation logic
#             st.subheader("Generate Business Model from PDF")
#             uploaded_bm = st.file_uploader("Upload a PDF file for business model generation", type=["pdf"], key="bm_uploader")

#             if uploaded_bm is not None:
#                 st.info(f"Uploaded: {uploaded_bm.name}")
#                 pdf_path_bm = save_uploaded_file(uploaded_bm)

#                 if st.button("Generate Business Model", key="generate_bm"):
#                     try:
#                         with st.spinner("Extracting text and generating business model..."):
#                             # Extract text from PDF (reuse logic from build_vectorstore)
#                             from pypdf import PdfReader
#                             reader = PdfReader(pdf_path_bm)
#                             document_content = ""
#                             for page in reader.pages:
#                                 document_content += page.extract_text() + "\n"
                            
#                             # Limit to first 10,000 characters to avoid token limits
#                             document_content = document_content[:10000]

#                             business_model = generate_business_model(document_content)
                            
#                         st.success("Business model generated!")
#                         st.session_state["business_model"] = business_model
                        
#                     except Exception as e:
#                         st.error(f"Error generating business model: {e}")

#             # Display generated business model
#             if "business_model" in st.session_state:
#                 st.markdown("### Generated Business Model")
#                 st.text_area("Business Model Output", st.session_state["business_model"], height=400, key="bm_output")


# if __name__ == "__main__":
#     main()




import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from rag import build_vectorstore, answer_question
from agent import generate_business_model

load_dotenv()


def check_api_key() -> bool:
    key = os.environ.get("OPENAI_API_KEY")
    return key is not None and key.strip() != ""


def save_uploaded_file(uploaded_file) -> str:
    suffix = os.path.splitext(uploaded_file.name)[1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.getbuffer())
    tmp.flush()
    tmp.close()
    return tmp.name


def display_conversation():
    history = st.session_state.get("conversation_history", [])
    for msg in history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])


def extract_text_from_pdf(pdf_path: str) -> str:
    from pypdf import PdfReader

    reader = PdfReader(pdf_path)
    text_parts = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)

    return "\n".join(text_parts)


def init_session_state():
    if "conversation_history" not in st.session_state:
        st.session_state["conversation_history"] = []

    if "vectordb" not in st.session_state:
        st.session_state["vectordb"] = None

    if "business_model" not in st.session_state:
        st.session_state["business_model"] = ""

    if "qa_pdf_name" not in st.session_state:
        st.session_state["qa_pdf_name"] = None

    if "bm_pdf_name" not in st.session_state:
        st.session_state["bm_pdf_name"] = None


def main():
    st.set_page_config(page_title="Agentic AI RAG Q&A Agent", page_icon="🤖", layout="wide")
    st.title("Agentic AI RAG Q&A Agent")

    if not check_api_key():
        st.error("OPENAI_API_KEY not found. Please set it in your .env file.")
        st.stop()

    init_session_state()

    tab1, tab2 = st.tabs(["Q&A Chat", "Business Model Generator"])

    # -------------------------
    # TAB 1: Q&A CHAT
    # -------------------------
    with tab1:
        st.subheader("Upload PDF and Chat with It")

        uploaded = st.file_uploader(
            "Upload a PDF file",
            type=["pdf"],
            key="qa_uploader"
        )

        if uploaded is not None:
            st.info(f"Uploaded: {uploaded.name}")

            # Rebuild only if a new file is uploaded
            if st.session_state["qa_pdf_name"] != uploaded.name:
                st.session_state["qa_pdf_name"] = uploaded.name
                st.session_state["vectordb"] = None
                st.session_state["conversation_history"] = []

            if st.button("Build Knowledge Base", key="build_kb"):
                try:
                    pdf_path = save_uploaded_file(uploaded)

                    with st.spinner("Building vector store..."):
                        vectordb = build_vectorstore(pdf_path)

                    st.session_state["vectordb"] = vectordb
                    st.session_state["conversation_history"] = []
                    st.success("Knowledge base built successfully.")

                except Exception as e:
                    st.error(f"Error building knowledge base: {e}")

        if st.session_state["vectordb"] is not None:
            st.markdown("---")
            st.subheader("Chat with Document")
            display_conversation()

            if st.session_state["conversation_history"]:
                if st.button("Clear Conversation", key="clear_conversation"):
                    st.session_state["conversation_history"] = []
                    st.rerun()
        else:
            st.info("Upload a PDF and click 'Build Knowledge Base' to start chatting.")

    # -------------------------
    # TAB 2: BUSINESS MODEL
    # -------------------------
    with tab2:
        st.subheader("Generate Business Model from PDF")

        uploaded_bm = st.file_uploader(
            "Upload a PDF file for business model generation",
            type=["pdf"],
            key="bm_uploader"
        )

        if uploaded_bm is not None:
            st.info(f"Uploaded: {uploaded_bm.name}")

            if st.session_state["bm_pdf_name"] != uploaded_bm.name:
                st.session_state["bm_pdf_name"] = uploaded_bm.name
                st.session_state["business_model"] = ""

            if st.button("Generate Business Model", key="generate_bm"):
                try:
                    pdf_path_bm = save_uploaded_file(uploaded_bm)

                    with st.spinner("Extracting text and generating business model..."):
                        document_content = extract_text_from_pdf(pdf_path_bm)

                        if not document_content.strip():
                            st.warning("No text could be extracted from this PDF.")
                        else:
                            # trim to avoid huge prompt size
                            document_content = document_content[:10000]
                            business_model = generate_business_model(document_content)
                            st.session_state["business_model"] = business_model

                    if st.session_state["business_model"]:
                        st.success("Business model generated successfully.")

                except Exception as e:
                    st.error(f"Error generating business model: {e}")

        if st.session_state["business_model"]:
            st.markdown("### Generated Business Model")
            st.text_area(
                "Business Model Output",
                value=st.session_state["business_model"],
                height=400,
                key="bm_output"
            )

    # -------------------------
    # GLOBAL CHAT INPUT
    # Must be outside tabs
    # -------------------------
    question = st.chat_input("Ask a question about the uploaded document")

    if question:
        if st.session_state["vectordb"] is None:
            st.warning("Please upload a PDF and build the knowledge base first.")
        else:
            st.session_state["conversation_history"].append(
                {"role": "user", "content": question}
            )

            try:
                with st.spinner("Thinking..."):
                    answer = answer_question(
                        st.session_state["vectordb"],
                        question,
                        conversation_history=st.session_state["conversation_history"][:-1]
                    )

                st.session_state["conversation_history"].append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"Error: {e}")

                # remove last user message if processing failed
                if st.session_state["conversation_history"]:
                    st.session_state["conversation_history"].pop()

            st.rerun()


if __name__ == "__main__":
    main()