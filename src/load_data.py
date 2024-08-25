import pandas as pd

def load_scholarships(file_path):
    print(f"Loading scholarships from {file_path}...")
    return pd.read_csv(file_path)

def load_user_profiles(file_path):
    print(f"Loading user profiles from {file_path}...")
    return pd.read_csv(file_path)