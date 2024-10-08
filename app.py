from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Load the scraped scholarship data from a CSV file
def load_scholarships_from_csv(file_path):
    try:
        # Load the CSV file, skipping lines with too many fields and print a warning for each
        df = pd.read_csv(file_path, on_bad_lines='warn')
        # Replace NaN values with empty strings
        df = df.fillna('')
        return df
    except pd.errors.ParserError as e:
        print(f"Error reading CSV file: {e}")
        return pd.DataFrame()

# Function to match scholarships based on user profile and other fields
def match_scholarships(user_profile, scholarships):
    scholarships['match_score'] = scholarships.apply(lambda x: calculate_match_score(x, user_profile), axis=1)
    
    # Sort by match score in descending order
    matched_scholarships = scholarships.sort_values(by='match_score', ascending=False)
    
    return matched_scholarships

# Scoring function based on various fields
def calculate_match_score(scholarship, user_profile):
    score = 0
    degree = user_profile['degree'].lower()
    location = user_profile['location'].lower()
    funds_needed = float(user_profile['funds_needed'])  # Convert to float for comparison
    
    # Scoring based on description
    if degree in scholarship['description'].lower():
        score += 10
    
    # Scoring based on location
    if location in scholarship['location'].lower():
        score += 10
    
    # Scoring based on funds needed vs scholarship grant
    if scholarship['Grant']:
        try:
            grant = float(scholarship['Grant'])  # Convert to float for comparison
            if funds_needed <= grant:
                score += 5
        except ValueError:
            pass  # Handle the case where 'Grant' cannot be converted to float

    # Scoring based on scholarship type and eligibility
    if 'scholaship_type' in scholarship and scholarship['scholaship_type'].lower() in user_profile.get('applicable_programmes', '').lower():
        score += 5

    # Scoring based on field of study match
    if 'field_of_study' in scholarship and degree in scholarship['field_of_study'].lower():
        score += 7
    
    # Additional matching for benefits, age, and experience if available
    if scholarship.get('age'):
        try:
            age = int(user_profile.get('age', 0))
            scholarship_age = int(scholarship['age'])
            if age <= scholarship_age:
                score += 3
        except ValueError:
            pass  # Handle the case where 'age' cannot be converted to int

    if scholarship.get('study_experience_required') and user_profile.get('study_experience', '').lower() in scholarship['study_experience_required'].lower():
        score += 5
    
    return score

# Load the scholarship data (assumes the CSV file is in the same directory)
csv_file_path = 'scholaships.csv'
scholarships = load_scholarships_from_csv(csv_file_path)

# API Endpoint to match scholarships
@app.route('/match_scholarships', methods=['POST'])
def match_scholarships_endpoint():
    try:
        # Get user profile data from request body (in JSON format)
        user_profile = request.json

        # Perform the matching
        matched_scholarships = match_scholarships(user_profile, scholarships)

        # Select top 5 matches
        top_matches = matched_scholarships.head(5).to_dict(orient='records')
        
        # Return the top matches as JSON response
        return jsonify(top_matches)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Main entry point
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Ensure this matches your Render configuration
    app.run(host='0.0.0.0', port=port, debug=True)