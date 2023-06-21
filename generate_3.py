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
    index = 201

    link = "https://writing9.com/text/6492c006fd0ea70018199e2c-q-some-people-believe-that-eventually-all-jobs-will"

    topic = """\
SOME PEOPLE BELIEVE THAT EVENTUALLY ALL JOBS WILL BE DONE BY ARTIFICIALLY INTELLIGENT ROBOTS. WHAT IS YOUR OPINION?\
"""

    essay = """\
These days with the advent of new technologies such as AI, a lot of people have lost their businesses and have been replaced by them. Someone may say that this process will continue, resulting in the loose of all the jobs. While others say that there are professions that only living humans can do. I agree with the latter opinion and process this view in this essay.
Most importantly, professions dealing with feelings are difficult to be managed by AI. It is a privilege for human beings to be moved, shocked or angry and needless to say, those emotions can not be understood by artificially made things. For example, jobs such as mental counsellors can not be replaced. This is because there are no patterns or concrete solutions that can be applied to a mental problem. Problems regarding sentiments are always different and so the solutions are uncountable like stars. It is impossible for AI to deal with it using a pattern programmed previously. 
On the other hand, someone may say that if we give all the accumulated information about a job, AI will be able to run the work. I agree to some extent but the more jobs AI steals, the more works people will nurture. AI is special in that it can use effectively all the past information. However, it is unable to make new things because it lacks creativity. Therefore, only humans are able to make innovations and innovative jobs can not be replaced by humans. 
In conclusion, AI will never replace all jobs because it can not understand feelings and give birth to innovations.
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
            "Đánh giá Lexical Resource trong bài viết của tôi một cách chi tiết hơn. Bài viết của tôi có mắc lỗi sai về từ vựng không? Nếu có, liệt kê tất cả lỗi sai.",
            "Đánh giá Grammatical Range and Accuracy trong bài viết của tôi một cách chi tiết hơn. Bài viết của tôi có mắc lỗi sai về ngữ pháp không? Nếu có, liệt kê lỗi sai tất cả lỗi sai.",
            "Estimate carefully the score of each criteria"
        ]
        headings = [
            "Feedback:\n\nTask Response:\n",
            "Coherence and Cohesion:\n",
            "Lexical Resource:\n",
            "Grammatical Range and Accuracy:\n",
            "Score:\n\nOverall:\n\nScore_TR:\nScore_CC:\nScore_LR:\nScore_GA:\n"
        ]
        
        print(".....Generating.....")

        run()

        # append the link in the links.csv
        with open('links.csv', "a") as f:
            f.write(f"\n{link}")

        print('DONE !!!')