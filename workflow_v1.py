from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.output_parsers import StrOutputParser 
from utils.config import GOOGLE_API_KEY 
from prompts.intent_prompt import intent_prompt 
from prompts.refund_prompt import refund_prompt 
from prompts.shipping_prompt import shipping_prompt 
from prompts.policy_prompt import policy_prompt
from prompts.cancellation_prompt import cancellation_prompt
from prompts.order_prompt import order_prompt
from models.intent import IntentOutput 
# Shared model 
model = ChatGoogleGenerativeAI( model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY, temperature=0.2, ) 

# Intent chain 
intent_chain = intent_prompt | model.with_structured_output(IntentOutput) 

# Response chains 
# refund_chain = refund_prompt | model | StrOutputParser() 
# shipping_chain = shipping_prompt | model | StrOutputParser()
# policy_chain = policy_prompt | model | StrOutputParser()
# cancellation_chain = cancellation_prompt | model | StrOutputParser()
# order_chain = order_prompt | model | StrOutputParser()

ROUTES = { 
    "refund": refund_prompt | model | StrOutputParser(), 
    "shipping": shipping_prompt | model | StrOutputParser(), 
    "cancellation": cancellation_prompt | model | StrOutputParser(), 
    "policy": policy_prompt | model | StrOutputParser(), 
    "order_status": order_prompt | model | StrOutputParser(), 
}

# Test query 
query = "when will i get my refund?" 


# Step 1: classify 
intent_result = intent_chain.invoke({"query": query}) 
print("Intent:", intent_result.intent) 
print("Confidence:", intent_result.confidence)


 # Step 2: route 
# if intent_result.intent == "refund":
#     response = refund_chain.invoke({"query": query})

# elif intent_result.intent == "shipping":
#     response = shipping_chain.invoke({"query": query})

# elif intent_result.intent == "cancellation":
#     response = cancellation_chain.invoke({"query": query})

# elif intent_result.intent == "policy":
#     response = policy_chain.invoke({"query": query})

# elif intent_result.intent == "order_status":
#     response = order_chain.invoke({"query": query})

# else:
#     response = "I need a little more information to help you correctly."

# Dictionary routing table->
selected_chain = ROUTES.get(intent_result.intent) 
if selected_chain: 
    response = selected_chain.invoke({"query": query}) 
    # for testing context propagation->> response = selected_chain.invoke({ "query": query, "confidence": intent_result.confidence })
else: response = "I need a little more information to help you correctly."


 # Step 3: final output 
print(" Final Response: ")
print(response)

