from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def cosine_sim(str1, str2):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([str1, str2])
    return cosine_similarity(tfidf[0], tfidf[1])[0][0]


def is_extremely_similar_cosine(str1, str2):
    return cosine_sim(str1, str2) > 0.8
