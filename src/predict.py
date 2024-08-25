import joblib
import pandas as pd

# Load the model and encoder
model = joblib.load('models\scholarship_match.pkl')
encoder = joblib.load('models\encorder.pkl')

# Load scholarships data
scholarships = pd.read_csv('scholarships.csv')

# Define a new user profile
new_user_profile = {
    'academic_background': 'STEM',
    'field_of_study': 'Engineering',
    'extracurricular_activities': ['Robotics'],
    'financial_needs': 'High',
    'country': 'USA'
}

# Convert the new user profile to a DataFrame
new_user_df = pd.DataFrame([new_user_profile])

# Encode the new user profile
new_user_encoded = encoder.transform(new_user_df).toarray()

# Predict the suitability of each scholarship for the new user
predictions = model.predict(new_user_encoded)

# Get the top matching scholarships
matching_scholarships = scholarships[predictions == 1]
print("Top Matching Scholarships:")
print(matching_scholarships)