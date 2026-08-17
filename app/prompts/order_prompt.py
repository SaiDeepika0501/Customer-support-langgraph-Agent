from langchain_core.prompts import PromptTemplate 
order_prompt = PromptTemplate( 
    input_variables=["query"], 
    template=""" 
You are an order status support specialist.
Customer query: {query} 
Write a helpful response that: 
- acknowledges the order status request, 
- asks for the order or tracking ID if missing, 
- avoids inventing shipment details.
 Response: 
 """ 
)