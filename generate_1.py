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

    index = 51

    link = 'https://www.ieltsbuddy.com/ielts-band-4-essay-samples.html'

    topic = """\
A growing number of people feel that animals should not be exploited by people and that they should have the same rights as humans, while others argue that humans must employ animals to satisfy their various needs, including uses for food and research.

Discuss both views and give your opinion.\
"""

    essay = """\
In this century, there are a countless number of people that are showing interest in what concerne animals rights, therefore it is becoming an actual and argued topic.

People are starting to look disapprovingly all situations and events with animal exploitation. Infact, circus for example, has lost its popularity and the audience prefer human performances.                                

Moreover, animal rights have become part of the law and animal’s abuse is punished with fees and occasionally with prison.     

Further more, also the animal breeding has been observed and people are realizing that the killing and the slaughter of animals is cruelly done. It is important to realize that people of new generations are developing a new sensibility concerning this issue, but currently it is emerging a new exstremist thought.                                                                         

Despite the huge number of vegeterian people (which the majority of them are following a new fashion), there are also people with distorted views.                                                                                                                                                                  

The area that worry me most regards the animal research which allows considerable and important improvements in the medical research, therefore in  human walfare. The animalist group are spreading wrong information , directly demaging the research sector.   As an illustration, few months ago an animalist  group destroyed years and years of neurological research freeing  rats used in a laboratory, because they would have been cruelly treated.  Unfortunately this animalists did not know that for each treatment was used anesthesia.        

Given these points, I defend animal rights and I do not support any form of animal exploitation , nevertheless I do not support any exetremist thought  especially concerning medical research.\
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