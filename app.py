from flask import Flask, render_template, request, redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy
import re
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(50))
    last = db.Column(db.String(50))
    address = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(15))

with app.app_context():
    db.create_all()

def valid_email(email):
    return re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email)


def valid_phone(phone):
    return re.match(r"^[0-9]{10}$", phone)   # 10 digit phone number

@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        email = request.form['email']

        if not valid_email(email):
            flash("Invalid Email Format!", "danger")
            return redirect(url_for('add'))
        if not valid_phone(request.form['phone']):
            flash("Phone must be valid", "danger")
            return redirect(url_for('add'))
        if Contact.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(url_for('add'))

        contact = Contact(
            first=request.form['first'],
            last=request.form['last'],
            address=request.form['address'],
            email=email,
            phone=request.form['phone']
        )

        db.session.add(contact)
        db.session.commit()
        return redirect('/')

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    contact = Contact.query.get(id)

    if request.method == 'POST':
        contact.first = request.form['first']
        contact.last = request.form['last']
        contact.email = request.form['email']
        contact.address = request.form['address']
        contact.phone = request.form['phone']

        if not valid_phone(request.form['phone']):
            flash("Phone must be valid!", "danger")
            return redirect(url_for('add'))
        if not valid_email(request.form['email']):
            flash("Email must be valid!", "danger")
            return redirect(url_for('add'))


        db.session.commit()
        return redirect('/')

    return render_template('edit.html', contact=contact)

@app.route('/delete/<int:id>')
def delete(id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)