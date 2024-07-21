from load_data import load_scholarships
from preprocess import preprocess_data
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

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
    X_train, X_test, y_train, y_test = preprocess_data(scholarships, user_profile)

    # Train the model
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy * 100:.2f}%')

    # Optionally save to database
    # save_to_sql(scholarships, 'mysql://username:password@localhost/scholarships_db', 'scholarships')
    # save_to_mongo(scholarships, 'mongodb://localhost:27017/', 'scholarships_db', 'scholarships')

if __name__ == '__main__':
    main()