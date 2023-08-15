import tiktoken

# enc = tiktoken.get_encoding("cl100k_base")
# enc = tiktoken.get_encoding("r50k_base")



def token_to_call(encoding, prompt, response, allow_model_token = 2046):
    ''' Returns the number of tokens required for chatgpt call'''
    
    enc = tiktoken.get_encoding(encoding)
    
    prompt_tokens = len(enc.encode(prompt)) # or we can just use fixed value
    response_tokens = len(enc.encode(response))
    
    total_tokens = allow_model_token - prompt_tokens + response_tokens
    
    return total_tokens
