# import required module
import os
import openai
from decouple import config

openai.api_key = config('OPENAI_KEY_3')


headings = [
    "Feedback:\n\nTask Response:\n",
    "Coherence and Cohesion:\n",
    "Lexical Resource:\n",
    "Grammatical Range and Accuracy:\n",
    "Score:\n\nOverall:\n\nScore_TR:\nScore_CC:\nScore_LR:\nScore_GA:\n"
]


def get_essay(text_file_path):
    with open(text_file_path, "r") as file:
        content = file.read()

    topic_end_id = content.find("Essay:\n")
    topic = content[len("Topic:") : topic_end_id].replace('"', '').strip()

    essay_end_id = content.find("Revised:\n")
    essay = content[topic_end_id + len("Essay:") : essay_end_id].replace('"', '').strip()

    return topic, essay


if __name__ == "__main__":
    
    for file_name in os.listdir("temp"):
        if os.path.isfile(os.path.join("temp", file_name)):

            text_file_path = os.path.join("temp", file_name)

            essay_title, essay_content = get_essay(text_file_path)
            essay_id = file_name[(file_name.index('_') + 1) : file_name.index('.')]

            print(f".....Generating essay {essay_id}.....")
            
            with open(f"doc/processed_essay/essay_{essay_id}.txt", "w") as f:
                    f.write(f"""Topic:\n\n"{essay_title}"\n\nEssay:\n\n"{essay_content}"\n\n\n""")

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

Nêu ra những điểm cần được cải thiện, cách cải thiện, và đồng thời ví dụ cho cách cải thiện.
""",
# Nêu ra những điểm cần được cải thiện, những điểm đó nằm ở đâu trong bài viết, và giải thích.
# Nếu không, liệt kê tất cả lỗi sai của Coherence and Cohesion và giải thích.
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

            
            with open(f"doc/processed_essay/essay_{essay_id}.txt", "a", encoding="utf-8") as f:
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

                    # Save general feedback in messages but not print 
                    if i == 1:
                        messages.append({"role": "assistant", "content": reply})
                    else:
                        print(reply + '\n\n', file = f)

                print(f'DONE ESSAY {essay_id} !!!')

                os.remove(text_file_path)
