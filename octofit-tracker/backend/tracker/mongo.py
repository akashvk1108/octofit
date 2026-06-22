import os
from pathlib import Path
from pymongo import MongoClient

BASE_DIR = Path(__file__).resolve().parent.parent
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017')
client = MongoClient(MONGODB_URI)
db = client['octofit_tracker']
activities_collection = db['activities']


def serialize_activity(doc):
    return {
        'id': str(doc.get('_id')),
        'user': doc.get('user', ''),
        'title': doc.get('title', ''),
        'description': doc.get('description', ''),
        'duration_minutes': doc.get('duration_minutes', 0),
        'date': doc.get('date', ''),
    }
