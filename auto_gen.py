from generate_3 import *
from scraping import *

openai.api_key = config('OPENAI_KEY_3')

messages = []
generated_content = ""
system_msg = "Ielts writing editor"
messages.append({"role": "system", "content": system_msg})

START_ID = 214

with open('essays.jsonl', 'r') as file:
    for line in file:
        data = json.loads(line)

        essay_url = data['url']
        essay_title = data['title']
        essay_content = data['content']

        link_status = check_csv('generated_links.csv' , essay_url)

        if link_status:
            continue
        else:
            with open('generated_links.csv', "a") as f:
                f.write(f"\n{absolute_url}")
            
            print(f".....Generating essay {START_ID}.....")
            
            generated_content = ''

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
                        messages=messages)
                    reply = response["choices"][0]["message"]["content"]
                    # Add generated output to do similarity check
                    generated_content += reply
                    # save general feedback in messages but not print 
                    if i == 1:
                        messages.append({"role": "assistant", "content": reply})
                    else:
                        print(reply + '\n\n', file = f)
                    
                with open(f"processed_essay/essay_{START_ID}.txt", "w") as f:
                    f.write(f"""Topic:\n\n"{topic}"\n\nEssay:\n\n"{essay}"\n\n\n""")
            
                syntaxes = [
                    f'This is IELTS writing task 2.\n\nTopic:\n"{topic}"\n\nEssay:\n"{essay}"\nPlease edit the essay according to IELTS structure',
                    f'This is IELTS writing task 2.\n\nTopic:\n"{topic}"\n\nEssay:\n"{essay}"\nPlease provide me detailed feedback in Vietnamese with clear explanations, based on four scoring criteria:\nTask Response\nCoherence and Cohesion\nLexical Resource\nGrammatical Range and Accuracy',
                    """\
Đánh giá Task Response trong bài viết của tôi một cách chi tiết hơn theo những tiêu chí sau:
Yêu cầu đề bài có được trả lời không?
Bài viết có giải thích đầy đủ tất cả các phần của nhiệm vụ không?
Ý tưởng có được mở rộng đầy đủ không?

Nếu có, liệt kê tất cả lỗi sai của Task Response theo cấu trúc sau:
Lỗi cần sửa
Ví dụ cho lỗi cải thiện
""",
                    """\
Đánh giá Coherence and Cohesion trong bài viết của tôi một cách chi tiết hơn theo những tiêu chí sau:
Bài viết của tôi có sự liên kết mạch lạc và hợp lí giữa tất cả các ý và các câu không?
Các liên kết câu có tự nhiên và logic không?

Nếu có, liệt kê tất cả lỗi sai của Coherence and Cohesion theo cấu trúc sau:
Lỗi cần sửa
Ví dụ cho lỗi cải thiện
""",
                    """\
Đánh giá Lexical Resource trong bài viết của tôi một cách chi tiết hơn theo những tiêu chí sau:
Bài viết của tôi có mắc lỗi sai về từ vựng không?
Từ vựng dùng có tự nhiên và thích hợp không?

Nếu có, liệt kê tất cả lỗi sai của Lexical Resource theo cấu trúc sau:
Lỗi cần sửa
Ví dụ cho lỗi cải thiện
""",
                    """\
Đánh giá Grammatical Range and Accuracy trong bài viết của tôi một cách chi tiết hơn theo những tiêu chí sau:
Bài viết của tôi có mắc lỗi sai về ngữ pháp không?

Nếu có, liệt kê tất cả lỗi sai của Grammatical Range and Accuracy theo cấu trúc sau:
Lỗi cần sửa
Ví dụ cho lỗi cải thiện
""",
                    "Estimate carefully the score of each criteria"
                ]
                headings = [
                    "Feedback:\n\nTask Response:\n",
                    "Coherence and Cohesion:\n",
                    "Lexical Resource:\n",
                    "Grammatical Range and Accuracy:\n",
                    "Score:\n\nOverall:\n\nScore_TR:\nScore_CC:\nScore_LR:\nScore_GA:\n"
                ]

                # Print similarity score
                og_content = topic + essay
                score = similarity_check([og_content, generated_content])
                print(score)

                with open('similar_scores.csv', "a") as f:
                    f.write(f"\nEssay {START_ID}: {score}")

                print(f'DONE ESSAY {START_ID} !!!')

                START_ID += 1
