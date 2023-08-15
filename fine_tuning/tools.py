import tiktoken
import openai
from decouple import config
import os

openai.api_key = config('OPENAI_KEY_1')

# enc = tiktoken.get_encoding("cl100k_base")
# enc = tiktoken.get_encoding("r50k_base")



def token_to_call(encoding, prompt, response, allow_model_token = 2046):
    ''' Returns the number of tokens required for chatgpt call'''
    
    enc = tiktoken.get_encoding(encoding)
    
    prompt_tokens = len(enc.encode(prompt)) # or we can just use fixed value
    response_tokens = len(enc.encode(response))
    
    total_tokens = allow_model_token - (prompt_tokens + response_tokens)
    
    return total_tokens


def request_ChatGPT(response):
    prompt = "Please rewrite this in Vietnamese: " + response #TODO: change the prompt

    response = openai.Completion.create(
        model="gpt-3.5-turbo",  
        prompt=prompt,
    )
    
    reply = response["choices"][0]["message"]["content"]
    
    print(reply)
    
    # if os.path.exists("fine_tuning/last_used_index.txt"):
    #     with open("last_used_index.txt", "r") as index_file:
    #         last_used_index = int(index_file.read())
 
    # else:
    #     last_used_index = 1
   
    # filename = f"fine_tuning/rewritten_vietnamese{last_used_index + 1}.txt"


    # with open(filename, "w", encoding="utf-8") as file:
    #     file.write(reply)

    #     # Update the last used index
    # last_used_index = last_used_index + 1

    # with open("fine_tuning/last_used_index.txt", "w") as index_file:
    #     index_file.write(str(last_used_index))
        
    # print("Updated index!")