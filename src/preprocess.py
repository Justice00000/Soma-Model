import pandas as pd

def preprocess_data(scholarships_df, user_profile):
    # Ensure consistent column names
    scholarships_df.columns = ['Unnamed: 0', 'title', 'degrees', 'funds', 'date', 'location', 'scholarship_id']
    
    # Drop the 'Unnamed: 0' column as it is not needed
    scholarships_df = scholarships_df.drop(columns=['Unnamed: 0'])
    
    # Encode categorical features
    features = pd.get_dummies(scholarships_df[['title', 'degrees', 'funds', 'date', 'location']])
    target = scholarships_df['scholarship_id']  # Target can be adjusted as necessary
    
    # Process user profile into a DataFrame (make sure these keys exist in user_profile)
    user_profile_df = pd.DataFrame([user_profile])
    
    # Encode user profile
    user_profile_vector = pd.get_dummies(user_profile_df).reindex(columns=features.columns, fill_value=0)
    
    return features, target, user_profile_vector