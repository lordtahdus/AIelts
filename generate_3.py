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
    index = 212

    link = "https://writing9.com/text/64a14ea2d38ec40018b4e5a4-the-most-important-aim-of-science-should-be-to-improve"

    topic = """\
The most important aim of science should be to improve people’s lives. 

To what extent do you agree or disagree?
"""

    essay = """\
There is a fact that the improvement of people’s lives should be the most significant purpose of science. I personally agree with this matter. The reasons why I believe will be addressed in this passage.

The most important reason why I advocate this notion is that all investigations need to be funded, in other words, the government should consider some budgets for doing them and this money has been collected from the people. For example, annually the individuals have to pay taxation and as a result, they would be entitled to benefit from the outcomes of the science. Without no money, the scientists will not be able to fulfil their purposes in their projects and they will fail undoubtedly.

Another substantial reason for this opinion is that we are living in a fast-changing world and science plays a vital role in people’s lives. This role can be classified in various aspects. Firstly, technology can help people to benefit from various equipment, for example, computers, smartphones and the Internet. Secondly, science is able to investigate healthcare facilities and introduce new medications to the people perfectly. For example, vaccination is an outstanding approach that results in the crowd is living easier.

In conclusion, there is a statement regarding this fact that the most essential goal of scientific activities should be people’s lives. I personally agree with this matter, due to the fact that the money is needed to afford scientific projects should be gained by the population. Additionally, the science consists of different classifications that are able to assist the society live more convenient such as creation of various appliances and healthcare amenities.
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
        similarity_check([og_content, generated_content])

        # append the link in the links.csv
        with open('links.csv', "a") as f:
            f.write(f"\n{link}")

        print('DONE !!!')