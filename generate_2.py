import openai
from decouple import config

openai.api_key = config('OPENAI_KEY_2')

messages = []
system_msg = "Ielts writing editor"
messages.append({"role": "system", "content": system_msg})



index = 40

link = "https://writing9.com/text/5eafca6273403800189c0e6e"

topic = """\
Children are facing more pressure nowadays from academic social and commercial perspective.What are the causes of these pressures and what measures should be taken to refuse these pressures?\
"""

essay = """\
It is common to say that in these days children come across with pressures like educational communal and commercial.This essay intends to discuss how to solve problems which is disturbing most children nowadays

In their life every child will face with academic difficulties.Todays children compete with children which is from global village instead of their neighbors or from other town children.Parents want their children to be perfect in each area.So most of them send their children to special schools which have  school bags even heavier than child himself.There are tutions after school times.Because of them kids can not get enough time to try other fields

Most countries children especially teens pressurized by pressures like social and commercial.They do not want to involve traditional things so most of the time they are against from their parents opinions.This kind of things lead more and more stress.And there are problems with their peers.That is good if they are kind and smart but if they are bully they will destroy our children's life.Because they see many children like them have modern technology like computers and mobile phones.Then they also want to get it.But you know not every family have good financial positioning that some of them can not get what their kids want.Therefore most of them put themselves into depression If they can not buy these things.

Children should not let these kind of challenges to destroy their innocent childhood.Every child in the world deserve the best things.We should help them find themselves in any way.Or else these pressures will demolish their physical and mental growth.\
"""

# create new text file
with open(f"essay_{index}.txt", "w") as f:
    f.write(f"""Topic:\n\n"{topic}"\n\nEssay:\n\n"{essay}"\n\n""")

with open('assets/essay_sample', 'a') as f:
    f.write(f"""\n\n
############################################################################

{index}.
Link: {link}

Topic:\n{topic}
Essay:\n{essay}
""")
 
syntaxes = [
    f'This is IELTS writing task 2.\n\nTopic:\n"{topic}"\n\nEssay:\n"{essay}"\nPlease edit the essay according to IELTS structure. Also, estimate the score.',
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
    "Score:\n"
]

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
    run()