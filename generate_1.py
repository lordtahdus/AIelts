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

    index = 155

    link = "https://writing9.com/text/5de0b65adb52040018c1232b"

    topic = """\
Describe an interesting conversation you had with other people.\
"""

    essay = """\
I have to admit that I’m not much of a social person – I mean, I am quite shy and inhibited, so most of the time I tend to avoid talking to strangers. But I do remember a time when I had to talk to a complete stranger, and as I remember it was around 5 years ago, on my very first trip to Ho Chi Minh City. It was just a short conversation, but I can still remember it quite well.

I was a 20-year-old freshman back then, and I was unable to navigate my way to the HCMC University of Education where I was about to start studying. Back then Google Map’s wasn’t as popular as it is nowadays, so the only way I could figure out the way was by asking a local. So after hours of wandering around, I finally resorted to asking a lady who was selling noodles at a food cart near where I was standing. I asked the lady if she would be so kind to tell me the way to the HCMC University of Education and she kindly replied by pointing to the big building across the road and saying ’it’s over there’.

The university was being renovated back then, so I was unable to recognise it, but before I went off to study I decided to sit down and order some noodles from the old lady and have a chat with her. It turns out that she was also from Ninh Thuan, which is my hometown. So we ended up chatting for ages about our lives and about how and why we had come to HCMC.

You know, I think I found this conversation so interesting simply because I found Mrs Kim to be such a nice lady.  As the conversation went on and I got to know her better I realized that she had had quite a tough life, yet she had managed to maintain such a sweet and gentle personality that many other women who have been through similar struggles to her would have lost by now.\
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