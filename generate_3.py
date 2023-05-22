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

    index = 59

    link = 'https://writing9.com/text/646a32e37e89e60018c7f9a2-do-you-agree-or-disagree-with-the-following-statement-it'

    topic = """\
Do you agree or disagree with the following statement: “It is better to be a follower than a leader.”\
"""

    essay = """\
In daily lives people have various positions in various parts of the world. A differentiation occurs between leaders and followers. Some people prefer to be a leader and free; nonetheless, others like to be a follower and depend on others. As far as I am concerned, I would rather be a leader instead of being a follower.

Initially, a leader is a director of a group and they are able to decide freely by considering both themselves and their group. They can decide or act independently when compared to followers and other members of the group. It is a fact that, sometimes, conversations and brainstorming can be necessary to find the optimum choice, however, a leader can make a decision by themselves in a risky situation without discussions. Or even a leader can follow their own path when conflicts arise because of clash of ideas since they have the power among the group. Therefore, a leader is the independent symbol of the group and they are able to play the dominator role of a group.

Secondly, a person can gain confidence by being a leader and they can use their increased confidence in diverse areas. Followers often involved in such discussions or conflicts, they are not sufficiently able to apply their own ideas. Nevertheless, by leading a society or crowd, leaders incessantly obtain self-confidence. They start to decide more legitimately and calmly when they encounter stressed and pressuring difficulties with the help of their confidence. Moreover, this confidence can assure accomplishment for leaders. In different parts of their lives, they may be successful and canalize others with a sense of self-confidence., which could bring success  Consequently, being a leader also helps people to be more confident and fulfill in different areas.

To sum up, being a leader has positive effects and consequences. First, it helps to be more free and independent. Second, it also ensures being confident and determined. Up to me, I would definitely prefer to be a leader.\
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