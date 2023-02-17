#!/usr/bin/env python3
# -*-coding:utf-8-*-

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer, UbuntuCorpusTrainer
import json
import yaml
from text_to_speech import text_to_speech
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

'''
This is an example showing how to create an export file from
an existing chat bot that can then be used to train other bots.
'''

# chatbot = ChatBot('Export Example Bot')

chatbot = ChatBot(
    "My ChatterBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    # database_uri="sqlite:///db.sqlite3",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.95
        }
    ]
)

with open('train/train_dict.json') as json_file:
    data_dict = json.load(json_file)

with open('train/train_data.yaml') as yaml_file:
    yaml_dict = yaml.load(yaml_file, Loader=yaml.Loader)
    # with open('train/train_data.json', 'w',encoding ='utf8') as f:
    #     json.dump(yaml_dict, f,indent= 2, ensure_ascii = False)

# print(data_dict)
for label in data_dict:
    print(label)
    # print(data_dict[label])

######## Select training method ##########

## $1 Use corpus trainer
# First, lets train our bot with some data
trainer = ChatterBotCorpusTrainer(chatbot)

# trainer.train('chatterbot.corpus.english.greetings')
trainer.train('train/train_data.json')

# ### $2 Use List traniner
# trainer = ListTrainer(chatbot)

# # Train the chat bot with a few responses
# trainer.train([
#     'How can I help you?',
#     'I want to create a chat bot',
#     'password wifi',
#     'password is 12345',
#     'cong ty meiko automation',
#     'cong ty cong nghe',
#     'Have you read the documentation?',
#     'No, I have not',
#     'This should help get you started: http://chatterbot.rtfd.org/en/latest/quickstart.html'
# ])

# # Now we can export the data to a file
# trainer.export_for_training('./my_export.json')

while True:
    try:
        request = input("Bạn: ")
        if ("bye" in request):
            break
        response = str(chatbot.get_response(request))
        print("ChatBot:$", response)
        # print("type: ", type(response))
        if str(response) in data_dict:
            print("co trong tu dien")
            response = data_dict[str(response)]
        text_to_speech(response)
        # print("type of text:", type(response))

    except:
        print("not found in library")
