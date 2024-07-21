import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

def preprocess_data(scholarships, user_profile):
    """
    Preprocess scholarships and user profile data.
    """
    # Align the user profile fields with the scholarship data fields
    user_profile_aligned = {
        'eligibility_criteria': user_profile['academic_background'],
        'country': user_profile['country'],
        'field_of_study': user_profile['field_of_study'],
        'financial_needs': user_profile['financial_needs'],
        'extracurricular_activities': ', '.join(user_profile['extracurricular_activities'])
    }

    scholarships['financial_needs'] = scholarships['eligibility_criteria'].apply(lambda x: 'High' if 'STEM' in x else 'Low')
    scholarships['field_of_study'] = scholarships['eligibility_criteria']
    scholarships['extracurricular_activities'] = scholarships['eligibility_criteria']

    # Create a 'match' column for testing purposes if it doesn't exist
    if 'match' not in scholarships.columns:
        scholarships['match'] = 0  # Default to 0 for all

    encoder = OneHotEncoder(handle_unknown='ignore')
    X = encoder.fit_transform(scholarships[['eligibility_criteria', 'country', 'field_of_study', 'financial_needs', 'extracurricular_activities']])
    y = scholarships['match']

    return train_test_split(X, y, test_size=0.2, random_state=42)