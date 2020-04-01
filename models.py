from flask import Flask
from flask_sqlalchemy import flask_sqlalchemy

app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flasky_state'
db = SQLAlchemy(app)

class State(db.Model):
    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    capital = db.Column(db.String, nullable=True)
    date_est = db.Column(db.Integer, nullable=True)
    abbr = db.Column(db.String(2))
    motto = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"State(id={self.id}, capital='{self.capital}', date_est={self.date_est}, abbr='{self.abbr}', motto='{self.motto}')"
