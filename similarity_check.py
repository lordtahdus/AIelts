from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def similarity_check(documents: list):
    # Build the TF-IDF matrix
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Calculate cosine similarity
    cosine_similarities = cosine_similarity(tfidf_matrix)

    # Calculate the similarity scores
    similarity_score = round(cosine_similarities[0, 1], 3)
    return (f"Similarity score: {similarity_score}")
