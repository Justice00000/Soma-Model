from sqlalchemy import create_engine
from pymongo import MongoClient

def save_to_sql(scholarships, db_url, table_name):
    """
    Save scholarships data to a SQL database.
    """
    engine = create_engine(db_url)
    scholarships.to_sql(table_name, engine, if_exists='replace')

def save_to_mongo(scholarships, db_url, db_name, collection_name):
    """
    Save scholarships data to a MongoDB database.
    """
    client = MongoClient(db_url)
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_many(scholarships.to_dict('records'))

# Example usage:
# save_to_sql(scholarships, 'mysql://username:password@localhost/scholarships_db', 'scholarships')
# save_to_mongo(scholarships, 'mongodb://localhost:27017/', 'scholarships_db', 'scholarships')