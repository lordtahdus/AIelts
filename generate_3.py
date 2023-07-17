import openai
from decouple import config

from similarity_check import *
from link_check import *

def run():
    global generated_content
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
            # Add generated output to do similarity check
            generated_content += reply
            # save general feedback in messages but not print 
            if i == 1:
                messages.append({"role": "assistant", "content": reply})
            else:
                print(reply + '\n\n', file = f)
            

if __name__ == "__main__":
    openai.api_key = config('OPENAI_KEY_3')

    messages = []
    generated_content = ""
    system_msg = "Ielts writing editor"
    messages.append({"role": "system", "content": system_msg})

    ##################################################
    index = 213

    link = "https://writing9.com/text/64a14dc3d38ec40018b4e59e-nowadays-women-as-well-as-men-work-full-time-therefore-women"

    topic = """\
Nowadays, women, as well as men, work full-time. Therefore, women and men should share household tasks equally. (e.g. cleaning and looking after children). To what extent do you agree or disagree?
"""

    essay = """\
Recent trends show that both men and women are working full-time compared to older days. Some people think that men cannot do most of the household tasks, whereas others argue that men should equally do work at home to help women. Balancing the household tasks equally for both is always debatable. 

To begin with, men always feel that they are responsible for managing the economic situation of the family such as daily needs, expenses, children's education and financial growth. So this contributes to men's mindset to focus on the financial stability of the family. Although women are responsible for children's needs, cooking, washing clothes and cleaning etc. For example these factor affects the recent days, where women are equally contributing to the family by working full time and managing household work is quite difficult these days. 

On the other hand, mature people think that they are equally responsible for household work to help women to be more balanced inside and outside the home. These people help out with cleaning, teaching kids, washing clothes, etc. where women need help with their day-to-day activities. Hence balancing  work at home would help to have a peaceful and understanding life between couples to avoid misunderstandings or conflicts. My colleagues experienced problems when they do not share the workload at home due to women facing more workloads and suffering. 

To conclude, I strongly agree that men should equally share the tasks with women at home to lead a peaceful and healthy life. With the growing culture of women working full-time and it would continue for future years, men should understand the difficulty and support women the most in the living location.
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
        
        print(f".....Generating essay {index}.....")

        run()

        # Print similarity score
        og_content = topic + essay
        score = similarity_check([og_content, generated_content])
        print(score)

        with open('similar_scores.csv', "a") as f:
            f.write(f"\nEssay {index}: {score}")

        # append the link in the links.csv
        with open('links.csv', "a") as f:
            f.write(f"\n{link}")

        print('DONE !!!')