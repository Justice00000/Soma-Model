import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the scraped scholarship data from a CSV file
def load_scholarships_from_csv(file_path):
    try:
        # Load the CSV, skipping lines with incorrect field numbers
        scholarships = pd.read_csv(file_path, on_bad_lines='warn')
        # Replace NaN values with an empty string or None
        scholarships = scholarships.fillna()  # Replacing NaN with an empty string for JSON compatibility
        return scholarships
    except pd.errors.ParserError as e:
        print(f"Error reading CSV file: {e}")
        return pd.DataFrame()

def match_scholarships(user_profile, scholarships):
    # Example matching logic based on title
    scholarships['match_score'] = scholarships['Title'].apply(lambda x: score_title(x, user_profile['degree']))
    
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
scholarships = load_scholarships_from_csv(csv_file_path)

@app.route('/match-scholarships', methods=['POST'])
def get_matched_scholarships():
    user_profile = request.json
    matched_scholarships = match_scholarships(user_profile, scholarships)
    
    # Convert the top matches to a JSON-friendly format
    top_matches = matched_scholarships.head(5).to_dict(orient='records')
    
    return jsonify(top_matches)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)