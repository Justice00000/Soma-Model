from load_data import load_scholarships
from preprocess import preprocess_data
from matching_algorithm import calculate_similarity, get_top_matches
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
from scrape import scrape_scholarships  # Import the new scraping function

def main():
    # Define user profile
    user_profile = {
        'title': 'Scholarship',
        'degrees': 'Master',
        'funds': '$1000',
        'date': '2024-07-30',
        'location': 'united-states'
    }
    
    # Scrape scholarships data
    print("Scraping scholarships data...")
    scraped_scholarships = scrape_scholarships(user_profile)
    
    # If scraping fails, fallback to loading local data
    if scraped_scholarships.empty:
        print("Falling back to local data...")
        scholarships = load_scholarships('data/processed_scholarships.csv')
    else:
        scholarships = scraped_scholarships
    
    # Preprocess data
    features, target, user_profile_vector = preprocess_data(scholarships, user_profile)
    
    # Train the model
    model = DecisionTreeClassifier(random_state=42)
    model.fit(features, target)
    
    # Make predictions
    y_pred = model.predict(features)
    accuracy = accuracy_score(target, y_pred)
    print(f'Accuracy: {accuracy * 100:.2f}%')
    
    # Get top matches for the user
    similarities = calculate_similarity(model, features, user_profile_vector)
    top_matches = get_top_matches(scholarships, similarities)
    
    # Display top matches
    print("Top Scholarship Matches:")
    print(top_matches[['title', 'funds', 'location']])

if __name__ == '__main__':
    main()