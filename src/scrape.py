import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_scholarships(user_profile):
    base_url = "https://chatgpt.com/scholarships"
    query = {
        'title': user_profile['title'],
        'degrees': user_profile['degrees'],
        'funds': user_profile['funds'],
        'date': user_profile['date'],
        'location': user_profile['location']
    }
    response = requests.get(base_url, params=query)
    
    if response.status_code != 200:
        print("Failed to retrieve data")
        return pd.DataFrame()  # Return an empty DataFrame on failure
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    scholarships = []
    for item in soup.select('.scholarship-item'):
        title = item.select_one('.title').text.strip()
        degrees = item.select_one('.degrees').text.strip()
        funds = item.select_one('.funds').text.strip()
        date = item.select_one('.date').text.strip()
        location = item.select_one('.location').text.strip()
        
        scholarships.append({
            'title': title,
            'degrees': degrees,
            'funds': funds,
            'date': date,
            'location': location
        })
    
    return pd.DataFrame(scholarships)

# Note: Replace the selectors ('.scholarship-item', '.title', etc.) with actual selectors from the target website.

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