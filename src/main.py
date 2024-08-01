import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from preprocess import preprocess_data
from matching_algorithm import calculate_similarity, get_top_matches
from scrape import scrape_scholarships

def main():
    user_profile = {
        'academic_background': 'Computer Science',
        'field_of_study': 'Software Engineering',
        'extracurricular_activities': 'AI research',
        'financial_needs': 'High',
        'country': 'Kenya'
    }

    try:
        print("Scraping scholarships data...")
        scholarships_df = scrape_scholarships(user_profile)
        if scholarships_df.empty:
            raise ValueError("No data scraped, falling back to local data...")
    except Exception as e:
        print(e)
        print("Falling back to local data...")
        scholarships_df = pd.read_csv('data/processed_scholarships.csv')

    features, target, user_profile_vector = preprocess_data(scholarships_df, user_profile)

    # Define and fit the model
    model = RandomForestClassifier()
    model.fit(features, target)
    accuracy = model.score(features, target)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")

    similarities = calculate_similarity(model, features, user_profile_vector)
    top_matches = get_top_matches(scholarships_df, similarities)
    print("Top Scholarship Matches:")
    print(top_matches[['title', 'funds', 'location']])

if __name__ == "__main__":
    main()