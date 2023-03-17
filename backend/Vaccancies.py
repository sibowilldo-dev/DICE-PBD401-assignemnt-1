from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    applications = db.relationship('Application', backref='job', lazy=True)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

@app.route('/')
def index():
    jobs = Job.query.all()
    return render_template('index.html', jobs=jobs)

@app.route('/job/<int:id>')
def job(id):
    job = Job.query.get_or_404(id)
    return render_template('job.html', job=job)

@app.route('/job/<int:id>/apply', methods=['GET', 'POST'])
def apply(id):
    job = Job.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        application = Application(name=name, email=email, job_id=job.id)
        db.session.add(application)
        db.session.commit()
        return redirect(url_for('job', id=id))
    return render_template('apply.html', job=job)

@app.route('/job/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        job = Job(title=title, description=description)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)
