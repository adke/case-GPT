import requests
from taipy.gui import Gui, State
import json
from clarifying_questions_database import clarifying_questions
from framework_database import framework_list

context = "Welcome to our case interview practice session. Today's case involves a retail company experiencing declining sales in its flagship store. The company suspects changing consumer preferences and increased competition from online retailers may be contributing factors."
conversation = {
    "Conversation": [context]
}
current_user_message = ""

API_URL = 'https://api.together.xyz/v1/chat/completions'
headers={
    "Authorization": "Bearer f0f8fe90841d6b1e22ee9f9649962f2ebf402a89bd037483c8a2e4a5e6732256",
}

def get_response(prompt: str) -> str:
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
    return output

def send_message(state: State) -> None:
    """
    Send the user's message to the API and update the conversation.

    Args:
        - state: The current state of the app.
    """
    global current_step
    
    # Add the user's message to the context
    state.context += f"Human: \n {state.current_user_message}\n\n AI:"
    
    # Check the current step in the conversation
    if current_step == 0:
        # Welcome message and ask for user input
        case_prompt = "Welcome to our case interview practice session. Today's case involves a retail company experiencing declining sales in its flagship store. The company suspects changing consumer preferences and increased competition from online retailers may be contributing factors."
        state.context += case_prompt
        state.context += "\nPlease provide your input:"
        current_step += 1
    elif current_step == 1:
        # Get user input and classify the case
        question = "Now, can you please restate your understanding of the case and classify it into one of the following casing categories: Market Entry, Product Launch, Operational Efficiency, Financial Analysis, or Other?"
        state.context += question
        current_step += 1
    elif current_step == 2:
        # Check if user input is in the correct category
        if "Operational Efficiency" not in state.current_user_message:
            state.context += "This is not the correct category, please try again"
        else:
            state.context += "That's the correct approach, go ahead and explain your framework"
            current_step += 1
    elif current_step == 3:
        # Check if framework is valid
        if not any(framework in state.current_user_message for framework in framework_list):
            state.context += f"The following framework {state.current_user_message} is not valid, please try again"
        else:
            state.context += "Your framework aligns with the operational efficiency focus. Please proceed with your analysis, making sure you provide the drivers for your framework."
            current_step += 1
    elif current_step == 4:
        # Provide a concise follow-up response to the analysis
        prompt_3 = f"Provide a concise follow-up response to {state.current_user_message} and ensure that the same information as {state.current_user_message} is not mentioned in the follow-up response"
        framework_response = get_response(prompt_3)
        state.context += framework_response
        state.context += "------------------------------------------------------------------------\n"
        state.context += "Awesome, now to finish off let's summarize the entire case"
        current_step += 1
    elif current_step == 5:
        # Rate the submitted summary
        gold_summary = "The company's declining sales are attributed to changing consumer preferences and increased competition from online retailers. To address this, we will implement targeted marketing campaigns, enhance the customer loyalty program, and optimize inventory levels to meet demand fluctuations"
        res_prompt = f"Now rate the submitted summary: {state.current_user_message} vs our gold standard summary: {gold_summary}"
        rating = get_response(res_prompt)
        state.context += rating
    
    # Update the conversation
    conv = state.conversation._dict.copy()
    conv["Conversation"] += [state.current_user_message, state.context]
    state.conversation = conv
    
    # Clear the input field
    state.current_user_message = ""

# Initialize the current step variable
current_step = 0

# Run the Taipy GUI
page = f"""
<|{conversation}|table|show_all|width=100%|>
<|{current_user_message}|input|label=Write your message here...|on_action=send_message|class_name=fullwidth|>
"""

if __name__ == "__main__":
    Gui(page).run(dark_mode=True, title="Taipy Chat")

