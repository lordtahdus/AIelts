import openai
from decouple import config

from link_check import *

def run():
    # while input != "quit()":
    with open(f"processed_essay/essay_{index}.txt", "a", encoding="utf-8") as f:
        for i in range(0,7):
            message = syntaxes[i]
            # Revised
            if i == 0:
                messages.append({"role": "user", "content": message})
                print("Revised:\n", file = f)
            # General feedback
            elif i == 1:
                messages.pop(1)
                messages.append({"role": "user", "content": message})
            # Specific Criteria and Score
            else:
                if len(messages) == 4:
                    messages.pop(3)
                messages.append({"role": "user", "content": message})
                print(headings[i-2], file = f)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages)
            reply = response["choices"][0]["message"]["content"]

            # save general feedback in messages but not print 
            if i == 1:
                messages.append({"role": "assistant", "content": reply})
            else:
                print(reply + '\n\n', file = f)
            

if __name__ == "__main__":
    openai.api_key = config('OPENAI_KEY_1')

    messages = []
    system_msg = "Ielts writing editor"
    messages.append({"role": "system", "content": system_msg})

    ##################################################

    index = 78

    link = "b"

    topic = """\
Unemployment remains the biggest challenge to school-leavers in most countries.

How far do you agree with this assessment?\
"""

    essay = """\
In recent years, unemployment became the biggest problem for the young generation all over the world. There are several other challenges which are currently being faced by the students right after their college such as, relationship failures, loss of self-identity, drug addiction, etc. In this essay, I will provide my opinion on this assessment, as I mostly agree to this and will elaborate on various other obstacles that folks are facing soon after their education.\
"""

    ##################################################

    link_status = check_csv('links.csv' , link)
    # Check Link if exsited
    if link_status:
        print("FOUND!")
    else:
        print("NOT FOUND!!!! 8==3")
        # create new text file
        with open(f"processed_essay/essay_{index}.txt", "w") as f:
            f.write(f"""Topic:\n\n"{topic}"\n\nEssay:\n\n"{essay}"\n\n\n""")
        
        syntaxes = [
            f'This is IELTS writing task 2.\n\nTopic:\n"{topic}"\n\nEssay:\n"{essay}"\nPlease edit the essay according to IELTS structure',
            f'This is IELTS writing task 2.\n\nTopic:\n"{topic}"\n\nEssay:\n"{essay}"\nPlease provide me detailed feedback in Vietnamese with clear explanations, based on four scoring criteria:\nTask Response\nCoherence and Cohesion\nLexical Resource\nGrammatical Range and Accuracy',
            "Đánh giá Task Response trong bài viết của tôi một cách chi tiết hơn và nêu ra gợi ý cải thiện (nếu có)",
            "Đánh giá Coherence and Cohesion trong bài viết của tôi một cách chi tiết hơn và nêu ra lỗi sai (nếu có)",
            "Đánh giá Lexical Resource trong bài viết của tôi một cách chi tiết hơn và nêu ra lỗi sai (nếu có)",
            "Đánh giá Grammatical Range and Accuracy trong bài viết của tôi một cách chi tiết hơn và nêu ra lỗi sai (nếu có)",
            "Estimate carefully the score of each criteria"
        ]
        headings = [
            "Feedback:\n\nTask Response:\n",
            "Coherence and Cohesion:\n",
            "Lexical Resource:\n",
            "Grammatical Range and Accuracy:\n",
            "Score:\n\nOverall:\n\nScore_TR:\nScore_CC:\nScore_LR:\nScore_GA:\n"
        ]
        
        run()

        # append the link in the links.csv
        with open('links.csv', "a") as f:
            f.write(f"\n{link}")

        print('DONE')