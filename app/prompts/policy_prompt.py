from langchain_core.prompts import PromptTemplate 
policy_prompt = PromptTemplate( 
    input_variables=["query"], 
    template=""" 
    You are a policy support specialist. 
    Customer query: {query} 
    Write a helpful response that: 
    - explains that policies may vary, 
    - gives a concise overview of return/refund policies, 
    - avoids inventing company-specific details, 
    - offers to provide exact policy details if the customer shares the product or order information. 
Response: 
""" 
)