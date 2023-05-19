import openai
import os

from decouple import config

openai.api_key = config('OPENAI_KEY_1')

messages = []
system_msg = "Ielts writing editor"
messages.append({"role": "system", "content": system_msg})



index = 40




file = f'processed_essay/essay_{index}.txt' 

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
    topic = ''.join(topic).strip()

    essay = lines[sep_indexes[0] + 1: sep_indexes[1]]
    essay = ''.join(essay).strip()

    revised = lines[sep_indexes[1] + 1: sep_indexes[2]]
    tr = lines[sep_indexes[2] + 1: sep_indexes[3]]
    cc = lines[sep_indexes[3] + 1: sep_indexes[4]]
    lr = lines[sep_indexes[4] + 1: sep_indexes[5]]
    ga = lines[sep_indexes[5] + 1: sep_indexes[6]]
    score = lines[sep_indexes[6] + 1:]

    contents = [
        ''.join(revised).strip(),
        '',
        ''.join(tr).strip(),
        ''.join(cc).strip(),
        ''.join(lr).strip(),
        ''.join(ga).strip(),
        ''.join(score).strip(),
    ]

    # print(tr)
    # print('\n\n')
    # print(''.join(tr).strip())
    # print(''.join(cc))
    # print(''.join(lr))
    # print(''.join(ga))
    # print(''.join(score))


syntaxes = [
    f'This is IELTS writing task 2.\n\nTopic:\n"{topic}"\n\nEssay:\n"{essay}"\nPlease edit the essay according to IELTS structure. Also, estimate the score.',
    f'This is IELTS writing task 2.\n\nTopic:\n"{topic}"\n\nEssay:\n"{essay}"\nPlease provide me detailed feedback in Vietnamese with clear explanations, based on four scoring criteria:\nTask Response\nCoherence and Cohesion\nLexical Resource\nGrammatical Range and Accuracy',
    "Đánh giá Task Response trong bài viết của tôi một cách chi tiết hơn và nêu ra lỗi sai (nếu có)",
    "Đánh giá Coherence and Cohesion trong bài viết của tôi một cách chi tiết hơn và nêu ra lỗi sai (nếu có)",
    "Đánh giá Lexical Resource trong bài viết của tôi một cách chi tiết hơn và nêu ra lỗi sai (nếu có)",
    "Đánh giá Grammatical Range and Accuracy trong bài viết của tôi một cách chi tiết hơn và nêu ra lỗi sai (nếu có)",
    "Estimate carefully the score of each criteria"
]
headings = [
    "Revised:\n",
    "",
    "Feedback:\n\nTask Response:\n",
    "Coherence and Cohesion:\n",
    "Lexical Resource:\n",
    "Grammatical Range and Accuracy:\n",
    "Score:\n"
]


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
                messages=messages)
            reply = response["choices"][0]["message"]["content"]

            # save general feedback in messages but not print 
            if i == 1:
                messages.append({"role": "assistant", "content": reply})
            else:
                f.write(headings[i])
                if user_options[i] == 0:
                    f.write('\n' + contents[i] + '\n\n')
                else:
                    print(reply + '\n\n', file = f)



if __name__ == "__main__":
    run()