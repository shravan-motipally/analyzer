from fuzzywuzzy import fuzz


def get_similarity_ratio(str1, str2):
    return fuzz.ratio(str1, str2)


def is_extremely_similar(str1, str2):
    return fuzz.ratio(str1, str2) > 80
