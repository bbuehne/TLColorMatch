from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from tlcolor import RGB


# Firebase
def connect_db():
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'project_id': 'tlcolormatch',
    })

    db = firestore.client()
    return db


app = Flask(__name__)


@app.route('/')
def index():
    if request.method == 'POST':
        name = request.form['title']
        sensor_data = request.form['sensordata']

        if not name:
            flash('Name is required')
        else:
            db = connect_db()
            lines = sensor_data.splitline()
            for line in lines:
                if 'sRGB' not in line:
                    continue
                else:
                    rgb = line.split(':')[1][1:].split(',')
                    doc_ref = db.collection('samples').document(name)
                    doc_ref.set({
                        'name' : name,
                        'r' : int(rgb[0]),
                        'g' : int(rgb[1]),
                        'b' : int(rgb[2])
                    })
                    return redirect(url_for('color_samples'))
    return render_template('index.html')

@app.route('/color_samples')
def color_samples():
    return render_template('color_samples.html')

if __name__ == '__main__':
    app.run()
