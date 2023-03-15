# app.py

from flask import Flask, render_template, request
from backend.database.models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Get form data
        id = request.form['id']
        email = request.form['email']


        # Create new user
        user = User(id=id, email=email)

        # Add user to database
        db.session.add(user)
        db.session.commit()

        # Display success message
        message = f"User {id} created successfully."
        return render_template('admin.html', message=message)
    else:
        return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)

