
index = 31

link = "https://writing9.com/text/645f66da96d136001a13488b-small-scale-shopes-are-reducing-in-recent-days-talk-about"

topic = """\
Small Scale shopes are reducing in recent days ,talk about your opinion on this.\
"""

essay = """\
In this contemporary era, the shops which run at a small level are declining at a rapid pace. I firmly opine that the basic cause of this trend is the establishment of  lavishing big stores as a way to flaunt  wealth. This put deleterious impacts on the income of small retailers and also becomes a hurdle for the public, who have the minimum capacity to spend.

To commence with, the major point of this deteriorating phenomenon which is earning level of small businessmen is going into vain. This is because the attractive hoardings of immense supermarkets influence the consumers as a consequence, no customer visits the little shops which badly affects their demand for the product. Moreover, the quality of goods  stops them to buy from small-scale shops. For instance, as per the survey conducted in America, it is believed by the majority of locals that giant malls are efficient due to the availability of distinct products such as clothes, groceries, food items, and accessories in one place. Thus, convenience is the factor leading to reduce sales in small markets.

Furthermore, another reason why people modify their choices is to show their status. This is because the big malls provide branded products which are considered quite fashionable and trendy instead of cheaper shop goods as people imitate their peers and visit the same shop which their mates do and utilize the huge amount in all things, only to maintain their sterling image which affects the portion of the community who cannot afford such expensive things.For example, a number of individuals with  credit card limits have to be suffered from losses due to overindulging towards big stores which creates an obstacle for them. Thus, small markets are the best way to purchase in large quantities at reasonable prices.

In conclusion, I think that although malls are beneficial for buying partywear clothes and things for special occasions, still small markets are helpful in various ways such as in saving income and maintaining the simple living of people.\
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

