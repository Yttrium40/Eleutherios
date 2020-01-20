import string

def is_punctuation(s):
    return s in string.punctuation

def is_punctuation_with_space_after(s):
    return s in [",", ".", ";", "!", "?", ":"]

def strip_punctuation(s):
    return s.translate(str.maketrans("", "", string.punctuation))
