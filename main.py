from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI(api_key="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")

def chat_with_chad(prompt):
    response = client.chat.completions.create(
        model = "gpt-4o", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
    
def main():
    while True:
        user_input = input("You: ")
        if user_input.lower in ["quit", "exit", "bye"]:
            break
        response = chat_with_chad(user_input)
        print("Chatbot: ", response)
        
if __name__ == "__main__":
    main()