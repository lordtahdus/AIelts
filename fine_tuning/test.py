import openai
from decouple import config


openai.api_key = config('OPENAI_KEY_3')

FINE_TUNED_MODEL = "babbage:ft-personal-2023-08-07-05-53-27"

# ada:ft-personal-2023-08-07-05-45-45
# babbage:ft-personal-2023-08-07-05-53-27

YOUR_PROMPT =f"""\
Topic:

"Mobile phones have made life easier and anyone can use a mobile phone to answer or make work calls or home calls art any place 7 days a week. Do you think this development has more positive effects or negative effects on the individual and the society ?"

Essay:

"In the present world, smartphones are being used everywhere for individual purposes and also for work matters. It has been observed that they are being utilized constantly. In this article, I will talk about its drawbacks and advantages for us and also for the whole of society. 

Firstly, we should consider the fact that mobiles can help us have an easier life. Thus, it has brought many pluses. Every single individual can access the nearest and dearest whenever he wants, and it helps us to communicate simply, and be in touch with each other. For example, in the past times, it took several months to ask someone whether they are in a good condition or not. However, it has decreased to a few seconds these days. In addition, the whole nation can benefit from these items. Companies can solve their work matters 24/7 because all of the employees are accessible. Therefore, advantages are not limited to just every individual. 

On the other hand, we should not neglect the drawbacks. Technologies, including have kept us far from each other in some ways. For example, face-to-face interactions have become restricted, and we all use social media or the like to contact each other. Therefore, we have become strangers rather than friends. Moreover, using smartphones in  public can disturb others. So, this is the negative effect which we have to consider. For instance, while commuting there are a lot of people on the bus, and talking loudly in these places can harm others. 

To conclude, smartphones have brought many advantages, but we have to consider the negative aspects. It helps us to keep in touch and develops communication. On the other side, it has weakened bonds and also has some drawbacks when it is used in public."
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
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens= 1500
    )
    
    reply = response["choices"][0]["message"]["content"]
    return reply



YOUR_PROMPT += "\n\n###\n\n"

response = openai.Completion.create(
    model=FINE_TUNED_MODEL,
    prompt=YOUR_PROMPT,
    max_tokens = 1500)

with open("rewritten_vietnamese.txt", "w", encoding="utf-8") as file:
    file.write(request_ChatGPT(response))

# with open("fine_tuning/text_2.txt", "w", encoding="utf-8") as outfile:
#     outfile.write(response["choices"][0]["text"])
