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

    index = 180

    link = "https://writing9.com/text/5e23f024be852b00187a5e5a"

    topic = """\
Traffic and housing problems in major cities could be solved by moving large companies and factories and their employees to the countryside.
To what extent do you agree or disagree with this opinion?\
"""

    essay = """\
It is common belief that there are those who protest relocation of big-size companies, factories as well as their staffs to rural areas. Yet, I firmly believe that this initiative is considered as a solution to traffic congestion and a shortage of accommodation. And this essay will address and enlist the following approaches.
To commence with, transferring sizable corporations and their workers out of inner-city, lead to alleviate the current traveling overload. Each large-scale businesses have hordes of workers who are able to be considered as the chief culprit behind the traffic jam problem, especially in the rush hours. As a consequence, the shift of big companies together with their employees to rural areas would help tackle the congested roads. Additionally, toxic waste from the means of transports is the key factor influencing pollution. Therefore, shifting the companies, factories, and employees to the suburb is able to cut down on emissions into the atmosphere through the acts of lowering the extent of vehicles circulating on the streets.
On top of that, it firms as together with factories transfer to the suburban area in order to relieve the pressure on urban housing supply systems. According to the recent survey, that workers have the propensity for opting for their accommodation near their works, giving rise to the apartment demand as well as the living cost. Consequently, if there has a tremendous shift in accommodation to the suburban area, city houses and apartments price will fall and be more reasonable with city dwellers.
In conclusion, by relocating workers to rural areas to work and reside, heavy traffic conditions and shortage of accommodation in city centers could be handled. From my perspective, I am certain that the aforementioned solutions will solve the problem effectively.\
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