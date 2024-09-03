from flask import Flask, request, jsonify, Response
import pandas as pd
import json

app = Flask(__name__)

# Function to load scholarships from CSV
def load_scholarships_from_csv(file_path):
    try:
        return pd.read_csv(file_path, on_bad_lines='warn')
    except pd.errors.ParserError as e:
        print(f"Error reading CSV file: {e}")
        return pd.DataFrame()

# Matching function
def match_scholarships(user_profile, scholarships):
    scholarships['match_score'] = scholarships['Title'].apply(lambda x: score_title(x, user_profile['degree']))
    matched_scholarships = scholarships.sort_values(by='match_score', ascending=False)
    return matched_scholarships

# Scoring function
def score_title(title, degree):
    title = title.lower()
    degree = degree.lower()
    if degree in title:
        return 10
    elif any(word in title for word in degree.split()):
        return 5
    return 0

# Load scholarships data
csv_file_path = 'scholarships.csv'
scholarships = load_scholarships_from_csv(csv_file_path)

@app.route('/match-scholarships', methods=['POST'])
def get_matched_scholarships():
    user_profile = request.json
    matched_scholarships = match_scholarships(user_profile, scholarships)
    top_matches = matched_scholarships.head(5).to_dict(orient='records')

    # Ensure the response is treated as JSON
    response_json = json.dumps(top_matches)
    
    return Response(response=response_json, status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)