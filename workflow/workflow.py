import pandas as pd
from model.embeddings import get_embeddings
from model.similarity import calculate_similarity

def preprocess_data(data):
    data.drop_duplicates(inplace=True)
    data.fillna('N/A', inplace=True)
    return data

def run_workflow(user_profile, df):
    df = preprocess_data(df)
    df['embeddings'] = df['description'].apply(get_embeddings)
    results = calculate_similarity(user_profile, df)
    return results

if __name__ == "__main__":
    df = pd.read_csv('../data_collection/scholarships.csv')
    user_profile = {
        'name': 'Jane Doe',
        'education_level': 'Undergraduate',
        'field_of_study': 'Computer Science',
        'location': 'Kenya',
        'financial_need': 'High'
    }
    results = run_workflow(user_profile, df)
    print(results.head())