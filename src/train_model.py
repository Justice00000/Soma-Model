import pandas as pd

# Load the datasets
user_profiles = pd.read_csv('data/user_profiles.csv')
scholarships = pd.read_csv('data/new_scholarships.csv')
labels = pd.read_csv('data/labels.csv')

# Convert columns to the same type (string)
user_profiles['user_id'] = user_profiles['user_id'].astype(str)
labels['user_id'] = labels['user_id'].astype(str)

# If there is a scholarship_id in the labels DataFrame, also ensure type consistency
if 'scholarship_id' in labels.columns:
    user_profiles['scholarship_id'] = user_profiles['scholarship_id'].astype(str)
    labels['scholarship_id'] = labels['scholarship_id'].astype(str)

# Merge the DataFrames
data = labels.merge(user_profiles, on='user_id', how='left')
data = data.merge(scholarships, on='scholarship_id', how='left')

# Print merged DataFrame preview
print("Merged DataFrame preview:")
print(data.head())