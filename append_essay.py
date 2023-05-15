
index = 39

link = ""

topic = """\
Forests produce fresh oxygen and participate in regulating climate. But every year tree cover of our planet is lessening due to deforestation.
What are the primary causes of deforestation? 
To what results may it lead?\
"""

essay = """\
As deforestation frequently occurs in many regions around the globe, it poses terrible threats to human survival. This essay will first prove deforestation resulting from human beings and climate change and later admit hotter climate and soil erosion as possible consequences.
To begin with, the primary reason for deforestation is human activities to fulfill the demands. It is a universal consensus that in order to solve the shortage of accommodation, many regions are cutting multitude numbers of trees for land to construct or for city expansion. Also, large-scale deforestation for woods is regarded as one of the most harmful activities people have done to the environment. In addition, it is hard to deny that wildfire due to climate change can reduce a large proportion of trees on Earth. Recently, a drought last for 2 years caused a tremendous bushfire season in Australia between 2019 and 2020, which makes governors declare a state of emergency.
On the other hand, the negative effects of deforestation will be a hotter climate and soil erosion. First of all, jungles play an essential role in regulating the air. Tree leaves convert carbon dioxide into oxygen, which means if trees get chopped down, the CO2 released by factories and cars will increase in amount. Therefore, the overall temperature can rise due to deforestation. Secondly, it is proven that when trees do not cover the land, the soil will be eroded rapidly. Conspicuously, poor soil, which plants hardly grow on, may become a wasteland in no time.
In conclusion, the reason why trees cover the planet is lessening is people deforest for land and for wood and long-term drought. Such events will lead to global warming and soil wearing away, which can bring many species to the verge of extinction.\
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

