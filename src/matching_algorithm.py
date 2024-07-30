import numpy as np

def calculate_similarity(model, X_test, user_profile_vector):
    """
    Calculate similarity scores for the user profile against the test set.
    """
    # Ensure user_profile_vector has the correct shape
    user_profile_vector = np.array(user_profile_vector).reshape(1, -1)
    
    # Check the shapes
    print("X_test shape:", X_test.shape)
    print("User profile vector shape:", user_profile_vector.shape)
    
    # Print the user profile vector to check its values
    print("User profile vector:", user_profile_vector)
    
    # Verify that user_profile_vector and X_test have the same number of features
    if X_test.shape[1] != user_profile_vector.shape[1]:
        raise ValueError("Number of features in user_profile_vector does not match X_test")

    # Get the probability of being a match
    # Make sure to use the probabilities for the positive class correctly
    probabilities = model.predict_proba(X_test)[:, 1]  # Get the probability for the positive class
    
    # Calculate the similarity scores using a metric like cosine similarity or dot product
    # Ensure X_test and user_profile_vector are correctly aligned
    similarities = np.dot(X_test, user_profile_vector.T).flatten()
    
    return similarities

def get_top_matches(scholarships, similarities, top_n=5):
    """
    Get the top N matching scholarships.
    """
    if len(similarities) != len(scholarships):
        raise ValueError("Length of similarities does not match length of scholarships DataFrame")

    scholarships['similarity'] = similarities
    top_matches = scholarships.sort_values(by='similarity', ascending=False).head(top_n)
    return top_matches