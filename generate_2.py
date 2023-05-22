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
    openai.api_key = config('OPENAI_KEY_2')

    messages = []
    system_msg = "Ielts writing editor"
    messages.append({"role": "system", "content": system_msg})

    ##################################################

    index = 60

    link = 'https://writing9.com/text/64692c7d7e89e60018c7f813-some-people-fail-in-school-but-end-up-being-successful'

    topic = """\
Some people fail in school, but end up being successful in life.

Why do you think that is the case?
What is the most important thing to succeed in life?\
"""

    essay = """\
In our society we are taught that the person who has the best scores in school, is the one that it’s going to succeed most in life. However, that is not always the case. In my opinion, this happens a because the real life is more about how agile and active is somebody when doing their job. Therefore, the most important characteristic that someone could have to succeed it’s to be hard worker.

The knowledge it’s so important in any job because this helps to do things in the right way.Nevertheless, if someone has a lot of information in their brain, but they don’t have a good attitude to work, they are not going to progress in their life. My own personal experience is a good proof of this.

When I was in school, I had a friend called Maria who was the best student during my whole career. She had the best scores in my class. But, when we had to go to practice with animals, she was the worst. She couldn’t handle a cow; she was always having a bad attitude, being lazy, and she didn’t want to help others. Right now, she hasn’t been able to last in any company. I think, this is related to her personality.

Hard worker doesn’t mean to be strong. Being a hard worker means to have the best predisposition to do a good job and finish it fast. People like that are always supporting others, transmitting good vibes, communicating well, learning from failure, and wanting to be better each time. That is what people needs to be successful in life.

To conclude, work hard play harder.\
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