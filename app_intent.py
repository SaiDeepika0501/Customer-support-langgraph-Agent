
# from langchain_google_genai import ChatGoogleGenerativeAI 
# from utils.config import GOOGLE_API_KEY 
# from prompts.intent_prompt import intent_prompt 
# from models.intent import IntentOutput 
# # Initialize model 
# model = ChatGoogleGenerativeAI( model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY, temperature=0.0, ) 
# # Structured output wrapper 
# structured_model = model.with_structured_output(IntentOutput) 
# # Build chain 
# chain = intent_prompt | structured_model 
# # Test query 
# query = "I want my money back" 
# result = chain.invoke({"query": query}) 
# print(result)
# print(type(result)) 
# print("Intent:", result.intent) 
# print("Confidence:", result.confidence)

from langchain_google_genai import ChatGoogleGenerativeAI 
from pydantic import ValidationError 
from utils.config import GOOGLE_API_KEY 
from prompts.intent_prompt import intent_prompt 
from models.intent import IntentOutput
from router import route_intent 
 # Initialize model 
model = ChatGoogleGenerativeAI( model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY, temperature=0.0, ) 
structured_model = model.with_structured_output(IntentOutput)
chain = intent_prompt | structured_model 
query = "I paid twice for my order and I’m not sure if I should request a refund or contact support." 
try:
     result = chain.invoke({"query": query}) 
     print("Intent:", result.intent) 
     print("Confidence:", result.confidence) 
except ValidationError as e: 
    print("Validation failed!") 
    print(e) 
except Exception as e: 
    print("Unexpected error!") 
    print(e)
next_step = route_intent(result.intent, result.confidence) 
print("Next step:", next_step)
