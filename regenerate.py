import openai
from decouple import config

openai.api_key = config('OPENAI_KEY_1')

messages = []
system_msg = "Ielts writing editor"
messages.append({"role": "system", "content": system_msg})



index = 39


directory = 'processed_essay'
file = f'{directory}\essay_{index}.txt' 

with open(file, 'r', encoding="utf-8") as f:
    lines = f.readlines()
    # print(''.join(f.readlines()))

    sep_indexes = [
        lines.index('Essay:\n', 2, 10),
        lines.index('Revised:\n', 7, 20),
        lines.index('Task Response:\n', 20),
        lines.index('Coherence and Cohesion:\n', 20),
        lines.index('Lexical Resource:\n', 20),
        lines.index('Grammatical Range and Accuracy:\n', 20),
        lines.index('Score:\n', 40),
    ]

    topic = lines[1:sep_indexes[0]]
    essay = lines[sep_indexes[0] + 1: sep_indexes[1]]
    revised = lines[sep_indexes[1] + 1: sep_indexes[2]]
    tr = lines[sep_indexes[2] + 1: sep_indexes[3]]
    cc = lines[sep_indexes[3] + 1: sep_indexes[4]]
    lr = lines[sep_indexes[4] + 1: sep_indexes[5]]
    ga = lines[sep_indexes[5] + 1: sep_indexes[6]]
    score = lines[sep_indexes[6] + 1:]

    print(topic)
    print(essay)

    syntax = []
    syntax 

    # i = 0
    # while i <= 7:
    #     message