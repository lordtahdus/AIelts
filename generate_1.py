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

    index = 64

    link = "https://writing9.com/text/6473113a7e89e60018c80bac-some-people-think-that-newly-built-houses-should-follow-the"

    topic = """\
Some people think that newly built houses should follow the style of old houses in local areas. Others think that people should have freedom to build houses of their own style. Discuss both these views and give your own opinion.\
"""

    essay = """\
There are those who think that people who make houses newly have to comply with the traditional style in municipal areas, whereas others consider that they have to design their own residences by themselves. Deciding whether or not it is wise to own style is subjective but for many it can be positive. 

On the one hand, if new citizens follow the conventional custom to create their dwellings, it would render the scenery of the town beautiful. To be specific, it would make the local area more famous in the country. For instance, one city in Kyoto decided a rule of building to oblige the traditional form in 2018, it generated some positive effects on the residents and town because it became the most popular area in Japan in 2020. Thus, this trend would produce some beneficial results. 

on the other hand, a lot of individuals build their own dwellings since they want to live in their favorite houses. It means that house owners design what they would like to do in their own residences. To illustrate, many families attach a garden in their houses to fulfill their hope such as playing with their children or watching nature. Hence, if newcomers are able to erect their home freely, they can design what they like. 

In my view, it depends on what house the person like to live in. There is no specific residence that fits everyone, and I think if individuals think that harmony with other residents is more essential than their favorites, they should comply the rule of old house, and vice versa. 

In conclusion, there are pros and cons for traditional custom and own style. It depends on the individual’s choice. Therefore, people have to consider what they want to obtain from their own buildings.\
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