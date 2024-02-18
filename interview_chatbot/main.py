import requests
from taipy.gui import Gui, State, notify

context = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by Google. How can I help you today? "
conversation = {
    "Conversation": ["Who are you?", "Hi! I am LLama-70B. How can I help you today?"]
}
current_user_message = ""

API_URL = 'https://api.together.xyz/v1/chat/completions'
headers={
      "Authorization": "Bearer f0f8fe90841d6b1e22ee9f9649962f2ebf402a89bd037483c8a2e4a5e6732256",
  }

def get_response(state: State, prompt:str) -> str:
  endpoint = 'https://api.together.xyz/v1/chat/completions'
  res = requests.post(endpoint, json={
      "model": "meta-llama/Llama-2-70b-chat-hf",
      "max_tokens": 512,
      "prompt": f"[INST] {prompt} [/INST]",
      "temperature": 0.0,
      "top_p": 0.7,
      "top_k": 50,
      "repetition_penalty": 1,
      "stop": [
          "[/INST]",
          "</s>"
      ],
      "repetitive_penalty": 1,
      "update_at": "2024-02-17T19:01:39.423Z"
  }, headers={
      "Authorization": "Bearer f0f8fe90841d6b1e22ee9f9649962f2ebf402a89bd037483c8a2e4a5e6732256",
  })
  output = res.json()['choices'][0]['message']['content']
  print(output)
  return output

def send_message(state: State) -> None:
    """
    Send the user's message to the API and update the conversation.

    Args:
        - state: The current state of the app.
    """
    # Add the user's message to the context
    state.context += f"Human: \n {state.current_user_message}\n\n AI:"
    # Send the user's message to the API and get the response
    answer = get_response(state, state.context).replace("\n", "")
    # Add the response to the context for future messages
    state.context += answer
    # Update the conversation
    conv = state.conversation._dict.copy()
    conv["Conversation"] += [state.current_user_message, answer]
    state.conversation = conv
    # Clear the input field
    state.current_user_message = ""

page = """
<|{conversation}|table|show_all|width=100%|>
<|{current_user_message}|input|label=Write your message here...|on_action=send_message|class_name=fullwidth|>
"""

if __name__ == "__main__":
    Gui(page).run(dark_mode=True, title="Taipy Chat")

