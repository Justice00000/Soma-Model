import pandas as pd
from sklearn.preprocessing import OneHotEncoder

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
    
    # Ensure the fields in the scholarships data match those in the user profile
    scholarships['financial_needs'] = scholarships['eligibility_criteria'].apply(lambda x: 'High' if 'STEM' in x else 'Low')
    scholarships['field_of_study'] = scholarships['eligibility_criteria']
    scholarships['extracurricular_activities'] = scholarships['eligibility_criteria']
    
    # One-hot encode categorical features
    encoder = OneHotEncoder(handle_unknown='ignore')
    scholarship_features = encoder.fit_transform(scholarships[['eligibility_criteria', 'country', 'field_of_study', 'financial_needs', 'extracurricular_activities']]).toarray()
    user_features = encoder.transform(pd.DataFrame([user_profile_aligned])).toarray()
    
    return scholarship_features, user_features

# Example usage:
# scholarships, user_profile = preprocess_data(scholarships, user_profile)