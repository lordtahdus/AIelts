import openai
import os

from decouple import config

openai.api_key = config('OPENAI_KEY_1')

messages = []
system_msg = "Ielts writing editor"
messages.append({"role": "system", "content": system_msg})










def run():
    # move the old_essay to old_essay folder
    os.rename(f'processed_essay/essay_{index}.txt', f'old_essay/essay_{index}.txt')

    user_options = [0,0,0,0,0,0,0]
    print('input 0 or 1')
    user_options[0] = int(input('Regenerate Revised? '))
    user_options[2] = int(input('Regenerate Task Response? '))
    user_options[3] = int(input('Regenerate Coherence and Cohesion? '))
    user_options[4] = int(input('Regenerate Lexical Resource? '))
    user_options[5] = int(input('Regenerate Grammatical Range and Accuracy? '))
    user_options[6] = int(input('Regenerate Score? '))

    # check for all user inputs are 0 and 1
    for option in user_options:
        assert option in [0,1], "Your input should be only 0 and 1"

    # write the new generated output
    with open(f"processed_essay/essay_{index}.txt", "w", encoding="utf-8") as f:
        f.write(f"""Topic:\n\n{topic}\n\nEssay:\n\n{essay}\n\n""")

        for i in range(0,7):
            message = syntaxes[i]
            # Revised
            if i == 0 and user_options[i] == 1:
                messages.append({"role": "user", "content": message})
            # General feedback
            elif i == 1:
                if len(messages) == 2:
                    messages.pop(1)
                messages.append({"role": "user", "content": message})
            # Specific Criteria and Score
            elif user_options[i] == 1:
                if len(messages) == 4:
                    messages.pop(3)
                messages.append({"role": "user", "content": message})

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens= 500)
            reply = response["choices"][0]["message"]["content"]

            # save general feedback in messages but not print 
            if i == 1:
                messages.append({"role": "assistant", "content": reply})
            else:
                f.write(headings[i])
                if user_options[i] == 0:
                    f.write(contents[i] + '\n\n\n')
                else:
                    f.write(reply + '\n\n\n')



if __name__ == "__main__":
    index = int(input("Which essay to regen (enter number)? "))
    file = f'processed_essay/essay_{index}.txt' 
    with open(file, 'r', encoding="utf-8") as f:
        lines = f.readlines()

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
        tr = lines[sep_indexes[2] + 1: sep_indexes[3]]
        cc = lines[sep_indexes[3] + 1: sep_indexes[4]]
        lr = lines[sep_indexes[4] + 1: sep_indexes[5]]
        ga = lines[sep_indexes[5] + 1: sep_indexes[6]]
        score = lines[sep_indexes[6] + 2:]

        contents = [
            ''.join(revised).strip(),
            '',
            ''.join(tr).strip(),
            ''.join(cc).strip(),
            ''.join(lr).strip(),
            ''.join(ga).strip(),
            ''.join(score).strip()
        ]

    syntaxes = [
        f'This is IELTS writing task 2.\n\nTopic:\n"{topic}"\n\nEssay:\n"{essay}"\nPlease edit the essay according to IELTS structure',
        f'This is IELTS writing task 2.\n\nTopic:\n"{topic}"\n\nEssay:\n"{essay}"\nPlease provide me detailed feedback in Vietnamese with clear explanations, based on four scoring criteria:\nTask Response\nCoherence and Cohesion\nLexical Resource\nGrammatical Range and Accuracy',
        "Đánh giá Task Response trong bài viết của tôi một cách chi tiết hơn. Bài viết của tôi có trả lời đúng câu hỏi đề bài không? Nếu không, nêu ra ví dụ để cải thiện.",
        "Đánh giá Coherence and Cohesion trong bài viết của tôi một cách chi tiết hơn và liệt kê lỗi sai (nếu có)",
        "Đánh giá Lexical Resource trong bài viết của tôi một cách chi tiết hơn và liệt kê lỗi sai (nếu có)",
        "Đánh giá Grammatical Range and Accuracy trong bài viết của tôi một cách chi tiết hơn và liệt kê lỗi sai (nếu có)",
        "Estimate carefully the score of each criteria"
    ]
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
    print("DONE!!")