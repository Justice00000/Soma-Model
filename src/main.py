from load_data import load_scholarships
from preprocess import preprocess_data
from matching_algorithm import calculate_similarity, get_top_matches
from database import save_to_sql, save_to_mongo

def main():
    # Load data
    scholarships = load_scholarships('data/scholarships.csv')
    
    # Define user profile
    user_profile = {
        'academic_background': 'STEM',
        'field_of_study': 'Engineering',
        'extracurricular_activities': ['Robotics'],
        'financial_needs': 'High',
        'country': 'USA'
    }
    
    # Preprocess data
    scholarship_features, user_features = preprocess_data(scholarships, user_profile)
    
    # Calculate similarity
    similarity_scores = calculate_similarity(user_features, scholarship_features)
    
    # Get top matches
    top_matches = get_top_matches(similarity_scores, scholarships)
    
    # Print top matches
    print("Top Scholarship Matches:")
    print(top_matches)

    # Optionally save to database
    # save_to_sql(scholarships, 'mysql://username:password@localhost/scholarships_db', 'scholarships')
    # save_to_mongo(scholarships, 'mongodb://localhost:27017/', 'scholarships_db', 'scholarships')

if __name__ == '__main__':
    main()
