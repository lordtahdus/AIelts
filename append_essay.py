
index = 37

link = "https://writing9.com/text/5e3917597a139900116abdd7"

topic = """\
 Stress-related illnesses are becoming increasingly common. 
-What do you think are the causes of this?
- What solution can you suggest?\
"""

essay = """\
People are increasingly suffering from sickness as a result of stress. This essay will discuss the main causes of stress-related sickness including longer working hour and increased job pressure. This essay will also suggest solutions to these problems including improvement one’s work life balance diet.
People place themselves under these unfavorable conditions because the workforce is a competitive domain For example, some people aspire to climb the corporate ladder to gain status and a high paying job. This often results in mental and physical suffering because they have to work overtime and take on additional roles which can be stressful. Some people believe that eventually jobs will be by artificially intelligent robots.
Monitoring a good work-life balance and improving one’s diet are both critical to mitigating stress related illnesses. People need to realize that if they live only for work they will suffer either mentally or physically and a poor diet will further exacerbate these issues. For example, many employees burn out from working too much and neglecting family, friends, exercise and hobbies as well as the foods they eat. Therefore, in order to reduce work one must include a better ration of work, rest, recreation and dietary sustenance. 
In conclusion, in today’s fast paced world more and more people are becoming ill as a result of stress. This essay discussed how stress is often caused by long working hours and intense workplace pressure. Thus essay also suggested that the solutions to this problem are twofold: to manage a better work-life balance and to eat a healthier diet.
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

