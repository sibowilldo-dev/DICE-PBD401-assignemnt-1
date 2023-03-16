from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/check_progress', methods=['GET', 'POST'])
def check_progress():
    if request.method == 'POST':
        email = request.form['email']
        conn = sqlite3.connect('Application.db')
        c = conn.cursor()
        c.execute("SELECT * FROM applications WHERE email=?", (email,))
        rows = c.fetchall()
        conn.close()
        return render_template('progress.html', rows=rows)
    return render_template('check_progress.html')

if __name__ == '__main__':
    app.run(debug=True)

