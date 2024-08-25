import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_embeddings(text):
    response = openai.Embedding.create(input=text, model='text-embedding-ada-002')
    return response['data'][0]['embedding']

if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv('data_collection/scholarships.csv')
    df['embeddings'] = df['description'].apply(get_embeddings)
    df.to_pickle('scholarships_with_embeddings.pkl')