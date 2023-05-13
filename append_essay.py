
index = 35

link = "https://writing9.com/text/645ef5b196d136001a1347b0-some-companies-sponsor-sport-as-a-way-to-advertise-themselves"

topic = """\
Some companies sponsor sport as a way to advertise themselves. Some people think it is good for the world of sports, while others think there are disadvantages. Discuss both views and give your opinion\
"""

essay = """\
There are controversial perspectives heating up a debate over the sport sponsorship of corporations. While some people think that this phenomenon is disadvantageous, others hold a claim that it is advantageous for the sports world. While the former is valid to some extent, I would consider myself an advocate of the latter.

Without a shadow of a doubt, there is a wealth of tremendous benefits for the world of sports when being sponsored by leading companies, especially pieces of equipment for sports team members. With sponsorship, athletes can have enough money to pay for usual costs, which helps them decrease financial burden. For instance, Nike, one of the most famous fashion brands in the world, invested in Vietnam U23 football team in terms of shoes so they do not need to find external jobs to purchase and they can fully focus on practicing and bringing medals for Vietnam. Therefore, sponsoring sports brings about myriads of beneficial impacts for the sports world.

While the advantage of sport sponsorship is widely acknowledged, its drawbacks still linger. Some companies opt for sponsoring popular sport programmes, which have a high rate of viewers, to promote their low equality products or services. For example, Bia Saigon, a beer producing company, sponsored Leicester-city football club and attracted their fans to encourage them to use their commodities which have bad effects on people’s health. Hence, advertising can cause a myriad of demerits for the world of sports.

In my conclusion, companies’ sponsorship for the sports world is tremendously satisfactory not only for those firms but also for sports teams. However, its downsides are hard to deny.

"""




with open(f"essay_{index}.txt", "w") as f:
    f.write(f"""Topic:\n\n"{topic}"\n\nEssay:\n\n"{essay}"\n
Revised:\n\nFeedback:\n\nTask Response:\n\nCoherence and Cohesion:\n
Lexical Resource:\n\nGrammatical Range and Accuracy:\n\nScore:""")
    
with open('assets/essay_sample', 'a') as f:
    f.write(f"""\n\n
############################################################################

{index}.
Link: {link}

Topic:\n{topic}
Essay:\n{essay}
""")

