from langchain_core.prompts import PromptTemplate 
shipping_prompt = PromptTemplate( input_variables=["query"], 
    template=""" You are a shipping support specialist. 
    Customer query: {query} 
    Write a helpful response that: 
    - acknowledges the shipping issue,
      - asks for the tracking or order ID if missing, 
      - avoids inventing delivery dates. Response: """ )