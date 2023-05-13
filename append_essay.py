
index = 26

link = ""

topic = """

"""

essay = """

"""




with open(f"essay_{index}.txt", "w") as f:
    f.write(f"""Topic:\n{topic}\nEssay:\n{essay}
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

