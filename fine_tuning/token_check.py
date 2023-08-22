import json
import os
from finetune_tools import token_to_call

main_directory = 'assets/unassessed_essays'
data = []

n_tok_exceed = 0

# with open('fine_tuning\cc/train_cc_sample.jsonl', 'r', encoding= "utf-8") as file:
#     row = 1
#     for line in file:
#         data = json.loads(line)

#         prompt = data['prompt']
#         completion = data['completion']
        
#         token = token_to_call("r50k_base", prompt, completion)
#         if token > 2048:
#             n_tok_exceed += 1
#             print(row)
        
#         row += 1
        

for itemname in os.listdir(main_directory):
    folder = os.path.join(main_directory, itemname)
    # checking if it is a folder
    if not os.path.isdir(folder):
        continue
    
    # iterate over each file (essay)
    for itemname_2 in os.listdir(folder):
        file = os.path.join(folder, itemname_2)
        # checking if it is a file
        if not os.path.isfile(file):
            continue

        essay_id = file[(file.index('y_') + 2) : file.index('.')]

        # read file
        with open(file, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            # indexes that separate each chunk of text
            sep_indexes = [
                lines.index('Essay:\n', 2, 20),
                lines.index('Revised:\n', 7, 40),
                lines.index('Task Response:\n', 20),
                lines.index('Coherence and Cohesion:\n', 20),
                lines.index('Lexical Resource:\n', 20),
                lines.index('Grammatical Range and Accuracy:\n', 20),
                lines.index('Score:\n', 40)
            ]
            topic = lines[1:sep_indexes[0]]
            topic = ''.join(topic).strip()

            essay = lines[sep_indexes[0] + 1: sep_indexes[1]]
            essay = ''.join(essay).strip()

            revised = lines[sep_indexes[1] + 1: sep_indexes[2] - 2]
            revised = ''.join(revised).strip()

            tr = lines[sep_indexes[2] + 1: sep_indexes[3]]
            tr = ''.join(tr).strip()

            cc = lines[sep_indexes[3] + 1: sep_indexes[4]]
            cc = ''.join(cc).strip()

            lr = lines[sep_indexes[4] + 1: sep_indexes[5]]
            lr = ''.join(lr).strip()

            ga = lines[sep_indexes[5] + 1: sep_indexes[6]]
            ga = ''.join(ga).strip()

            token = token_to_call("r50k_base", topic + essay, tr)
            if token > 2040:
                n_tok_exceed += 1
                print(essay_id)



print(n_tok_exceed)

"""
Hãy làm ngắn  trong khoảng 1300 tokens và không dịch những cụm từ trong ngoặc kép. Hãy giữ lại càng nhiều ví dụ.
"""
