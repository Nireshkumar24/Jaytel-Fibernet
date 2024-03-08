from ensurepip import bootstrap
from operator import index
from flask_bootstrap import Bootstrap
from flask import Flask,render_template, request,jsonify,redirect, session,g, url_for,flash
import logging,json,os
from kiteconnect import KiteConnect
import os
from flask_mysqldb import MySQL
import bcrypt
import mysql.connector
from mysql.connector import Error
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask import send_file
import pandas as pd
from io import BytesIO


app = Flask(__name__,template_folder='templates',static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Jaytel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a Stock model
class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(64), nullable=False)
    Contact = db.Column(db.Integer, nullable=False)
    Address = db.Column(db.String(500), nullable=False)
    
# Create the database tables
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method == 'POST':
      Register1 = Register(
           Name=request.form.get('name'),
           Contact=request.form.get('contact', type=int),
           Address=request.form.get('sendermessage'))
      db.session.add(Register1)
      db.session.commit()
      
    return render_template('contact.html')
 

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/dashboard')
# def dashboard():
#      entries = Register.query.all()
#      return render_template('Dashboard.html',entries=entries)
 
 

# @app.route('/dashboard', methods=['GET', 'POST'])
# def dashboard():
#     search_query = request.args.get('search')  # Get the search term from the query string
#     if search_query:
#         # Filter entries where name is like the search query
#         entries = Register.query.filter(Register.Contact.like(f'%{search_query}%')).all()
#     else:
#         # If no search query, display all entries
#         entries = Register.query.all()
#     return render_template('Dashboard.html', entries=entries)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    search_query = request.args.get('search', '')  # Get the search term from the query string
    if search_query:
        # Filter entries where any field matches the search query
        entries = Register.query.filter(
            or_(
                Register.Name.like(f'%{search_query}%'),
                Register.Contact.like(f'%{search_query}%'),
                Register.Address.like(f'%{search_query}%')
            )
        ).all()
    else:
        # If no search query, display all entries
        entries = Register.query.all()
    return render_template('Dashboard.html', entries=entries)


@app.route('/export_data')
def export_data():
    # Query your database for the data you want to export
    # Here, I'm assuming you're exporting all entries from the Register model
    query_results = Register.query.all()
    
    # Convert query results into a list of dictionaries
    data = [r.__dict__ for r in query_results]
    
    # Create a Pandas DataFrame from the list of dictionaries
    # Exclude '_sa_instance_state' from our records
    df = pd.DataFrame(data).drop('_sa_instance_state', axis=1)
    
    # Create a BytesIO buffer to save the Excel file in memory
    output = BytesIO()
    
    # Use the DataFrame's to_excel method to write the DataFrame to the BytesIO buffer
    # Make sure to specify the engine as 'openpyxl'
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    # Rewind the buffer
    output.seek(0)
    
    # Send the Excel file as a downloadable response
    return send_file(output, as_attachment=True, attachment_filename='export.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
     app.run(port=5001,debug=True)