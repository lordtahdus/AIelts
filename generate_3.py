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
    index = 205

    link = "https://writing9.com/text/649506d4fd0ea7001819a34b-some-people-say-that-advertising-encourages-us-to-buy-things"

    topic = """\
Some people say that advertising encourages us to buy things we really do not need. Others say that advertisements tell us about new products that may improve our lives. Which viewpoint do you agree with? Use specific reasons and examples to support your answer.\
"""

    essay = """\
Promoting their products through various channels has been always the most popular tool for the companies to sell their products. Although some people believe that we can discover new merchandise via marketing, I personally agree that the advertisement has the power of convincing people to purchase unnecessary items.

On the one hand, advertisement is required to allow people to learn about the products that can be beneficial to them. Some items specifically made for target audience may not be found in the neighbourhood stores. As a consequence of the development of online marketing, people from all around the world have access to a wide range of products and they can effortlessly order them online.  For instance, my mother has diabetes and she has been dealing with some challenges such as non-healing wounds that come with this disease. One day we saw a TV ad about a scar cream that was specifically produced for diabetes patients. We ordered that cream online and she has been satisfied with the results. I can say that it helped her greatly. If we did not see the on-screen ad about this cream, she would not have had the chance to heal her scars.

On the other hand, marketing has the power of convincing people to purchase the items they do not necessarily require. There are a great number of various products’ promotions on social media, TV and radio. Doubtlessly, we can say that most of these products are not there in aid of people but for the companies’ profit. Additionally, they are designed to create spending temptation. It is hard to withstand especially the discounts or offers accompanying these products. For example, although I create a shopping list every time before I do grocery shopping, I end up buying more items for the reason that the flyers I receive push me to purchase more than I need. There are so many discounts, offers I come across that if I do not take advantage of them, I feel like I would lose a great deal. This is the power that the advertising companies have over us.

In conclusion, although the product promotion have advantages such as helping people find out the items that are beneficial to them, more often than not it triggers people to spend money on the items that they are not in need of.
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