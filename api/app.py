from flask import Flask, request, jsonify
import pandas as pd
import os
from workflow.workflow import run_workflow

app = Flask(__name__)

# Determine the correct path to the CSV file
csv_file_path = os.path.join(os.path.dirname(__file__), '../data_collection/scholarships.csv')

@app.route('/match', methods=['POST'])
def match_scholarships():
    try:
        user_profile = request.json
        df = pd.read_csv(csv_file_path)
        results = run_workflow(user_profile, df)

        # Ensure results is a DataFrame and convert to a list of dictionaries
        if isinstance(results, pd.DataFrame):
            results = results.to_dict(orient='records')
        
        # Return the data as a JSON array
        return jsonify(results)
    except FileNotFoundError:
        return jsonify({"error": "CSV file not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)