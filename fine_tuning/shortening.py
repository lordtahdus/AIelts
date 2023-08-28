"""
THIS PROGRAM SHORTEN THE ESSAYS

        UNFINISHED
"""

import json
import os
from finetune_tools import token_to_call
from typing import List

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

def get_sep_indexes(lines):
    sep_indexes = [
        lines.index('Essay:\n', 2, 20),
        lines.index('Revised:\n', 7, 40),
        lines.index('Task Response:\n', 20),
        lines.index('Coherence and Cohesion:\n', 20),
        lines.index('Lexical Resource:\n', 20),
        lines.index('Grammatical Range and Accuracy:\n', 20),
        lines.index('Score:\n', 40)
    ]
    return sep_indexes

def get_contents_each_essay(lines, sep_indexes) -> List:
    """
    Breakdown the essay and return a list of 8 elements
        0-Topic | 1-Essay | 2-Revised | 3-TR | 4-CC | 5-LR | 6-GA | 7-Score
    """
    topic = lines[1:sep_indexes[0]]
    essay = lines[sep_indexes[0] + 1: sep_indexes[1]]
    revised = lines[sep_indexes[1] + 1: sep_indexes[2] - 2]
    tr = lines[sep_indexes[2] + 1: sep_indexes[3]]
    cc = lines[sep_indexes[3] + 1: sep_indexes[4]]
    lr = lines[sep_indexes[4] + 1: sep_indexes[5]]
    ga = lines[sep_indexes[5] + 1: sep_indexes[6]]
    score = lines[sep_indexes[6] + 2:]
    contents = [
        ''.join(topic).strip(),
        ''.join(essay).strip(),
        ''.join(revised).strip(),
        ''.join(tr).strip(),
        ''.join(cc).strip(),
        ''.join(lr).strip(),
        ''.join(ga).strip(),
        ''.join(score).strip()
    ]
    return contents

def run(shorten_part: int):
    n_tok_exceed = 0
    assert shorten_part in [3,4,5,6], "Only 3, 4, 5 ,6"
    # begins the loop
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
                # breakdown the essay into 8 elements (parts)
                sep_indexes = get_sep_indexes(lines)
                contents = get_contents_each_essay(lines, sep_indexes)
                # get which part that need to be shortened
                shorten_content = contents[shorten_part]
                token = token_to_call("r50k_base", contents[0] + contents[1], shorten_content)
                if token > 2040:
                    n_tok_exceed += 1
                    print(essay_id)
    print(n_tok_exceed)


if __name__ == "__main__":
    main_directory = 'assets/unassessed_essays'
    n_tok_exceed = 0
    print(n_tok_exceed)

    syntax = "Hãy làm ngắn trong khoảng 1300 tokens và không dịch những cụm từ trong ngoặc kép. Hãy giữ lại càng nhiều ví dụ."
    
    run(4)
