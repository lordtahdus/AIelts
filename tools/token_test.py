import tiktoken

# enc = tiktoken.get_encoding("cl100k_base")
enc = tiktoken.get_encoding("r50k_base")


print(enc)

assert enc.decode(enc.encode("hello world")) == "hello world"

vietnam = enc.encode("Xin chào", allowed_special="all")
print(vietnam)

vietnam = enc.encode("Xin chào")
print(vietnam)

# To get the tokeniser corresponding to a specific model in the OpenAI API:
enc = tiktoken.encoding_for_model("davinci")
# enc = tiktoken.encoding_for_model("gpt-3.5")
print(enc)