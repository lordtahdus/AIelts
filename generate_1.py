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

    index = 53

    link = 'https://writing9.com/text/5e2689aebe852b00187b65a2'

    topic = """\
Some people think that money is the best gift for teenagers. Others disagree. Discuss both these views and give your opinion.\
"""

    essay = """\
Nowadays, people give a gift to their family, relatives, and friends in different outstanding circumstances like birthday, wedding ceremony, etc. Some people believe money is the best gift to give youngsters, but to the best of my knowledge, I completely disagree with this statement.
On the one hand, money is a better present in today’s sluggish economic condition than. Money helps adolescents to balance their expenditures and also instead of receiving unsurprising presents, it helps them to act independently. They can readily manage their budgets and acquire exactly what they need. For more clarification, I mention an example of my own experience here. About eight years ago before my twenty-year-old birthday, I got in trouble and needed money. Close friends of mine and my parents, as they knew my poor economic condition, decided to give me money as a gift on my birthday that helped me to handle that situation. Undoubtedly, it is one of the best presents that I have ever experience in my life and never be forgotten.
On the flip side, some people disagree that money is the best gift to give. Gifts must be different in each situation due to various factors such as ambiance, age, type, etc., so choosing a present among the various infinite gifts would be an invaluable job. It helps us to experience a distinct sense that someone spends his or her time to elect a gift that is fitted or can fill our needs. Moreover, gifts have spiritual values and we don’t assess or compare them with money. Each present besides its feeling and energy remains in our mind forever. It helps us to create a distinguished picture of our personalities and be alive in their minds. Also giving money is not good at all ambiances. About two months ago, I read a paper that conducted a survey to be aware of the tastes or manners of newly married couples. The paper stated that over 87% of the couples don’t prefer to receive money from each other and to some extent in some cases, they mentioned that their feelings and attitudes toward their wife or husband can be affected by this gift.
To recapitulate, it is clear that the disadvantages of giving money as a gift outweigh its advantages, so I do recommend to those who want to select a gift, each gift has an individual sense and money can’t act be a sense.\
    """

    ##################################################

    link_status = check_csv('links.csv' , link)
    # Check Link if exsited
    if link_status:
        print("FOUND!")
    else:
        print("NOT FOUND!!!! 8==3")
        with open('links.csv', "a") as f:
            f.write(f"\n{link}")
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