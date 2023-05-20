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

    index = 49

    link = 'https://www.ieltsbuddy.com/ielts-band-5-essay-samples.html(3)'

    topic = """\
A growing number of people feel that animals should not be exploited by people and that they should have the same rights as humans, while others argue that humans must employ animals to satisfy their various needs, including uses for food and research.

Discuss both views and give your opinion.\
"""

    essay = """\
Although some people believe that humans should use animals to satify their different necessities, such as feeding and researching, the number of indivuduals that defend that animals should not be exploited as well as shoud have the same prerogatives as humankind is increasing. In my opinion, animals should recieve a better treatment and not to be abuse anymore.

In the humanity history for centuries it was common to utilize animals for lots of tasks, like transportation. Most of them worked their entire lifes without stopping, suffering abuse. The animals were domesticated just to satisfy human necessities, with which most of people agreeded at that time withou questioning.

Nevertheless, more recente studies have proved that animals have feelings, not exactly the same as the humans, but some similars emotions. Nowadays, it is not necessary anymore to use animals for jobs, for research and even for feeding. With the evolution, all of this need can be satisfied with the new technology. For instance, there are different means of transport, even eco-friendly ones, also planty of other options to substitute meat for great and nutritive substances that not involve sacrifying animals.

More than this, animals should have recognized rights to assure them a healthy and safe life, not exactly the same as humans, but laws to protect them that take in consideration their aspects. As an example in Brazil we have some recent changes in law in order to forbid the use of animals in researchs and to penalize animals abuse.

In conclusion, I strongly believe that animals should not be employ anymore to satisfy individuals needs. Furthermore, animals must have rights recognize worldwide to assecure them a better quality of life, based on the human law, observed the peculiarities.\
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