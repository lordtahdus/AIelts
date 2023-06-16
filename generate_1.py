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

    index = 130

    link = "https://writing9.com/text/60e96fab00657e00180f5f93-should-private-schools-receive-government-funding-give-reasons-for-your-answer"

    topic = """\
Should private schools receive government funding?
Give reasons for your answer, and include any relevant examples from your own knowledge or experience.\
"""

    essay = """\
Schools are an essential component for the all-around development of children; however, is it necessary for the government to invest in private schools. Even though governmental institutes need a decent amount of money to operate, I find the notion to fund private academies completely flawed since they do not charge students with high fees but they also gain sufficient profit by charging for extra-curricular activities.

Most of the government-owned schools are deficient in budget. This is because these schools are backward in terms of infrastructure which requires money for renovation, and the authorities charge very little fees from students. This in turn makes it necessary for the government to provide funds as they are unable to generate enough income and thus, it is required to keep institutes functional.

Contrarily, non-governmental institutes charge high fees for children. To elaborate more, private schools provide amenities along with surplus facilities at the cost of extra money which is willingly paid by most of the parents for the future of their kids. As evidence, there is a large difference between the fees structure of private and public schools. Had these private schools not been charged this much fee, there could be a need to provide funds. However, unnecessary money is already being paid to them.

In addition to high tuition fees, extra money is charged for various other activities in these private schools. Firstly, parents are insisted to pay admission fees to secure a seat as there are limited slots available. Secondly, students are forced to buy books and uniforms from school only which provides these schools extra profit. Furthermore, there are made to pay examination fees, welfare amounts, and much more.

To recapitulate, two main points are mentioned in this essay: reasons to provide funds to public schools, and reasons not to invest in private institutes.\
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