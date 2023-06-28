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
    openai.api_key = config('OPENAI_KEY_3')

    messages = []
    system_msg = "Ielts writing editor"
    messages.append({"role": "system", "content": system_msg})

    ##################################################
    index = 209

    link = "https://writing9.com/text/dnafiqnfnqiniqqádnkankdkqnk"

    topic = """\
Some people think that it is more beneficial to take part in sports which are played in teams, like football, while other people think that taking part in individual sports, like tennis or swimming, is better. Discuss both views and give your own opinion.
"""

    essay = """\
As a human being who wants to get fit from time to time, sports play a big role to make us healthy. There are numerous type of sports in this world, yet, it can be divided into two sections, individual and team sports. While there are still debates over which type is better, here I would like to describe my views on both types and choose which one is better. 

Swimming, tennis, or even running are several sports that consider as individual sports. In this type of sports, our success is highly dependent on our performance and determination to achieve our goals. If the athletes want to be the winner, they must train harder than anyone else and set the goal as high as they can. Our achievements are not relying on outside factors. For example, Usain Bolt as a runner from Jamaica, always comes to the training earlier and trains as hard as he could. Therefore he achieves several medals at the Olympics. 

On the other hand, team sports such as basketball and football  count heavily on teamwork. Even though each individual has tremendous skills, if they cannot work as a team, their team will fail. As social creatures, human cannot life on their own, our life will be depends on someone. Therefore, teamwork will be one of the key for us to survive not only in sports, but also in our entire life. 

To summarize, both individual and team sports have their own benefits, however, to achieve more in sports and also in our life, I rather to choose team sports.
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
            """\
            Đánh giá Task Response trong bài viết của tôi một cách chi tiết hơn theo những tiêu chí sau:
            Yêu cầu đề bài có được trả lời không?
            Bài viết có giải thích đầy đủ tất cả các phần của nhiệm vụ không?
            Ý tưởng có được mở rộng đầy đủ không?

            Nếu có, liệt kê tất cả lỗi sai của Task Response theo cấu trúc sau:
            Lỗi cần sửa
            Ví dụ cho lỗi cải thiện
            """,
            """\
            Đánh giá Coherence and Cohesion trong bài viết của tôi một cách chi tiết hơn theo những tiêu chí sau:
            Bài viết của tôi có sự liên kết mạch lạc và hợp lí giữa tất cả các ý và các câu không?
            Các liên kết câu có tự nhiên và logic không?

            Nếu có, liệt kê tất cả lỗi sai của Coherence and Cohesion theo cấu trúc sau:
            Lỗi cần sửa
            Ví dụ cho lỗi cải thiện

            """,
            """\
            Đánh giá Lexical Resource trong bài viết của tôi một cách chi tiết hơn theo những tiêu chí sau:
            Bài viết của tôi có mắc lỗi sai về từ vựng không?
            Từ vựng dùng có tự nhiên và thích hợp không?

            Nếu có, liệt kê tất cả lỗi sai của Lexical Resource theo cấu trúc sau:
            Lỗi cần sửa
            Ví dụ cho lỗi cải thiện
            """,
            """\
            Đánh giá Grammatical Range and Accuracy trong bài viết của tôi một cách chi tiết hơn theo những tiêu chí sau:
            Bài viết của tôi có mắc lỗi sai về ngữ pháp không?
            
            Nếu có, liệt kê tất cả lỗi sai của Grammatical Range and Accuracy theo cấu trúc sau:
            Lỗi cần sửa
            Ví dụ cho lỗi cải thiện
            """,
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