import pandas as pd

def load_scholarships(file_path):
    """
    Load scholarships data from a CSV file.
    """
    return pd.read_csv(file_path)

# Example usage:
# scholarships = load_scholarships('data/scholarships.csv')