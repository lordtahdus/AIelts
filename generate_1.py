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

    index = 190

    link = "https://writing9.com/text/60832dd405dcca0018f95fba-some-believe-it-is-important-for-cities-and-towns-to"

    topic = """\
Some believe it is important for cities and towns to invest heavily in building large outdoor public spaces.

To what extent do you agree or disagree?\
"""

    essay = """\
With the development of populations in cities and towns, the living density is rising sharply in recent years. People need more outdoor space to relax and take activities, so I think it is important to invest suitably in building outdoor public areas, not heavily.

Building large outdoor public space in the city and town could provide an area for the citizen to relax and enjoy the free time. Due to the heavy working stress in the office, people need an outdoor space to relax. In addition, most public parks or outdoor activity areas are close to the huge community. Residents could easily arrive there, and walk around or play with their children. For instance, I live in the city place area, there is a huge public area in front of my apartment. There are a dog park, soccer field, and some activity equipment. I saw a lot of people went to the park when they get off work. Some people were walking their dogs, and some people play with their children. Therefore, the outdoor public field is an important relaxing place in people’s daily life. 

However, although building outdoor public is beneficial to citizen, that does not mean the government needs to invest a lot of funding into that. A suitable amount of money is acceptable. For example, the government need to research the data of public construction expense every year for all districts in the city and town. Moreover, the authority should arrange a number of investment reasonably for building public parks and activities. After they made the decision, residents have the right to vote to agree or disagree. If do so, it will be an effective way to control the cost of public construction. Therefore, the government could support the construction of the public space, but investing a reasonable amount of money is acceptable.

In conclusion, for this discussion, I agree to build more public outdoor areas in cities and towns, because people need this kind of place to relax and enjoy the leisure time. However, the government needs to control the investment. The amount of spending should be calculated in advance.\
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