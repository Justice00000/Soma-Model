from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from embeddings import get_embeddings

def calculate_similarity(user_profile, df):
    user_profile_text = " ".join(user_profile.values())
    user_embedding = get_embeddings(user_profile_text)
    similarities = cosine_similarity([user_embedding], df['embeddings'].tolist())
    df['similarity_score'] = similarities[0]
    return df.sort_values(by='similarity_score', ascending=False)

if __name__ == "__main__":
    df = pd.read_pickle('scholarships_with_embeddings.pkl')
    user_profile = {
        'name': 'Jane Doe',
        'education_level': 'Undergraduate',
        'field_of_study': 'Computer Science',
        'location': 'Kenya',
        'financial_need': 'High'
    }
    results = calculate_similarity(user_profile, df)
    print(results.head())