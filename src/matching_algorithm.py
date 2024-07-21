import numpy as np

def calculate_similarity(model, X_test, user_profile_vector):
    """
    Calculate similarity scores for the user profile against the test set.
    """
    # Get the probability of being a match
    probabilities = model.predict_proba(X_test)[:, 0]  # Get the probability for the single class
    user_probabilities = model.predict_proba(user_profile_vector)[:, 0]  # Get the probability for user profile
    
    # Calculate the similarity scores
    similarities = np.dot(probabilities, user_probabilities.T)
    return similarities

def get_top_matches(scholarships, similarities, top_n=5):
    """
    Get the top N matching scholarships.
    """
    scholarships['similarity'] = similarities
    top_matches = scholarships.sort_values(by='similarity', ascending=False).head(top_n)
    return top_matches