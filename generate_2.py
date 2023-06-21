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
    openai.api_key = config('OPENAI_KEY_2')

    messages = []
    system_msg = "Ielts writing editor"
    messages.append({"role": "system", "content": system_msg})

    ##################################################

    index = 132

    link = 'https://writing9.com/text/5fdddd029c0924001808472d-new-technologies-have-changed-the-way-fro-children-to-spend'

    topic = """\
New technologies have changed the way fro children to spend their free time do the advantages outweigh the disadvantages\
"""

    essay = """\
The advanced technoligies is changing children's free time. Some poeple claim that will creat bad influences to child but i think new technologies have benifites to them.

Adimittedly, the advanced technologies are agreing now due to media report lots of negative news such as a child does not make any relationships because drop into the computer and mobile phone but that is not means teachnologies caused this event to happen. The besically reason is children using it not very well beacuse thet are so young and thet can not control themselves.

In my opinion, technologies are good for children and it is destined to play a important role in children's life. The technologies are not just game, children can get knowlegdes and more deeper insight in what disguss in classes and contacting with world through it. We are in a fast-changingcentury if children fo not know how to manipulate technologies such as new system of computer and mobile phone even virtual technologies they will be kept from society. Technologies are friends to children, thet always playing with them when they are with out families. When they want to play with technologies they have to focus on them and consider the methods of technologies' using that will lead children explore then they will be more smart. Everything borns for a reason. Children spent more time in advanced technologies is normal now they need to changing and  catch up the world rather than let the world be suit with them. 

In conclusion, people have to teach children how to make a good relationship with advanced technologies rather than criticize it.\
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
            "Đánh giá Task Response trong bài viết của tôi một cách chi tiết hơn. Bài viết của tôi có trả lời đúng câu hỏi đề bài không? Nếu không, nêu ra ví dụ để cải thiện.\nĐây là cấu trúc của đánh giá:\n<Lỗi cần cải thiện>\n<Ví dụ cải thiện>",
            "Đánh giá Coherence and Cohesion trong bài viết của tôi một cách chi tiết hơn. Bài viết của tôi có sự liên kết mạch lạc và hợp lí giữa tất cả các ý và các câu không? Nếu không, nêu ra ví dụ để cải thiện.\nĐây là cấu trúc của đánh giá:\n<Lỗi cần cải thiện>\n<Ví dụ cải thiện>",
            "Đánh giá Lexical Resource trong bài viết của tôi một cách chi tiết hơn. Bài viết của tôi có mắc lỗi sai về từ vựng không? Nếu có, liệt kê tất cả lỗi sai.\nĐây là cấu trúc của đánh giá:\n<Lỗi cần cải thiện>\n<Ví dụ cải thiện>",
            "Đánh giá Grammatical Range and Accuracy trong bài viết của tôi một cách chi tiết hơn. Bài viết của tôi có mắc lỗi sai về ngữ pháp không? Nếu có, liệt kê lỗi sai tất cả lỗi sai.\nĐây là cấu trúc của đánh giá:\n<Lỗi cần cải thiện>\n<Ví dụ cải thiện>",
            "Estimate carefully the score of each criteria"
        ]
        headings = [
            "Feedback:\n\nTask Response:\n",
            "Coherence and Cohesion:\n",
            "Lexical Resource:\n",
            "Grammatical Range and Accuracy:\n",
            "Score:\n\nOverall:\n\nScore_TR:\nScore_CC:\nScore_LR:\nScore_GA:\n"
        ]
        
        print(".....Generating.....")

        run()

        # append the link in the links.csv
        with open('links.csv', "a") as f:
            f.write(f"\n{link}")

        print('DONE !!!')