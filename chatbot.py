from langchain_google_genai import ChatGoogleGenerativeAI
import os 
import dotenv
dotenv.load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

print("Chat Model: ", llm.model)
input_prompt = input ("Type your prompt [Press q to quit]: \n")

while input_prompt.lower() != 'q':
    response = llm.invoke(input_prompt)
    print("Response: ", response.content)
    input_prompt = input ("Type your prompt [Press q to quit]: \n")
