from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""
    # split when "next line" is observed. Then set() to remove duplicates
    asplit = a.split("\n")
    bsplit = b.split("\n")
    asplit = set(asplit)
    bsplit = set(bsplit)


    return asplit & bsplit


def sentences(a, b):
    """Return sentences in both a and b"""

    asplit = set(sent_tokenize(a))
    bsplit = set(sent_tokenize(b))


    return asplit & bsplit


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    a_list = a.split()
    b_list = b.split()
    # a's substring and b's substring
    asub = []
    bsub = []


    for word in a_list:
        for i in range(len(word)+1-n):
            asub.append(word[i:n+i])
    for word in b_list:
        for i in range(len(word)+1-n):
            bsub.append(word[i:n+i])

    asub = set(asub)
    bsub = set(bsub)

    return asub & bsub
