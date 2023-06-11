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

    index = 110

    link = "https://writing9.com/text/5ca027656ee679cd043e1255"

    topic = """\
More and more people want to own famous brands of cars, clothes and other items. What are the reason for this. Is this a positive or negative trend?\
"""

    essay = """\
Nowadays, the trend of purchasing well-known brands of vehicles, clothes and other goods has been increasing. This raises the question why it is happening and how society will be effected. From my perspective, I suppose it will have a negative impact on society.
There are many compelling reasons why more and more people are obsessed with owning the famous brand of items. Firstly, Owing to the availability of mass media, people might be unconciously overwhelmed by commercials which display captivating fashion pieces  by touching the smart phone, watching TV or even walk on the street. Therefore, the repetitive slogan and remarkable logo of some famous brands are planted into their brains. Not only young people but also elderly people are the target of advertising agencies. Another explanation is their desire for social acceptance that drives them into  buying well reputed and expensive to show off and post their stunning pictures on social media like Facebook, etc,. to attract more attention and admiration. Lastly, famous brand ‘s popularity and high cost are often supposed to associate with the high-qualified items so consumers often flick into to purchase the well-known brands.
Nonetheless, as I believe this trend is largely detrimental to this country’s tradition and culture. Because a country’s history and customs have a strong tie to the existence of domestically produced goods . If the endless development of world-renowned brands continues, these famous items will expel the locally made products from commodity market, thus the disappearance of domestic product, lead to the economic crisis in the future. Given the dominance of the internationally famous brands, this will create the clothing styles difference in poverty and wealth, leading to the background discrimination.
To summarize,  the well-known commodities have a negative influence in domestically made products consumption, society and economic rate of a country due to the excessive advertising.\
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