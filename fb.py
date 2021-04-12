import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore




# Use the application default credentials
def connect_db():
  cred = credentials.ApplicationDefault()
  firebase_admin.initialize_app(cred, {
    'project_id': 'tlcolormatch',
  })

  db = firestore.client()
  return db

def stock_data():
  db = connect_db()

  sample_list = [
    {'name': 'demogreen', 'r': 58, 'g': 85, 'b': 78},
    {'name': 'demoone', 'r': 158, 'g': 5, 'b': 78},
    {'name': 'demotwo', 'r': 8, 'g': 85, 'b': 201},
    {'name': 'demothree', 'r': 58, 'g': 185, 'b': 78},
  ]

  for sample in sample_list:
    doc_ref = db.collection(u'samples').document(sample['name'])
    doc_ref.set({
      u'name' : sample['name'],
      u'r' : sample['r'],
      u'g' : sample['g'],
      u'b' : sample['b']
    })