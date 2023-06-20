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

    index = 195

    link = "https://writing9.com/text/5eb2bef8b32f7c00182757f4"

    topic = """\
Some children recieve almost no encouragement from their parents regarding their performance at school, while other children recieve too much pressure from their over enthusiastic parents which can have a negative impacts on the child.
Why do you think some parents put too much pressure on their children to perform well at school?
What do you think the role of a parents should be in their child education?\
"""

    essay = """\
The parents are playing a very essential role behind the success of their offsprings.Fewer guardians do not interfere with toddler school activities.Whereas, some parents show over attitude regarding students' action which have bad effects on the minor development.So, I intend to explore the reasons behind this practice along with parents' responsibility in order to youngsters study.
To regard with cause of why parents put an excess of pressure on children.Firstly, it is true that the parents always think about children better future.Therefore, they force their children to obtain high grades.However, due to this practice, children do not able to maintain focus on performance just because of parents fear.As a result, they choose the wrong path in the term of success like doing the cheating, give money to teachers for high marking and sometimes, skips their classes and exams.Further point is that, childhood is a very crucial stage in the whole life.At that time, toddler decided where they want to make future with the help of parents.Therefore, with love and care children can share their feelings with parents.Yet, due to pressure, they may choose bad society rather than successful life.As a result, bonding with family members may be become weak.
Moving further, parents should take steps wisely while keeping negative and positive outcomes in mind.Moreover, parents select corporal punishment, but somewhere it has negative impacts.Therefore, parents should make strong relationship with children, which act as children may explore their feelings without any fear and worry.By this, parents can make right decision with the aid of adolescent interest.Another point is that, the parents guide children regarding fruitful effects of education along with make schedule for playing and studying which may be proved very effective in order to kid may make mind fresh and sharp.
In conclusion, parents should always treat children in well manner which by this they can avoid bad society and also run into positive path.\
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
            "Đánh giá Task Response trong bài viết của tôi một cách chi tiết hơn. Bài viết của tôi có trả lời đúng câu hỏi đề bài không? Nếu không, nêu ra ví dụ để cải thiện.",
            "Đánh giá Coherence and Cohesion trong bài viết của tôi một cách chi tiết hơn. Bài viết của tôi có sự liên kết mạch lạc và hợp lí giữa tất cả các ý và các câu không? Nếu không, nêu ra ví dụ để cải thiện.",
            "Đánh giá Lexical Resource trong bài viết của tôi một cách chi tiết hơn. Bài viết của tôi có mắc lỗi sai về từ vựng không? Nếu có, liệt kê tất cả lỗi sai.",
            "Đánh giá Grammatical Range and Accuracy trong bài viết của tôi một cách chi tiết hơn. Bài viết của tôi có mắc lỗi sai về ngữ pháp không? Nếu có, liệt kê lỗi sai tất cả lỗi sai.",
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