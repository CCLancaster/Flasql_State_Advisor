from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

    points = db.relationship('Point', backref='state', lazy=True)

    def __repr__(self):
        return f"State(id={self.id}, name='{self.name}', capital='{self.capital}', date_est={self.date_est}, abbr='{self.abbr}', motto='{self.motto}')"
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

point_flags = db.Table('point_flags',
    db.Column('flag_id', db.Integer, db.ForeignKey('flags.id'), primary_key=True),
    db.Column('point_id', db.Integer, db.ForeignKey('points.id'), primary_key=True)
)

class Point(db.Model):
    __tablename__ = 'points'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    lat = db.Column(db.Integer)
    lon = db.Column(db.Integer)
    description = db.Column(db.String(200))
    state_id = db.Column(db.Integer, db.ForeignKey('states.id', ondelete='CASCADE'))

    flags = db.relationship('Flag',
        secondary=point_flags,
        lazy='subquery',
        backref=db.backref('points', lazy=True)
    )

    def __repr__(self):
        return f"Point(id={self.id}, name='{self.name}', lat={self.lat}, lon={self.lon}, description='{self.description}', state_id={self.state_id})"

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lon': self.lon,
            'description': self.description,
            'state': self.state_id.as_dict()['name'],
        }

class Flag(db.Model):
    __tablename__ = 'flags'

    id = db.Column(db.Integer, primary_key=True)
    flag = db.Column(db.String(25), unique=True, nullable=False)

    def __repr__(self):
        return f"Flag(id={self.id}, flag='{self.flag}')"
    
    def as_dict(self):
        return {'id': self.id, 'flag': self.flag}

def get_or_create(model, defaults=None, **kwargs):
  instance = db.session.query(model).filter_by(**kwargs).first()
  if instance:
    return instance, False
  else:
    params = dict((k, v) for k, v in kwargs.items())
    params.update(defaults or {})
    instance = model(**params)
    db.session.add(instance)
    db.session.commit()
    return instance, True