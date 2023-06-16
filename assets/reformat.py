# import required module
import os
# assign directory
directory = 'assets/band_8.5'
 
# iterate over files in
# that directory
for filename in os.listdir(directory):
    file = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(file):
        print(file)

    # read file
    with open(file, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        
        # print(lines)
        
        topic_essay_revised = lines[0: lines.index('Feedback:\n')]
        feedback = lines[lines.index('Feedback:\n'):]

        score_dict = [0,0,0,0,0]

        for index, item in enumerate(feedback):
            if "Task Response:" in item:
                score_dict[0] = float(item[14:].strip())
                feedback[index] = "Task Response:\n"

            if "Coherence and Cohesion:" in item:
                score_dict[1] = float(item[23:].strip())
                feedback[index] = "Coherence and Cohesion:\n"

            if "Lexical Resource:" in item:
                score_dict[2] = float(item[17:].strip())   
                feedback[index] = "Lexical Resource:\n"

            if "Grammatical Range and Accuracy:" in item:
                score_dict[3] = float(item[31:].strip())   
                feedback[index] = "Grammatical Range and Accuracy:\n"

            if "Score:" in item:
                if len(item) > 7:
                    score_dict[4] = float(item[7:].strip())
                else:
                    score_dict[4] = feedback[index + 1]
                # delete all the remaining items from "Score:" onwards
                for j in range(index, len(feedback)):
                    feedback.pop(-len(feedback)+index)

        print(score_dict)
        assert 0 not in score_dict, "fail to read score"

        feedback.append(
            f"""\nScore:\n\nOverall: {score_dict[4]}\n
Score_TR: {score_dict[0]}\nScore_CC: {score_dict[1]}\nScore_LR: {score_dict[2]}\nScore_GA: {score_dict[3]}\n"""
        )

        # print("".join(topic_essay_revised))
        # print("".join(feedback))

    # write file
    with open(file, 'w', encoding="utf-8") as f:
        f.write("".join(topic_essay_revised))
        f.write("".join(feedback))

