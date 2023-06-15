import os
import json

# assign main directory
main_directory = 'assets'
data = []
# iterate over essay folders in that directory
for itemname in os.listdir(main_directory):
    folder = os.path.join(main_directory, itemname)
    # checking if it is a folder
    if not os.path.isdir(folder):
        continue

    for itemname_2 in os.listdir(folder):
        file = os.path.join(folder, itemname_2)
        # checking if it is a file
        if not os.path.isfile(file):
            continue

        # read file
        with open(file, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            # indexes that separate each chunk of text
            sep_indexes = [
                lines.index('Essay:\n', 2, 10),
                lines.index('Revised:\n', 7, 30),
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
            cc = lines[sep_indexes[3] + 1: sep_indexes[4]]
            lr = lines[sep_indexes[4] + 1: sep_indexes[5]]
            ga = lines[sep_indexes[5] + 1: sep_indexes[6]]
            score = lines[sep_indexes[6] + 2:]
            feedback = [
                ''.join(tr).strip(),
                ''.join(cc).strip(),
                ''.join(lr).strip(),
                ''.join(ga).strip(),
                ''.join(score).strip()
            ]
        # "prompt":"<Topic>\n<Essay>\n\n###\n\n"
        # separator for prompt: \n\n###\n\n
        # "completion":" <detailed feedback> END"
        # stop sequence: END
        # completion starts with a whitespace
        dictionary = {
            "prompt":f"IELTS writing topic:\n{topic}\nEssay:\n{essay}\n\n###\n\n",
            "completion":f" Feedback:\n\
Task Response:{feedback[0]}\n\
Coherence and Cohesion:{feedback[1]}\n\
Lexical Resource:{feedback[2]}\n\
Grammatical Range and Accuracy:{feedback[3]} END"
        }
        json_object = json.dumps(dictionary, ensure_ascii=False)
        data.append(json_object)
        
        # with open("assets/train_feedback_sample.json", "w", encoding="utf-8") as outfile:
            # json.dump(dictionary, outfile, ensure_ascii=False)
            
        
        # handle the essays in old_format folder
        #TODO

        # print(dictionary['prompt'])

with open("fine_tuning/train_feedback_sample.jsonl", "w", encoding="utf-8") as outfile:
    for example in data:
        outfile.write(example)
        outfile.write("\n")

# C:/Users/ADMIN/Documents/GitHub/ielts-bot/assets/train_feedback_sample.jsonl
    