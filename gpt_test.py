import openai
import os


openai.api_key = ""





directory = 'processed_essay'
 
# iterate over files in
# that directory
for filename in os.listdir(directory):
    file = os.path.join(directory, filename)
    essay_num = (file[-6:-4])
    # reset messages
    messages = []
    system_msg = "Ielts writing editor"
    messages.append({"role": "system", "content": system_msg})

    print(file)

    # with open(file, 'r', encoding="utf-8") as f:
    #     lines = f.readlines()
    #     # print(''.join(f.readlines()))

    #     sep_index = lines.index('Essay:\n', 2, 10)
    #     topic = lines[1:sep_index]
    #     essay = lines[sep_index + 1:]

    #     print(topic)
    #     print(essay)

    #     syntax = []
    #     syntax 

    #     # i = 0
    #     # while i <= 7:
    #     #     message
             


def run():
    # while input != "quit()":
        message = f"""
"""
        messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})

        with open("output.csv", "a", encoding="utf-8") as f:
            print(reply, file = f)

# if __name__ == "__main__":
#     run()