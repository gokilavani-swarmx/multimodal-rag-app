import streamlit as st
import subprocess
import pandas as pd, re
from api_utils import upload_document, list_documents, delete_document


def local_model_list():
    # Command to run in the command prompt
    command = "Ollama list"  # Replace with your command

    # Run the command
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    # Print the output and errors
    # print("Output:\n", stdout.decode())
    if stderr:
        print("Errors:\n", stderr.decode())

    ollama_mdl_df = pd.DataFrame(
        [
            re.sub(r"\s{2,}", ",", vl.strip()).split(",")
            for vl in stdout.decode().splitlines()
        ]
    )

    # Make the first row the header
    ollama_mdl_df.columns = ollama_mdl_df.iloc[0]
    ollama_mdl_df = ollama_mdl_df[1:]

    # Reset the index
    ollama_mdl_df.reset_index(drop=True, inplace=True)

    # print("completed without error")

    # Display the DataFrame
    return ollama_mdl_df["NAME"].values.tolist()


def display_sidebar():
    # Sidebar: Model Selection
    # model_options = ["gpt-4o", "gpt-4o-mini"]
    model_options = local_model_list()
    st.sidebar.selectbox("Select Model", options=model_options, key="model")

    # Sidebar: Upload Document
    st.sidebar.header("Upload Document")
    uploaded_files = st.sidebar.file_uploader(
        "Choose a file", type=["pdf", "docx", "html"], accept_multiple_files=True
    )
    if uploaded_files is not None:
        if st.sidebar.button("Upload"):
            with st.spinner("Uploading..."):
                for uploaded_file in uploaded_files:
                    upload_response = upload_document(uploaded_file)
                    if upload_response:
                        # st.sidebar.success(
                        #     f"File '{uploaded_file.name}' uploaded successfully with ID {upload_response['file_id']}."
                        # )
                        st.sidebar.success(
                            upload_response['message']
                        )
                        st.session_state.documents = (
                            list_documents()
                        )  # Refresh the list after upload

    # Sidebar: List Documents
    st.sidebar.header("Uploaded Documents")
    if st.sidebar.button("Refresh Document List"):
        with st.spinner("Refreshing..."):
            st.session_state.documents = list_documents()

    # Initialize document list if not present
    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()

    documents = st.session_state.documents
    if documents:
        for doc in documents:
            st.sidebar.text(
                f"{doc['filename']} (ID: {doc['id']}, Uploaded: {doc['upload_timestamp']})"
            )

        # Delete Document
        selected_file_id = st.sidebar.selectbox(
            "Select a document to delete",
            options=[doc["id"] for doc in documents],
            format_func=lambda x: next(
                doc["filename"] for doc in documents if doc["id"] == x
            ),
        )
        if st.sidebar.button("Delete Selected Document"):
            with st.spinner("Deleting..."):
                delete_response = delete_document(selected_file_id)
                if delete_response:
                    st.sidebar.success(
                        f"Document with ID {selected_file_id} deleted successfully."
                    )
                    st.session_state.documents = (
                        list_documents()
                    )  # Refresh the list after deletion
                else:
                    st.sidebar.error(
                        f"Failed to delete document with ID {selected_file_id}."
                    )
