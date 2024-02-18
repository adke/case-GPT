import json
import requests
from clarifying_questions_database import clarifying_questions
from framework_database import framework_list

def get_response(prompt):
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
      "Authorization": "Bearer API Key",
  })
  output = res.json()['choices'][0]['message']['content']
  print(output)

def retailDeclineCase():

  case_prompt = "Welcome to our case interview practice session. Today's case involves a retail company experiencing declining sales in its flagship store. The company suspects changing consumer preferences and increased competition from online retailers may be contributing factors."
  print(case_prompt)
  human_input = input()

  question = "Now, can you please restate your understanding of the case and classify it into one of the following casing categories: Market Entry, Product Launch, Operational Efficiency, Financial Analysis, or Other?"
  prompt_2 = f"If {human_input} is a question in {clarifying_questions}, answer it without answering other questions in {clarifying_questions}, be as concise as possible"
  response_api = get_response(prompt_2)
  print(response_api)
  print(question)

  human_input = input()

  while "Operational Efficiency" not in human_input:
    print("This is not the correct category, please try again")
    human_input = input()

  print("That's the correct approach, go ahead and explain your framework")
  framework = input()


  while (framework_list[0] or framework_list[1] or framework_list[2]) not in framework:
    print(f"The following framework {framework} is not valid, please try again")
    framework = input()

  print("Your framework aligns with the operational efficiency focus. Please proceed with your analysis, making sure you provide the drivers for your framework.")

  analysis = input()

  prompt_3 = f"Provide a concise follow-up response to {analysis} and ensure that the same information as {analysis} is not mentioned in the follow-up response"

  framework_response = get_response(prompt_3)
  print(framework_response)
  print("------------------------------------------------------------------------")
  print("Awesome, now to finish off let's summarize the entire case")
  summarized = input()
  gold_summary = "The company's declining sales are attributed to changing consumer preferences and increased competition from online retailers. To address this, we will implement targeted marketing campaigns, enhance the customer loyalty program, and optimize inventory levels to meet demand fluctuations"
  res_prompt = f"Now rate the submitted summary: {summarized} vs our gold standard summary: {gold_summary}"
  rating = get_response(res_prompt)
  print(rating)


def main():
    retailDeclineCase()

if __name__=="__main__":
    main()

