from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

from tlcolor import RGB


# Firebase
def connect_db():
    cred = credentials.ApplicationDefault()
    default_app = firebase_admin.initialize_app(cred, {
        'project_id': 'tlcolormatch',
    })

    db = firestore.client()
    return db


app = Flask(__name__)


@app.route('/', methods=('GET','POST'))
def index():
    app.name = 'tlcolormatch'
    app.config['SECRET_KEY'] = 'lkasd83ksu39si23'
    if request.method == 'POST':
        name = request.form['title']
        sensor_data = request.form['sensordata']

        if not name:
            flash('Name is required')
        else:

            lines = sensor_data.splitlines()
            for line in lines:
                if 'sRGB' not in line:
                    continue
                else:
                    rgb = line.split(':')[1][1:].split(',')

    return render_template('index.html')

@app.route('/color_samples', methods=('GET','POST'))
def color_samples():
    if request.method == 'POST':
        name = request.form['title']
        sensor_data = request.form['sensordata']
        if not name:
            flash('Name is required')
        else:
            lines = sensor_data.splitlines()
            for line in lines:
                if 'sRGB' not in line:
                    continue
                else:
                    rgb = line.split(':')[1][1:].split(',')
                    doc_ref = fdb.collection('samples').document(name)
                    doc_ref.set({
                        'name' : name,
                        'r' : int(rgb[0]),
                        'g' : int(rgb[1]),
                        'b' : int(rgb[2])
                    })
                    return redirect(url_for('color_samples'))

    # retrieve samples
    doc_ref = fdb.collection('samples')
    samples = doc_ref.get()
#    print(dir(samples))
    sample_list = {}
    for sample in samples:
        sample_list[sample.to_dict()['name']] = sample.to_dict()
    print(sorted(sample_list))
    samples = [ sample_list[x] for x in sorted(sample_list)]
    print(samples)

    return render_template('color_samples.html', samples=samples)

fdb = connect_db()
if __name__ == '__main__':
    app.run()
