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

    index = 185

    link = "https://writing9.com/text/602e066b9e689200183c38d3-the-world-has-seen-an-enormous-increase-in-flights-for"

    topic = """\
The world has seen an enormous increase in flights for leisure,business and commercial purpose around the world over recent years. 
What do you think are the main advantages and disadvantages of such flights?
Do you think flight should be texted more?\
"""

    essay = """\
Exploration to many countries for enjoyment, trades and exchange phenomena for a few decades in the universe is enhancing drastically. From my perspective, the aircraft schedule should be extended more to create a smooth economical flow. This essay will discuss of the merits of the boarding on aeroplane and also describe some related demerits of this issue.

One of the positives of doing business using an aeroplane is to increase the profit of trades. Not only that the development of the exchange issues at the same time, but also it creates a lot of savings of the time issues. Compare to the past men are now very busy with their tasks. To demonstrate, they have to go to various places which distance is too long. As a result, the more time that he lessens, the more making profit can be possible. Another advantage is that, it can reduce physical pressure. For instance, if a person goes abroad he can prosper his tasks and it would be possible if he uses aeroplane for his journey.

Despite these advantages, aircraft is not a cheap issue. Moreover, a folk who is rich in his wealth can be able to use the aeroplane. This is because the costing of manufacturing plane is too high. Hence, the journey is too long to endure it for his body. As a consequence, a person must have physical stamina where he can travel to long-distance for his business works. For example, if a human wants to ordain his journey he has to prepare a lot of money. Therefore, there is no need to add any flight if a person cannot be able to purchase the aircraft journey schedule.

To sum up, using aircraft is required to construct a development of the country's financial condition and in my opinion, the enhancing of flight schedule may make a more prosper for the nation. However, fair for plain travel should be reasonable so that it can be purchasable for the all classes of the people.\
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