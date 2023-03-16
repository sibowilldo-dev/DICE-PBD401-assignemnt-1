from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutdb.db'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class applications(db.Model):
    u_id = db.column('user_id', db.int, primary_key=True)
    vac_id = db.column('vacancy_id', db.int, primary_key=True)
    stat_id = db.column('status_id', db.int)
    created = db.column('created_at', db.datetime)
    updated = db.column('updated_at', db.datetime)

    def _init_(self, u_id, vac_id, stat_id, created, updated):
        self.u_id = u_id
        self.vac_id = vac_id
        self.stat_id = stat_id
        self.created = created
        self.updated = updated


class documents(db.model):
    id = db.column('id', db.int, primary_key=True)
    appl_id = db.column('application_id', db.int, foreign_key=True)
    title = db.column('title', db.String(100))
    descr = db.column('description', db.String(100))
    loc = db.column('location', db.String(100))
    doc_type = db.column('document_type', db.String(100))
    created = db.column('created_at', db.datetime)
    updated = db.column('updated_at', db.datetime)

    def _init_(self, appl_id, title, descr, loc, doc_type, created, updated):
        self.appl_id = appl_id
        self.title = title
        self.descr = descr
        self.loc = loc
        self.type = doc_type
        self.created = created
        self.updated = updated


class statuses(db.Model):
    id = db.column('id', db.int, primary_key=True)
    mod_type = db.column('model_type', db.String(100))
    name = db.column('name', db.String(100))
    descr = db.column('description', db.String(100))
    created = db.column('created_at', db.datetime)
    updated = db.column('updated_at', db.datetime)

    def _init_(self, mod_type, name, descr, created, updated):
        self.mod_type = mod_type
        self.name = name
        self.descr = descr
        self.created = created
        self.updated = updated


class users(db.Model):
    id = db.column('id', db.int, primary_key=True, foreign_key=True)
    email = db.column('email', db.String(100))
    stat_id = db.column('status_id', db.int, foreign_key=True)
    created = db.column('created_at', db.datetime)
    updated = db.column('updated_at', db.datetime)

    def _init_(self, email, stat_id, created, updated):
        self.email = email
        self.stat_id = stat_id
        self.created = created
        self.updated = updated


class profile(db.model):
    id = db.column('id', db.int, primary_key=True)
    user_id = db.column('id', db.int, foreign_key=True)
    g_name = db.column('given_name', db.String(100))
    f_name = db.column('family_name', db.String(100))
    name = db.column('name', db.String(100))
    created = db.column('created_at', db.datetime)
    updated = db.column('updated_at', db.datetime)

    def _init_(self, user_id, g_name, f_name, name, created, updated):
        self.user_id = user_id
        self.g_name = g_name
        self.f_name = f_name
        self.name = name
        self.created = created
        self.updated = updated


class categories(db.model):
    id = db.column('id', db.int, primary_key=True)
    name = db.column('name', db.String(100))
    created = db.column('created_at', db.datetime)
    updated = db.column('updated_at', db.datetime)

    def _init_(self, name, created, updated):
        self.name = name
        self.created = created
        self.updated = updated


class types(db.model):
    id = db.column('id', db.int, primary_key=True)
    name = db.column('name', db.String(100))
    created = db.column('created_at', db.datetime)
    updated = db.column('updated_at', db.datetime)

    def _init_(self, name, created, updated):
        self.name = name
        self.created = created
        self.updated = updated


class vacancies(db.model):
    id = db.column('id', db.int, primary_key=True)
    cat_id = db.column('category_id', db.int, foreign_key=True)
    type_id = db.column('type_id', db.int, foreign_key=True)
    title = db.column('title', db.String(100))
    descr = db.column('description', db.String(100))
    exp = db.column('expires_at', db.datetime)
    created = db.column('created_at', db.datetime)
    updated = db.column('updated_at', db.datetime)

    def _init_(self, cat_id, type_id, title, descr, exp, created, updated):
        self.cat_id = cat_id
        self.type_id = type_id
        self.title = title
        self.descr = descr
        self.exp = exp
        self.created = created
        self.updated = updated
