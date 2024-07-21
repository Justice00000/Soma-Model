import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

def preprocess_data(scholarships, user_profile):
    """
    Preprocess scholarships and user profile data.
    """
    # Combine relevant fields into a single text field for scholarships
    scholarships['combined'] = scholarships['Title'] + ' ' + scholarships['About']
    
    # Create a text field for user profile
    user_profile_text = f"{user_profile['academic_background']} {user_profile['field_of_study']} {' '.join(user_profile['extracurricular_activities'])} {user_profile['financial_needs']} {user_profile['country']}"
    
    # Vectorize the text fields using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(scholarships['combined'])
    user_vector = vectorizer.transform([user_profile_text])
    
    # Create a target column (this should be derived from your actual data, here we assume all are a match for simplicity)
    scholarships['match'] = 1  # In a real scenario, you need a column indicating if a scholarship is a match or not
    
    y = scholarships['match']  # Replace with actual target column if available
    
    return train_test_split(X, y, test_size=0.2, random_state=42), user_vector

# Example usage:
# scholarships, user_profile = preprocess_data(scholarships, user_profile)