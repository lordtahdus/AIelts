import openai
import os
from typing import List
from decouple import config

openai.api_key = config('OPENAI_KEY_1')


"""================= READ ME =================

This program regenerate specific parts of the generated output for multiple essays
at once (which are stored in need_regen folder).

The required format is to put "?" next to the headings that need regeneration.
For other parts that don't need regeneration, just leave it blank.

After regenerated successfully, the essay will relocate back to supervised essay,
where we can give another check.

Example:

    Revised:
    Task Response:?
    Coherence and Cohension:
    Lexical Resource:?
    Grammatical Range and Accuracy:

In this case, TR and LR will be regenerated.
"""



# a list saves all the previous messages
messages = []
system_msg = "Ielts writing editor"
messages.append({"role": "system", "content": system_msg})


def get_user_options_and_contents() -> tuple[dict, dict]:
    """
    Get the parts that need to be regenerated for all essays
    """
    user_options_all = {}
    contents_all = {}
    # keys as essay index, values as list of 0 and 1
    directory = "need_regen"

    # get the parts that need regen for each essay
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(file):
            print(file)

        # read file
        with open(file, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            
            # print(lines)

            # initialise for each essay
            essay_index = file[17:-4]
            user_options_all[essay_index] = []
            contents_all[essay_index] = []

            # used to separate the file into multiple parts
            sep_indexes = [
                lines.index('Essay:\n', 2, 10)
            ]

            parts = [
                    "Revised:", "Task Response:", "Coherence and Cohesion:",
                    "Lexical Resource:", "Grammatical Range and Accuracy:", "Score:"
            ]
            for row, item in enumerate(lines):
                for part in parts:
                    if part in item:
                        parts.remove(part) # remove the part when it is first occurred
                        sep_indexes.append(row)
                        if len(item.strip()) != len(part):
                            assert item[len(part)] == "?", "Wrong format"
                            user_options_all[essay_index].append(1)
                        else:
                            user_options_all[essay_index].append(0)
            
            contents_all[essay_index] = get_contents_each_essay(lines, sep_indexes)

    return (user_options_all, contents_all)


def get_contents_each_essay(lines, sep_indexes) -> List:
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
        '',
        ''.join(tr).strip(),
        ''.join(cc).strip(),
        ''.join(lr).strip(),
        ''.join(ga).strip(),
        ''.join(score).strip()
    ]
    return contents


def request_ChatGPT(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens= 500
    )
    reply = response["choices"][0]["message"]["content"]
    return reply


def get_specific_syntaxes(contents_each: List):
    syntaxes = [
        f'This is IELTS writing task 2.\n\nTopic:\n"{contents_each[0]}"\n\nEssay:\n"{contents_each[1]}"\nPlease edit the essay according to IELTS structure',
        f'This is IELTS writing task 2.\n\nTopic:\n"{contents_each[0]}"\n\nEssay:\n"{contents_each[1]}"\nPlease provide me detailed feedback in Vietnamese with clear explanations, based on four scoring criteria:\nTask Response\nCoherence and Cohesion\nLexical Resource\nGrammatical Range and Accuracy',
        """\
Đánh giá Task Response trong bài viết của tôi một cách chi tiết hơn.\
Yêu cầu đề bài có được trả lời không?\
Bài viết có giải thích đầy đủ tất cả các phần của nhiệm vụ không?\
Ý tưởng có được mở rộng đầy đủ không?
Nêu ra những lỗi sai cần được cải thiện và giải thich.
""",
        """\
Đánh giá Coherence and Cohesion trong bài viết của tôi một cách chi tiết hơn.\
Bài viết của tôi có sự liên kết mạch lạc và hợp lí giữa tất cả các ý và các câu không?\
Các liên kết câu có tự nhiên và logic không?
Nêu ra những lỗi sai cần được cải thiện và giải thich.
""",
        """\
Đánh giá Lexical Resource trong bài viết của tôi một cách chi tiết hơn.
Bài viết của tôi có mắc lỗi sai về từ vựng không? Từ vựng dùng có tự nhiên và thích hợp không?

Nếu có, liệt kê tất cả lỗi sai của Lexical Resource theo cấu trúc sau:
<Lỗi cần sửa>
<Giải thích>
""",
        """\
Đánh giá Grammatical Range and Accuracy trong bài viết của tôi một cách chi tiết hơn.
Bài viết của tôi có mắc lỗi sai về ngữ pháp không?

Nếu có, liệt kê tất cả lỗi sai của Grammatical Range and Accuracy theo cấu trúc sau:
<Lỗi cần sửa>
<Giải thích>
""",
        "Estimate carefully the score of each criteria"
    ]
    return syntaxes


def run():

    user_options_all, contents_all = get_user_options_and_contents()
    
    print(".....Start Generating.....")
    
    for essay_index in user_options_all.keys():
        user_options_each: List = user_options_all[essay_index]
        contents_each: List = contents_all[essay_index]

        # ChatGPT requesting syntaxes
        syntaxes = get_specific_syntaxes(contents_each)
        
        # check for all user inputs are 0 and 1
        for option in user_options_each:
            assert option in [0,1], "Your input should be only 0 and 1"

        # write the new generated output
        # the regenerated file will have the suffix "...generating..._",
        # which will be remove when the old essay is moved to the old folder
        with open(f"need_regen/essay_{essay_index}...generating..._.txt", "w", encoding="utf-8") as f:
            f.write(f"""Topic:\n\n{contents_each[0]}\n\nEssay:\n\n{contents_each[1]}\n\n""")
            
            print(f"{essay_index}...")
            print(user_options_each)

            user_options_each.insert(1, 0) # this exists because of General Feedback

            # loop through all parts and regenerate the chosen parts
            for i in range(0,7):

                ### Save the messages to request
                message = syntaxes[i]
                # Revised
                if i == 0 and user_options_each[i] == 1:
                    messages.append({"role": "user", "content": message})
                # General feedback
                elif i == 1:
                    if len(messages) == 2:
                        messages.pop(1)
                    messages.append({"role": "user", "content": message})
                # Specific Criteria and Score (i = 2,3,...6)
                elif user_options_each[i] == 1:
                    if len(messages) == 4:
                        messages.pop(3)
                    messages.append({"role": "user", "content": message})

                ### Request ChatGPT
                if i==1 or user_options_each[i] == 1:
                    reply = request_ChatGPT(messages)

                ### Save general feedback in messages but not print 
                if i == 1:
                    messages.append({"role": "assistant", "content": reply})
                    
                ### Write revised + specific feedback + score into the new file
                else:
                    f.write(headings[i])
                    # old part
                    if user_options_each[i] == 0:
                        f.write(contents_each[i+2] + '\n\n\n')
                    # regenerated part
                    else:
                        f.write(reply + '\n\n\n')

        # move the old_essay to old_essay folder
        os.replace(f'need_regen/essay_{essay_index}.txt', f'old_essay/essay_{essay_index}.txt')
        # remove the suffix "...generating..._" for the regenerated and move to processed folder
        os.replace(f"need_regen/essay_{essay_index}...generating..._.txt", f"processed_essay/essay_{essay_index}.txt")

        print(f"DONE {essay_index}\n")


if __name__ == "__main__":
    # used to write in the new file
    headings = [
        "Revised:\n\n",
        "",
        "Feedback:\n\nTask Response:\n\n",
        "Coherence and Cohesion:\n\n",
        "Lexical Resource:\n\n",
        "Grammatical Range and Accuracy:\n\n",
        "Score:\n\n"
    ]
    run()
    print(" !! DONE ALL !!")