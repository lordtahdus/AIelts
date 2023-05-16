
index = 46

link = "https://writing9.com/text/5eafca6273403800189c0e6e"

topic = """\
Some educationalists think that a programme of international exchange visits will offer various benefits for teenage school students.
Do you think the advantages of it outweigh the disadvantages?\
"""

essay = """\
In our modern life, one of the most important aspect is education.Respectively, programme of international exchange became a popular in resent year. I am on the view that advantages of it overweight disadvantages. In this essay I will explore my ideas with reasons and examples before coming to a conclusion.

On the one hand, there some drawbacks of this programme of international exchange, especially among teenage school students. Firstly, it chance to get acquainted with new culture. In other words, this programme way to adopt different cultures and lifestyles which are not suitable for our value. Secondly, we can travel and enjoy around cities with spectacular view for free and it really helps to leave our comfort zone.

On the other hand, the mean benefit of studying abroad is improve knowledge level. I am sure that, exchange opinions with teachers and professors from different countries, absolutely help to develop our knowledge to new degree. For instance, we can learn something new, expand our outlook, recognise about their culture, traditions and history from them and teach others what we know. In addition, another important advatage is that students can make new friends and build relationships. Friends always help to relax and adapt. 

To sum up, when we analyse the issue in depth, it becomes crystal clear that programme of international exchange  has more advantages than disadvantages also it really help to students braking knowledge and start new life.\
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

