from langchain_core.prompts import PromptTemplate
cancellation_prompt = PromptTemplate( 
    input_variables=["query"], 
    template=""" 
    You are a cancellation support specialist. 
    Customer query: {query} 
    Write a helpful response that: 
    - acknowledges the cancellation request, 
    - asks for the order ID if missing, 
    - explains that cancellation depends on order status, 
    - avoids promising successful cancellation. 
Response:
 """ 
)