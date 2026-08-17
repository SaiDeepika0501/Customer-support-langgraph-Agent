from langchain_core.prompts import PromptTemplate 
intent_prompt = PromptTemplate( input_variables=["query"], template=""" 
    Classify the customer query into exactly one of these intents: - refund - shipping - cancellation - policy - order_status - other 
    Customer query: {query} """ )