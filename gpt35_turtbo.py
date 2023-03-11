

api_key = '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'
import openai
import os
openai.api_key = api_key
# openai.organization = "MEIKO"

conversation=[{"role": "system", "content": "You are a helpful assistant."}]

while(True):
    user_input = input("You: ")
    if user_input == "bye":
        break
    conversation.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = conversation,
        temperature=2,
        max_tokens=1024,
        top_p=0.9
    )
    for choice in response['choices']:
        print("\n" + choice['message']['content'] + "\n")

    conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    print("\n" + response['choices'][0]['message']['content'] + "\n")