import streamlit as st
from api_utils import get_api_response


def display_chat_interface():
    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Query:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Generating response..."):
            response = get_api_response(
                prompt, st.session_state.session_id, st.session_state.model
            )

            if response:
                st.session_state.session_id = response.get("session_id")

                formatted_output = ""
                for key, val in response["answer"].items():
                    formatted_output += key + ": \n" + val + "\n\n"

                st.session_state.messages.append(
                    {"role": "assistant", "content": formatted_output}
                )

                result_dict = response["answer"]
                with st.chat_message("assistant"):
                    for key, val in result_dict.items():
                        with st.container():     
                            # Display upvote and downvote buttons
                            col1, col2 = st.columns([4, 1])
                            with col1:
                            #    st.markdown(f"### {key}")
                            #    st.markdown(val)
                               st.write(f"<h3 style='font-family:Calibri; font-size:20px;'>{key}</h3>", unsafe_allow_html=True)
                               st.write(f"<p style='font-family:Calibri; font-size:15px;'>{val}</p>", unsafe_allow_html=True)
                            with col2:
                                st.write("###")  # Ensure proper formatting
                                col3, col4 = st.columns([1, 1])
                                with col3:
                                    if st.button('👍', key=f"upvote_{key}"):
                                        st.session_state.votes[key] += 1
                                with col4:
                                    if st.button('👎', key=f"downvote_{key}"):
                                        st.session_state.votes[key] -= 1

                    # st.markdown(response["answer"])

                    with st.expander("Details"):
                        st.subheader("Generated Answer")
                        st.code(response["answer"])
                        st.subheader("Model Used")
                        st.code(response["model"])
                        st.subheader("Session ID")
                        st.code(response["session_id"])
            else:
                st.error("Failed to get a response from the API. Please try again.")
