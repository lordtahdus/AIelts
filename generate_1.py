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

    index = 47

    link = 'https://www.ieltsbuddy.com/ielts-band-5-essay-samples.html'

    topic = """\
Some of the methods used in advertising are unethical and unacceptable in today’s society.
To what extent do you agree with this view?\
"""

    essay = """\
Nowadays in worldwide nations, every moment, we are displayed advertisements on TV shows, magazines or huge LED boards situated on intersections. In what methods they are produced or how much producers care about ethical trend to making them? I believe they intent to have more watcher to earn more money regardless to its consequences.

In first point of view, some families my does not need something that is displaying on tv, but as home wife see the advertisement will feel that is a good idea to have it and decide to buy it immediately. In another case, there is families who have young offspring who mentally is not wise enough to perceive everything in family situation. Therefore, they will have high demand while they are watching a new toy advertisement. Begging his parent to purchase it and crying all time. As a result his poor father will be finally obliged to buy the toy.

In second point, they may use psychological weaknesses; for example, by displaying a young lady with fitness body who is using some stuff on show to attract people for the good. It may apparently not so bad, but if we go deep in down will understand that how it may have an effect of youth brain and corrupt it.

Or by using a charming sentences on cigarette box "the ideal of a manhood" as a person see this advertisement on the box, will feel himself on his dreams and will buy it.

In conclusion, the advertisement makers, regardless to the bad effects the advertise may cause on people, will made them due to make their customers satisfying. But it may have bad consequences on society which due to avoiding this trend i suggest authorities make some plans for the circumstance to check and control advertisements before showing up.\
"""

    ##################################################

    link_status = check_csv('links.csv' , link)
    # Check Link if exsited
    if link_status:
        print("FOUND!")
    else:
        print("NOT FOUND!!!! 8==3")
        with open('links.csv', "a") as f:
            f.write(f"{link}")
        # create new text file
        with open(f"processed_essay/essay_{index}.txt", "w") as f:
            f.write(f"""Topic:\n\n"{topic}"\n\nEssay:\n\n"{essay}"\n\n""")
        
        syntaxes = [
            f'This is IELTS writing task 2.\n\nTopic:\n"{topic}"\n\nEssay:\n"{essay}"\nPlease edit the essay according to IELTS structure',
            f'This is IELTS writing task 2.\n\nTopic:\n"{topic}"\n\nEssay:\n"{essay}"\nPlease provide me detailed feedback in Vietnamese with clear explanations, based on four scoring criteria:\nTask Response\nCoherence and Cohesion\nLexical Resource\nGrammatical Range and Accuracy',
            "Đánh giá Task Response trong bài viết của tôi một cách chi tiết hơn và nêu ra lỗi sai (nếu có)",
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