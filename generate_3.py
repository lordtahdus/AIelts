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
    index = 210

    link = "https://writing9.com/text/649c3f1d8824d200198b8519-in-some-countries-it-is-thought-advisable-that-children-begin"

    topic = """\
In some countries it is thought advisable that children begin formal education at four years old, while in others they do not have to start school until they are seven or eight.

How far do you agree with either of these views?
"""

    essay = """\
Age is a vital factor for children to learn. It is stated that children in some countries begin their formal education when they are four years old. Conversely, others started school at seven or eight years old. Personally, children should start learning at the age of seven. Their brain is ready for learning at this age. Children at seven will Study more effectively. There are reasons to support this view. 

To start with, Children at seven have a higher ability to learn. They are grown up enough for learning and understanding efficiently. Since their brain is developed enough to distinguish situations, they can learn with more comprehension. They are able to take better advantages from their brain at this age. When their brain is developed, they will be able to gain a lot of advantages from that. They can comprehend easy things faster than those who start to learn at a young age. This means that starting to teach children at age of seven will provide more advantages for children. 

Next, children at this age will be able to control and manage their stress and behavior while studying. This is an essential reason because they need to be able to focus particularly on their task. They can manage their emotions while learning. This cannot be taught to kids at four. They are too young to control their behavior and emotions in the classroom. Therefore, pupils at the age of seven can control themselves to focus on lessons. This means that children at seven will have enough maturity to control themselves.  

On the other hand, some countries send kids to go on formal education while they are just four. This can motivate children to learn since they were young. They can be taught the skill of learning at a young age, so they can learn more easily when they are grown up. However, the age of four should be a period of playing and entertaining. Since at this age it is too complicated for kids to learn in a formal lesson. Therefore, it is not the right time to send them to school. 

In conclusion, children should be taught in a formal lesson when they are seven. Kids at this age have a higher ability to learn. Their brain is developed enough to comprehend the lesson. In addition, they are grown enough to control themselves while learning. Children at age four are not grown enough to control themselves.
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