import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(user_features, scholarship_features):
    """
    Calculate cosine similarity between user profile and scholarships.
    """
    return cosine_similarity(user_features, scholarship_features)

def get_top_matches(similarity_scores, scholarships, top_n=5):
    """
    Get top N scholarship matches based on similarity scores.
    """
    top_indices = np.argsort(similarity_scores[0])[::-1][:top_n]
    return scholarships.iloc[top_indices]

# Example usage:
# similarity_scores = calculate_similarity(user_features, scholarship_features)
# top_matches = get_top_matches(similarity_scores, scholarships)