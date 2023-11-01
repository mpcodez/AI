import nltk
import random
from nltk.chat.util import Chat, reflections

nltk.download('punkt')

# Define patterns and responses for the chatbot
psychobabble = [
    ["(.*) my therapist is offline (.*)",
     ["I'm here to listen. You can tell me about what's on your mind.", "I'm here to help. What's bothering you?"]],
    
    ["(.*) (sad|depressed|anxious|lonely) (.*)",
     ["I'm sorry to hear that you're feeling this way. Can you tell me more about it?", "It's okay to feel this way sometimes. What's been on your mind?"]],
    
    ["(.*) (family|relationship|work|friend) (.*)(trouble|problem)(.*)",
     ["Relationships can be challenging. Tell me more about what's going on.", "I'm here to listen. What's been bothering you about your (family/relationship/work/friend)?"]],
    
    ["(.*) (I feel|I'm feeling) (.*)",
     ["I hear you. Can you tell me more about why you're feeling this way?", "Feelings are important. What's been going on that's making you feel like this?"]],
    
    ["(.*) (therapy|therapist) (.*)(help|benefit|good)(.*)",
     ["Therapy can be very beneficial. It's great that you're seeking help. How has your therapy been going so far?", "Therapy is a positive step towards improving your mental health. What do you think about your therapy sessions?"]],
    
    ["(.*) (suggestion|advice) (.*)(feel better|improve|cope)(.*)",
     ["I'm not a therapist, but I can suggest trying activities like exercise, meditation, or talking to friends and family. These can sometimes help improve your mood."]],
    
    ["(.*) (thank you|thanks)(.*)",
     ["You're welcome! I'm here to support you. Is there anything else you'd like to talk about?"]],
    
    ["(.*)",
     ["I'm here to listen and chat, but please remember that I'm not a substitute for professional help. If you're in crisis or need urgent support, please reach out to a mental health professional or a crisis helpline."]]
]

# Create a Chat instance and set a name for the chatbot
chatbot = Chat(psychobabble, reflections)

print("Hello, I'm here to chat with you. Feel free to talk about anything on your mind.")

# Start the chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Goodbye. Take care!")
        break
    response = chatbot.respond(user_input)
    print("Bot: " + response)
