import re
from nltk.tokenize import TweetTokenizer

tokenizer = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=True)
urls = r'(?:https?\://t.co/[\w]+)'

def tokenize(text, only_alpha=True, remove_hashtags=True):
    tokens = tokenizer.tokenize(text)

    if only_alpha:
        tokens = [tk for tk in tokens if tk.isalpha()]
    else:
        tokens = [tk for tk in tokens if tk[0] != "#"] if remove_hashtags else tokens
        tokens = [tk for tk in tokens if not re.match(urls, tk)]
    return tokens
