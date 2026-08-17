from langchain_core.prompts import PromptTemplate

refund_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
You are a refund support specialist.

Customer query:
{query}

Write a helpful response that:
- acknowledges the refund request,
- asks for the order ID if missing,
- does not promise approval,
- explains that eligibility will be checked.

Response:
"""
)

# testing the context propagation
# refund_prompt = PromptTemplate( 
#     input_variables=["query", "confidence"], 
#     template=""" 
#     You are a refund support specialist. 
#     Classification confidence: 
#     {confidence} 
#     Customer query: 
#     {query} 
#     If confidence is below 0.8, 
#     ask one clarifying question first.
#       Otherwise, proceed with refund assistance. 
#       Response: """
#      )