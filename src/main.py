import pandas as pd

# Sample user profile data
user_profile = {
    'degree': 'High School',
    'funds_needed': 5000,
    'location': 'canada'
}

# Load the scraped scholarship data from a CSV file
def load_scholarships_from_csv(file_path):
    try:
        # Skip lines with too many fields and print a warning for each
        return pd.read_csv(file_path, on_bad_lines='warn')
    except pd.errors.ParserError as e:
        print(f"Error reading CSV file: {e}")
        return pd.DataFrame()

def match_scholarships(user_profile, scholarships):
    # Example matching logic based on title
    # Updated scoring function for better matching
    scholarships['match_score'] = scholarships['description'].apply(lambda x: score_title(x, user_profile['degree']))
    
    # Sort by match score in descending order
    matched_scholarships = scholarships.sort_values(by='match_score', ascending=False)
    
    return matched_scholarships

def score_title(title, degree):
    # Improved scoring function
    title = title.lower()
    degree = degree.lower()
    
    # Simple scoring based on the presence of degree in the title
    if degree in title:
        return 10  # High score for a match
    elif any(word in title for word in degree.split()):
        return 5  # Partial match score
    return 0  # No match

# File path to the CSV containing scraped scholarships
csv_file_path = 'scholaships.csv'

# Load the scholarships data
scholarships = load_scholarships_from_csv(csv_file_path)

# Get matched scholarships
matched_scholarships = match_scholarships(user_profile, scholarships)

# Display top matches (e.g., top 5)
top_matches = matched_scholarships.head(5)
print("Top Matched Scholarships:")
print(top_matches)