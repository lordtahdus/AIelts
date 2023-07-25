import openai
from decouple import config
from similarity_check import *
from link_check import *
import json


openai.api_key = config('OPENAI_KEY_3')

generated_content = ""

START_ID = 214

headings = [
    "Feedback:\n\nTask Response:\n",
    "Coherence and Cohesion:\n",
    "Lexical Resource:\n",
    "Grammatical Range and Accuracy:\n",
    "Score:\n\nOverall:\n\nScore_TR:\nScore_CC:\nScore_LR:\nScore_GA:\n"
]

with open('essays.jsonl', 'r') as file:
    for line in file:
        data = json.loads(line)

        essay_url = data['url']
        essay_title = data['title']
        essay_content = data['content']

        link_status = check_csv('generated_links.csv' , essay_url)

        if link_status:
            START_ID += 1
            continue
        else:
            print(f".....Generating essay {START_ID}.....")
            
            with open(f"processed_essay/essay_{START_ID}.txt", "w") as f:
                    f.write(f"""Topic:\n\n"{essay_title}"\n\nEssay:\n\n"{essay_content}"\n\n\n""")
            
            generated_content = ''

            syntaxes = [
                f'This is IELTS writing task 2.\n\nTopic:\n"{essay_title}"\n\nEssay:\n"{essay_content}"\nPlease edit the essay according to IELTS structure',
                f'This is IELTS writing task 2.\n\nTopic:\n"{essay_title}"\n\nEssay:\n"{essay_content}"\nPlease provide me detailed feedback in Vietnamese with clear explanations, based on four scoring criteria:\nTask Response\nCoherence and Cohesion\nLexical Resource\nGrammatical Range and Accuracy',
                """\
Đánh giá Task Response trong bài viết của tôi một cách chi tiết hơn.\
Bài viết của tôi có trả lời đúng câu hỏi đề bài không?\
Ý tưởng có được mở rộng đầy đủ không?
Nêu ra những điểm cần được cải thiện và giải thich.
""",
                """\
Đánh giá Coherence and Cohesion trong bài viết của tôi một cách chi tiết hơn.\
Bài viết của tôi có sự liên kết mạch lạc và hợp lí giữa tất cả các luận điểm và lập luận không?\
Các câu được liên kết chặt chẽ và nối tiếp với nhau không?

Nếu không, liệt kê tất cả lỗi sai của Coherence and Cohesion và giải thích.
""",
                """\
Đánh giá Lexical Resource trong bài viết của tôi một cách chi tiết hơn.\
Bài viết của tôi có mắc lỗi sai về từ vựng không? Những từ, cụm từ dùng có hợp ngữ cảnh không?

Nếu có, liệt kê tất cả lỗi sai và giải thích.
""",
                """\
Đánh giá Grammatical Range and Accuracy trong bài viết của tôi một cách chi tiết hơn.
Bài viết của tôi có mắc lỗi sai về ngữ pháp không?

Nếu có, liệt kê tất cả lỗi sai và giải thích.
""",
                "Estimate carefully the score of each criteria"
            ]

            #reset to
            messages = []
            system_msg = "Ielts writing editor"
            messages.append({"role": "system", "content": system_msg})
            
            with open(f"processed_essay/essay_{START_ID}.txt", "a", encoding="utf-8") as f:
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
                        messages=messages,
                        max_tokens=1000
                    )
                    reply = response["choices"][0]["message"]["content"]

                    # Add generated output to do similarity check
                    # generated_content += reply

                    # Save general feedback in messages but not print 
                    if i == 1:
                        messages.append({"role": "assistant", "content": reply})
                    else:
                        print(reply + '\n\n', file = f)

                # Print similarity score
                # og_content = essay_title + essay_content
                # score = similarity_check([og_content, generated_content])
                # print(score)

                # with open('similar_scores.csv', "a") as f:
                #     f.write(f"\nEssay {START_ID}: {score}")

                print(f'DONE ESSAY {START_ID} !!!')

                # Append link when done
                with open('generated_links.csv', "a") as f:
                    f.write(f"\n{essay_url}")
                    
                START_ID += 1
