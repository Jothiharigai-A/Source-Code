import numpy as np
from flask import Flask, request, jsonify, render_template,session, redirect, url_for
import pickle
import pandas as pd
import csv
from flask_sqlalchemy import SQLAlchemy
from sklearn.compose import ColumnTransformer




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


# model = pickle.load(open('model.pkl', 'rb'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('home.html', message="Invalid username and password")
    


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], password=request.form['password']))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('login.html', message="User Already Exists")
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('service'))
        return render_template('service.html', message="Incorrect Details")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))

@app.route('/service')
def service():
    return render_template('service.html')


@app.route('/preview')
def preview():
    with open("dataset.csv") as file:
        reader = csv.reader(file)
        return render_template('CSV_Priview.html',data=reader)
    

@app.route('/graph')
def graph():
    return render_template("graph.html")
    

@app.route('/result')
def result():
    if request.method == 'POST':
        input= request.form
        mh_predict = pd.DataFrame({
            'Gender': [input['Gender']],
            'Self_Employed': [input['Self_Employed']],
            'Family_History': [input['Family_History']],
            'Work_Interfere': [input['Work_Interfere']],
            'Employee_Numbers': [input['Employee_Numbers']],
            'Tech_Company': [input['Tech_Company']],
            'Benefits': [input['Benefits']],
            'Care_Options': [input['Care_Options']],
            'Seek_Help': [input['Seek_Help']],
            'Anonymity': [input['Anonymity']],
            'Medical_Leave': [input['Medical_Leave']],
            'Mental_Health_Consequence': [input['Mental_Health_Consequence']],
            'Coworkers': [input['Coworkers']],
            'Supervisor': [input['Supervisor']],
            'Mental_Health_Interview': [input['Mental_Health_Interview']],
            'Physical_Health_Interview': [input['Physical_Health_Interview']],
            'Mental_VS_Physical': [input['Mental_VS_Physical']],
            'Observed_Consequence': [input['Observed_Consequence'],]
        })
        prediksi= model.predict_proba(mh_predict)[0][1]

        if prediksi>0.5:
            pred= 'Get Treatment'
        else:
            pred= 'No Treatment'
    return render_template('result.html')


if __name__ == "__main__":
    app.secret_key = "ThisIsNotASecret:p"
    filename= r'D:\Source Code\Final_Project.sav'
    model= pickle.load(open(filename, 'rb'))
    with app.app_context():
        db.create_all()
        app.run(debug=True)
