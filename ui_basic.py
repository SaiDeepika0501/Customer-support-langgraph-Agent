# import streamlit as st 
# st.title("AI Customer Support") 
# with st.chat_message("assistant"): 
#     st.write("Hello! How can I help you today?") 
# user_input = st.chat_input("Type your message...") 
# if user_input: 
#     with st.chat_message("user"): 
#         st.write(user_input) 
#     with st.chat_message("assistant"): 
#         st.write(f"I received: {user_input}")

import streamlit as st

st.title("AI Customer Support")

# Initialize history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# New input
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # Fake assistant reply
    reply = f"I received: {user_input}"

    # Save assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    st.rerun()

