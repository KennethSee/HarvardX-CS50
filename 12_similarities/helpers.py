from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""
    ls_same = []
    a_list = a.split("\n")
    b_list = b.split("\n")
    for item in a_list:
        if item in b_list and item not in ls_same:
            ls_same.append(item)
    return ls_same

def sentences(a, b):
    """Return sentences in both a and b"""
    a_token = sent_tokenize(a)
    b_token = sent_tokenize(b)
    ls_sentence = []
    for item in a_token:
        if item in b_token and item not in ls_sentence:
            ls_sentence.append(item)
    return ls_sentence


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    substring_list = []
    
    # create list of substrings of length n in string a
    a_list = make_substring_list(a, n)
    # create list of substrings of length n in string b
    b_list = make_substring_list(b, n)
        
    # perform comparison
    for item in a_list:
        if item in b_list and item not in substring_list:
            substring_list.append(item)
            
    # return list of unique substrings that appear in both a and b
    return substring_list

def make_substring_list(s, n):
    '''
    Returns list of substrings of length n
    '''
    length_s = len(s)
    substring_list = []
    for i in range(length_s):
        if i + n - 1 < length_s:
            substring_list.append(s[i:i+n])
    return substring_list
