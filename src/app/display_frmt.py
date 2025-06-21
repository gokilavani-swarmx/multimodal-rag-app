import streamlit as st
# from streamlit.elements import icon

# Given string
jsn = "{'chain_baseline': 'The accuracy range for the CI1A model with J thermocouple output is larger of -2% or -3ß C (-6ß F).', 'chain_mv_text': 'The accuracy range for the CI1A model with J thermocouple output is not explicitly stated in the provided context. However, it is mentioned that the CI1B model has an accuracy range of 30-500°C (86-932°F) for its J thermocouple output.', 'chain_multimodal_mv_img': ' The accuracy range for the CI1A model with J thermocouple output is 0-115°C (32-240°F). This information is provided in a table that summarizes different thermocouple models and their temperature ranges, along with their accuracy ranges. ', 'chain_multimodal_embd': ' Based on the provided context, the accuracy range for the CI1A model with J thermocouple output is 0 to 115°C (32 to 240°F) with a larger of -2% or -3°C (-6°F). This means that the measurement results may be within this temperature range, but there might be an error of up to -2% or -3°C. It is important to note that this accuracy range applies only to the CI1A model with J thermocouple output. The accuracy ranges for other models in the Thermalert® CI™ Compact Infrared Sensor series may be different. '}"

# Convert string to dictionary
result_dict = eval(jsn)

# Initialize session state to keep track of votes
if 'votes' not in st.session_state:
    st.session_state.votes = {key: 0 for key in result_dict.keys()}

formatted_output = ""

# Display and format the outputs
for key, val in result_dict.items():
    with st.container():     
        # Display upvote and downvote buttons
        col1, col2 = st.columns([4, 1])
        with col1:
            # st.write(f"### {key}")
            st.write(f"<h3 style='font-family:Calibri; font-size:20px;'>{key}</h3>", unsafe_allow_html=True)
            st.write(f"<p style='font-family:Calibri; font-size:15px;'>{val}</p>", unsafe_allow_html=True)
            # st.write(val)
        with col2:
            st.write(f"###")
            col3, col4 = st.columns([1, 1])
            # with col3:
            #     if st.button('👍', key=f"upvote_{key}"):
            #         st.session_state.votes[key] += 1    
            # with col4:
            #     if st.button('👎', key=f"downvote_{key}"):
            #         st.session_state.votes[key] -= 1
            with col3:
                # Adding style to center the buttons
                st.write(
                    f"<div style='display: flex; justify-content: center;'>"
                    f"<button style='font-size:20px;'>{'👍'}</button>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                if st.button('👍', key=f"upvote_{key}"):
                    st.session_state.votes[key] += 1
            with col4:
                st.write(
                    f"<div style='display: flex; justify-content: center;'>"
                    f"<button style='font-size:20px;'>{'👎'}</button>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                if st.button('👎', key=f"downvote_{key}"):
                    st.session_state.votes[key] -= 1
            
        # Display current votes
        # st.write(f"Votes: {st.session_state.votes[key]}")
    
    formatted_output += f"{key}: \n{val}\n\n"

# Print the formatted output
st.write(formatted_output)
