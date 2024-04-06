from utils import *
from encode_document import *
from init_llm_model import *
def init():
  my_vectordb, SENTEMB = encode_document()
  GEMINI = load_model()

  return my_vectordb, SENTEMB, GEMINI

def chat(my_vectordb, SENTEMB,GEMINI):
  """Simulates a simple chat interface with conversation history in Google Colab."""
  conversation_history = ""
  while True:
    user_input = input("User: ")
    conversation_history += f"User: {user_input}\n"

    if user_input.lower() == "quit":
      print("Assistant: Goodbye!")
      break


    response_conv_turn = handle_conversation_turn(conversation_history, my_vectordb, SENTEMB, GEMINI)
    response = response_conv_turn.text
    conversation_history += f"Assistant: {response}\n"
    print(f"Assistant: {response}\n")

  return conversation_history

if __name__ == "__main__":
  my_vectordb, SENTEMB, GEMINI = init()
  chat(my_vectordb,SENTEMB,GEMINI)