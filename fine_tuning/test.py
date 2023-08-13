import openai
from decouple import config
import os

openai.api_key = config('OPENAI_KEY_3')

FINE_TUNED_MODEL = "babbage:ft-personal-2023-08-07-05-53-27"

# ada:ft-personal-2023-08-07-05-45-45
# babbage:ft-personal-2023-08-07-05-53-27

YOUR_PROMPT =f"""\
Topic:

"Some people say that the main environmental problem of our time is that loss of particular species of plants and animals. Others say that there are more important environmental problems.

Discuss both these views and give your own opinion.

Give reasons for your answer and include any relevant examples from your own knowledge or experience."

Essay:

"Some argued that the critical environmental consequence during our current era is the extinction of species of creatures, while others argued that it is not the only problem that we have to deal with. The following paragraphs will discuss both points of view.

 On the one hand, we could not deny the fact that there are more and more fauna and flora that disappear in the modern day. Initially, the hunting of hunters aims at some rare ingredients, for instance, the horns of the rhinos are believed to be fairy medicine, or they can be luxury decorations in some wealthy families. In addition, the population of this animal has a significant decrease during the 19th century and is nearly extinct nowadays. Moreover, biological weapons are a factor in the death of many kinds of animals and plants, which make the world less diverse in the ecosystem.

On the one hand, there are more important nature issues that directly affect to the human-being. First and foremost, climate change makes the earth hotter and hotter over time. This can lead to many different effects, a case in point is the ice melting in the Antarctic and the Arctic, as a result, many cities and lands are forecast to be drowned under the seawater next decade, furthermore, by increasing the temperature, many forests are burning which lead to the lack of oxygen. Moreover, due to the waste of carbon dioxide passing the limit, the ozone layer is getting more and more damage, which is the cause of many skin diseases.

In conclusion, I do believe that the loss of animals and plants is one of the environmental problems, however, there are many more issues that we have to cope with, such as climate change and the dramatically increasing in carbon dioxide that discharge into the environment."
"""

# YOUR_PROMPT =f"""\
#  Task Response:

# Trong bài viết của bạn, bạn đã trả lời đúng câu hỏi đề bài và văn phùng tổng quan rõ ràng. Bạn đã nêu ra cả một lợi ích cho xã hội và cá nhân, bao gồm việc làm cho cuộc sống cụ thể và phát triển mạng xã hội. Tuy nhiên, trong bài viết của bạn, bạn không đưa ra suy nghĩ của mình về những ảnh hưởng cụ thể của việc sử dụng điện tử để di động máy tính.

# Để cải thiện điểm này, bạn nên thể hiện suy nghĩ của mình một cách rõ ràng và minh bạch hơn. Bạn có thể đề cập đến những ảnh hưởng cụ thể và ý tưởng không rõ ràng của việc làm cho cuộc sống cụ thể và phát triển mạng xã hội ở dưới đây:

# 1. Ý tưởng của một số tổ chức bảo tồn điện thoại di động: Trong bài viết của bạn, bạn đã nêu ra việc một số người dùng đều có thể sử dụng điện thoại di động để cung cấp thông tin và giá trị của mình. Tuy nhiên, bạn chưa đưa ra các ý kiến ​​và luận điểm cụ thể để tăng tính thuyết phục của bài viết. Bạn có thể cung cấp thêm thông tin và ví dụ cụ thể để minh chứng cho suy nghĩ của mình.

# 2. Ý tưởng của người bán điện tử: Trong bài viết của bạn, bạn nêu ra ý kiến ​​về việc sử dụng điện tử trong việc hợp nhận và giao hướng thành công trong khóa viết. Tuy nhiên, bạn không đề cập đến các ảnh hưởng khác và tác động tiêu cực của việc sử dụng điện tử trong khóa viết của người càng lớn. Hãy cung cấp thêm thông tin và ví dụ để giải thích cách việc này sẽ làm giảm nguồn thông tin của xứng đáng với người dùng.

# Tổng quan, bạn cần phát triển và so sánh ý kiến ​​của mình về những ảnh hưởng của việc sử dụng điện tử trong xã hội và phát triển mạng xã hội. ENDNOTE và Đoạt được qua được các luận điểm của b
# """


def request_ChatGPT(messages):
    prompt = "Please rewrite this in Vietnamese: " + messages 

    response = openai.Completion.create(
        model="gpt-3.5-turbo",  
        prompt=prompt,
        max_tokens=1500, 
    )
    
    reply = response["choices"][0]["message"]["content"]
    
    
    if os.path.exists("fine_tuning/last_used_index.txt"):
        with open("last_used_index.txt", "r") as index_file:
            last_used_index = int(index_file.read())
 
    else:
        last_used_index = 1
   
    filename = f"fine_tuning/rewritten_vietnamese{last_used_index + 1}.txt"


    with open(filename, "w", encoding="utf-8") as file:
        file.write(reply)

        # Update the last used index
    last_used_index = last_used_index + 1


    print(f"Rewritten Vietnamese version saved to '{filename}'")


    with open("fine_tuning/last_used_index.txt", "w") as index_file:
        index_file.write(str(last_used_index))
        
    print("Updated index!")
    

YOUR_PROMPT += "\n\n###\n\n"

response = openai.Completion.create(
    model=FINE_TUNED_MODEL,
    prompt=YOUR_PROMPT,
    stop = " END",
    max_tokens = 1600
)

request_ChatGPT(response)

print(response)

with open("fine_tuning/text_1.txt", "w", encoding="utf-8") as outfile:
    outfile.write(response["choices"][0]["text"])
