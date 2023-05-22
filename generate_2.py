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

    index = 52

    link = 'https://writing9.com/text/6469c7b97e89e60018c7f8d1-at-present-the-population-of-some-countries-include-a-relatively'

    topic = """\
At present the population of some countries include a relatively large number of young adults, compared with the number of older people.
Do the advantages outweigh the disadvantages? Give reasons for your answer with relevant example.\
"""

    essay = """\
In recent times, some nations have a comparatively large number of young people than the number of older people. Possessing younger people than  older ones has both positive and negative sides as well. However,  positivity never outweighs the negativity. The following essay will explore the two sides and provide a plausible example. 

To start with, there is a saying that young adults are the future of any nation. The contribution of young adults in numerous sectors of the country is huge. Hence, with the help of their strength and ,fitness they easily take the leadership of any sector. For example, the economy, employment, sports and defence cannot be imagined without the performance of young people. Moreover, young people have the courage and motivation to take responsibility which cannot be done by  older people.  For example, a recent study demonstrates that, young people have 60% more stamina and courage than old people. Therefore, countries are fully dependent on the young generation more than the old ones.

Conversely, if the volume of the young generation outweighs the old ones obviously that will have some demerits. Building a nation with both younger and older people is necessary. The old people are the forerunners of  a country and the young generation always follow their footprints. For example, the old generation can easily be friends, philosophers and guides of the young generation. Furthermore, the old generation can help the young generation in learning new things and ideas and share their experiences with the younger generation. Therefore, to build a country both young and old people are required.

To conclude, although the volume of the young generation outweighs the old generation, it does not outweigh the merits of the younger generation. However, to achieve a balanced society and nation there are no alternatives for younger people.
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