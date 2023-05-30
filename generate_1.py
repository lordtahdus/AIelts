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

    index = 72

    link = "https://writing9.com/text/6475e70b91cbdc0018c4d6e9-many-children-are-encouraged-by-their-parents-to-get-a"

    topic = """\
Many children are encouraged by their parents to get a part time job in their free time.

What are the advantages and disadvantages to children of doing so?\
"""

    essay = """\
Many children are stimulated by their parents to work in part-time jobs in their leisure time. The main benefits are children are going to be more responsible and they will realise the difficulties of earning money. However, the main drawbacks are a lack of interest in school and unlimited financial independence. 

Children are depending financially on their parents and they need to ask money from their fathers to buy the things they like. When children got a job at an early age, they will be independent individuals economically and, as a result, they will buy whatever they are wishing. If they are working after  school hours, they will have less time to concentrate on their school subject and, consequently, they will fail exams. For example,  students who are using their free time to work, are likely to have less qualified occupations in the future. 

The first advantage is the work that they are working on will make them more responsible. This is to say, having a job is making people more aware of the problems that their parents are facing. Another benefit is children will understand how hard is to earn money. If they are gaining experience in earning money, they will be more careful about the money they are spending. Since they are receiving a salary regularly, they will be more aware of how difficult earn money. For instance, students who start to receive remuneration earlier than their peers, are likely to manage their money more properly. 

To conclude, the positive impacts are children will have more responsibility at an early age and they will understand the importance of money. However, the negative impacts are they will fail in their assignments and have hazardous financial freedom.\
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