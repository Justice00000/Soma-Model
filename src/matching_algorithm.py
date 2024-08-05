import numpy as np

def calculate_similarity(model, features, user_profile_vector):
    # Assuming you need to calculate the similarity score for each feature
    # by predicting probabilities for each feature
    probabilities = model.predict_proba(user_profile_vector)
    similarities = probabilities.flatten()  # Flatten to get the 1D array of probabilities

    # If you need to compute similarity with multiple entries
    if features.shape[0] != len(similarities):
        raise ValueError(f"Length of similarities {len(similarities)} does not match number of entries in features {features.shape[0]}")

    return similarities


def get_top_matches(scholarships_df, similarities):
    if len(similarities) != len(scholarships_df):
        raise ValueError("Length of similarities does not match length of scholarships DataFrame")

    scholarships_df['similarity'] = similarities
    top_matches = scholarships_df.sort_values(by='similarity', ascending=False).head(10)
    
    return top_matches