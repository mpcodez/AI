import openai

# Set your OpenAI API key
openai.api_key = 'YOUR_API_KEY'

def chat_with_bot(message):
    # Define the conversation history (prepend the user's message)
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message}
    ]

    # Generate a response from the chatbot
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    # Extract the chatbot's reply
    bot_reply = response['choices'][0]['message']['content']

    return bot_reply

print("Hello! I'm here to chat with you. You can talk to me about your concerns.")
print("Type 'exit' to end the conversation.")

while True:
    user_message = input("You: ")
    
    if user_message.lower() == 'exit':
        print("Chatbot: Goodbye! Take care.")
        break
    
    bot_response = chat_with_bot(user_message)
    print("Chatbot:", bot_response)
