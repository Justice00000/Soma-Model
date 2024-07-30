from load_data import load_scholarships
from preprocess import preprocess_data
from matching_algorithm import calculate_similarity, get_top_matches
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

def main():
    # Load data
    scholarships = load_scholarships('data/processed_scholarships.csv')
    
    # Define user profile
    user_profile = {
        'title': 'Schaefer Halleen’s Social Equity Scholarship',
        'degrees': 'Master',
        'funds': '$1000',
        'date': '30 June 2022',
        'location': 'united-states'
    }
    
    # Preprocess data
    features, target, user_profile_vector = preprocess_data(scholarships, user_profile)
    
    # Train the model
    model = DecisionTreeClassifier(random_state=42)
    model.fit(features, target)
    
    # Make predictions
    y_pred = model.predict(features)  # Adjust as necessary
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