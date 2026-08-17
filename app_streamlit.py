####        support-engine response

#  import streamlit as st 
# from support_engine import generate_support_response 
# st.set_page_config( 
#     page_title="AI Customer Support", 
#     page_icon="🤖", layout="centered" ) 
# st.title("🤖 AI Customer Support") 
# st.caption("LangChain + Gemini + Structured Routing")

# # Initialize session history 
# if "messages" not in st.session_state: 
#     st.session_state.messages = [ 
#         { "role": "assistant", 
#          "content": "Hello! How can I help you today?" 
#          } ]
    
# # Display chat history 
# for msg in st.session_state.messages: 
#     with st.chat_message(msg["role"]): 
#         st.write(msg["content"]) 

# # User input 
# user_input = st.chat_input("Type your message...") 
# if user_input: 
# # Save user message 
#    st.session_state.messages.append({ "role": "user", "content": user_input }) 
# # Display user message immediately 
#    with st.chat_message("user"): 
#       st.write(user_input)
#  # Generate assistant response 
#    with st.chat_message("assistant"): 
#     with st.spinner("Thinking..."): 
#         result = generate_support_response(user_input) 
#         st.write(result["response"]) 
        
#         # Optional debug info 
#         with st.expander("Debug Info"): 
#             st.write(f"Intent: {result['intent']}") 
#             st.write(f"Confidence: {result['confidence']:.2f}")
#  # Save assistant message 
#    st.session_state.messages.append({ 
#       "role": "assistant", 
#       "content": result["response"] 
#       })
# if st.button("🗑️ Clear Chat"): 
#     st.session_state.messages = [ 
#        { "role": "assistant", 
#         "content": "Hello! How can I help you today?" } ] 
#     st.rerun()

###            RAG RESPONSE
import streamlit as st
from rag_engine import generate_rag_response

st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Customer Support")
st.caption("RAG + FAISS + Gemini")

# Initialize session history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! Ask me about company policies, refunds, shipping, cancellations, or payments."
        }
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Single chat input
user_input = st.chat_input("Ask about company policies...")

if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Generate RAG response
    with st.chat_message("assistant"):
        with st.spinner("Searching policies..."):

            answer, sources = generate_rag_response(user_input)

            st.write(answer)

            with st.expander("Sources"):
                for s in sources:
                    st.write("- " + s)

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

# Clear chat
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! Ask me about company policies, refunds, shipping, cancellations, or payments."
        }
    ]
    st.rerun()