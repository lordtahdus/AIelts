import json
import os
from finetune_tools import token_to_call
from doc.regen_large_scale import get_contents_each_essay


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


def run():
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
                shorten_part = contents[4]
                token = token_to_call("r50k_base", contents[0] + contents[1], shorten_part)
                if token > 2040:
                    n_tok_exceed += 1
                    print(essay_id)


if __name__ == "__main__":
    main_directory = 'assets/unassessed_essays'
    n_tok_exceed = 0
    print(n_tok_exceed)

    """
    Hãy làm ngắn  trong khoảng 1300 tokens và không dịch những cụm từ trong ngoặc kép. Hãy giữ lại càng nhiều ví dụ.
    """
