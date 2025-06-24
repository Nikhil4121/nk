


from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'
import os

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(app.instance_path, "nk_web.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Nkweb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<Nkweb {self.name}>'

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    users = Nkweb.query.all()
    return render_template('home.html', users=users)

@app.route('/add_user', methods=['GET'])
def get_users():
    users = Nkweb.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email, 'message': user.message} for user in users])

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.is_json:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

    if not name or not email or not message:
        flash('All fields are required.', 'error')
        return redirect(url_for('home'))

    new_user = Nkweb(name=name, email=email, message=message)

    db.session.add(new_user)
    db.session.commit()

    flash('Message sent successfully!', 'success')
    return redirect(url_for('home'))
    

if __name__ == '__main__':
    
    app.run(debug=True)