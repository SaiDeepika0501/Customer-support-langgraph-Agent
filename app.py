from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.output_parsers import StrOutputParser 
from utils.config import GOOGLE_API_KEY 
from prompts.customer_support import customer_support_prompt 
# Initialize Gemini 2.5 Flash
model = ChatGoogleGenerativeAI( 
  model="gemini-2.5-flash", 
  google_api_key=GOOGLE_API_KEY, 
  temperature=0.2, 
) 
# Output parser 
parser = StrOutputParser() 
# Build the LCEL chain 
chain = customer_support_prompt | model | parser 
# Test question 
question = "Can i cancel my order?" 
response = chain.invoke({"question": question}) 
print("Customer:", question) 
print() 
print("Assistant:") 
print(response)