from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_chad(prompt):
    response = client.chat.completions.create(
        model = "gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
    
def main():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
        response = chat_with_chad(user_input)
        print("Chatbot: ", response)
        
if __name__ == "__main__":
    main()