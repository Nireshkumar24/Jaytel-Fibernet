from ensurepip import bootstrap
from operator import index
from flask_bootstrap import Bootstrap
from flask import Flask,render_template, request,jsonify,redirect, session,g, url_for,flash
import logging,json,os
import os
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

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Implement your authentication logic here
        if username == 'Jaytel_Fibernet' and password == 'Jaytel@2024':  # Placeholder, use real validation
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html')
    return render_template('login.html')
 
@app.route('/logout')
def logout():
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
    query_results = Register.query.all()
    data = [{'ID': r.id, 'Name': r.Name, 'Contact': r.Contact, 'Address': r.Address} for r in query_results]
    df = pd.DataFrame(data, columns=['ID', 'Name', 'Contact', 'Address'])   
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    
    return send_file(output, as_attachment=True, attachment_filename='export.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/delete_all_data')
def delete_all_data():
    try:
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
        return "All data deleted successfully!"
    except Exception as e:
        db.session.rollback()
        return "Error occurred while deleting data: " + str(e)

@app.route('/delete/<int:record_id>')
def delete_record(record_id):
    try:
        record = Register.query.get(record_id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return f"Record with ID {record_id} deleted successfully."
        else:
            return f"No record found with ID {record_id}."
    except Exception as e:
        db.session.rollback()
        return f"Error occurred while deleting record with ID {record_id}: {str(e)}"


if __name__ == '__main__':
     app.run(port=5001,debug=True)