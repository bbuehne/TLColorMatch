from flask import Flask, render_template, request, url_for, flash, redirect

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from colormap.colors import rgb2hex
from colormap.colors import hex2rgb

from math import sqrt

# Firebase
def connect_db():
    cred = credentials.ApplicationDefault()
    default_app = firebase_admin.initialize_app(cred, {
        'project_id': 'tlcolormatch',
    })

    db = firestore.client()
    return db

def get_sample_list():
    doc_ref = fdb.collection('samples')
    samples = doc_ref.get()
    sample_list = {}
    for sample in samples:
        ss = sample.to_dict()
        sample_list[ss['name']] = ss
        sample_list[ss['name']]['rgb'] = hex2rgb(ss['hex_color'])
    return sample_list

def distance(color):
    r, g, b = color[1]
    sample_list = get_sample_list()
    samples = [ (sample_list[x]['name'], sample_list[x]['rgb']) for x in sample_list]
    distance_list = []
    for sample in samples:
        sr, sg, sb = sample[1]
        color_diff = round(sqrt(abs(r - sr)**2 + abs(g - sg)**2 + abs(b - sb)**2) / sqrt(3*(255**2)),4)
        distance_list.append((color_diff, sample[0], rgb2hex(sr, sg, sb)))

    def dist_val(e):
        return e[0]

    distance_list.sort(key=dist_val)

    return distance_list


app = Flask(__name__)


@app.route('/', methods=('GET','POST'))
def index():
    app.name = 'tlcolormatch'
    app.config['SECRET_KEY'] = 'lkasd83ksu39si23'
    if request.method == 'POST':
        name = request.form['title']
        sensor_data = request.form['sensordata']
        distance_data = ()
        if not name:
            flash('Name is required')
        else:
            lines = sensor_data.splitlines()
            for line in lines:
                if 'HEX' not in line:
                    continue
                else:
                    hex_color = line.split(':')[1][1:]
                    color = (name,hex2rgb(hex_color))
                    distance_list = distance(color)[:10]
                    color = (name, hex_color)
                    distance_data = (color, distance_list)
    else:
        distance_data = ()
    return render_template('index.html', distance_data=distance_data)

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
                if 'HEX' not in line:
                    continue
                else:
                    hex_color = line.split(':')[1][1:]
                    doc_ref = fdb.collection('samples').document(name)
                    doc_ref.set({
                        'name' : name,
                        'hex_color' : hex_color
                    })
                    return redirect(url_for('color_samples'))

    # retrieve samples
    sample_list = get_sample_list()
    samples = [ sample_list[x] for x in sorted(sample_list)]

    return render_template('color_samples.html', samples=samples)

fdb = connect_db()
if __name__ == '__main__':
    app.run()
