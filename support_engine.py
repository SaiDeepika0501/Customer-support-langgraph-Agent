from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.output_parsers import StrOutputParser 
from utils.config import GOOGLE_API_KEY 
from prompts.intent_prompt import intent_prompt 
from prompts.refund_prompt import refund_prompt 
from prompts.shipping_prompt import shipping_prompt 
from prompts.policy_prompt import policy_prompt 
from prompts.cancellation_prompt import cancellation_prompt 
from prompts.order_prompt import order_prompt 
from prompts.payment_prompt import payment_prompt
from models.intent import IntentOutput 

# Shared model 
model = ChatGoogleGenerativeAI( 
    model="gemini-2.5-flash", 
    google_api_key=GOOGLE_API_KEY, 
    temperature=0.2, )

# Intent chain 
intent_chain = intent_prompt | model.with_structured_output(IntentOutput) 

# Response chains 
ROUTES = { 
    "refund": refund_prompt | model | StrOutputParser(), 
    "shipping": shipping_prompt | model | StrOutputParser(), 
    "cancellation": cancellation_prompt | model | StrOutputParser(), 
    "policy": policy_prompt | model | StrOutputParser(), 
    "order_status": order_prompt | model | StrOutputParser(),
    "payment": payment_prompt | model | StrOutputParser(), } 
def generate_support_response(query: str): 
    """Classify, route, and generate a response.""" 
    # Step 1: classify 
    intent_result = intent_chain.invoke({"query": query}) 
    # Step 2: route 
    selected_chain = ROUTES.get(intent_result.intent) 
    if selected_chain: 
        response = selected_chain.invoke({"query": query}) 
    else: response = "I need a little more information to help you correctly." 
    return { 
        "intent": intent_result.intent, 
        "confidence": intent_result.confidence, 
        "response": response, }