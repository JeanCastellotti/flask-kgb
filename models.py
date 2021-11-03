from app import db, login_manager
from datetime import datetime, date
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


missions_agents = db.Table(
    'missions_agents',
    db.Column('mission_id',
              db.Integer,
              db.ForeignKey('missions.id'),
              primary_key=True),
    db.Column('agent_id',
              db.Integer,
              db.ForeignKey('agents.user_id'),
              primary_key=True))

missions_targets = db.Table(
    'missions_targets',
    db.Column('mission_id',
              db.Integer,
              db.ForeignKey('missions.id'),
              primary_key=True),
    db.Column('target_id',
              db.Integer,
              db.ForeignKey('targets.user_id'),
              primary_key=True))

missions_contacts = db.Table(
    'missions_contacts',
    db.Column('mission_id',
              db.Integer,
              db.ForeignKey('missions.id'),
              primary_key=True),
    db.Column('contact_id',
              db.Integer,
              db.ForeignKey('contacts.user_id'),
              primary_key=True))

missions_hideouts = db.Table(
    'missions_hideouts',
    db.Column('mission_id',
              db.Integer,
              db.ForeignKey('missions.id'),
              primary_key=True),
    db.Column('hideout_id',
              db.Integer,
              db.ForeignKey('hideouts.id'),
              primary_key=True))


class Mission(db.Model):
    __tablename__ = 'missions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    code = db.Column(db.String(10), nullable=False)
    country_id = db.Column(db.Integer,
                           db.ForeignKey('countries.id'),
                           nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)
    speciality_id = db.Column(db.Integer,
                              db.ForeignKey('specialities.id'),
                              nullable=False)
    status = db.Column(db.String(10), nullable=False, default='preparation')
    starts_at = db.Column(db.Date, nullable=False, default=date.today)
    ends_at = db.Column(db.Date, nullable=False, default=date.today)
    agents = db.relationship('Agent',
                             secondary=missions_agents,
                             backref=db.backref('missions'))
    targets = db.relationship('Target',
                              secondary=missions_targets,
                              backref=db.backref('missions'))
    contacts = db.relationship('Contact',
                               secondary=missions_contacts,
                               backref=db.backref('missions'))
    hideouts = db.relationship('Hideout',
                               secondary=missions_hideouts,
                               backref=db.backref('missions'))


class Type(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    missions = db.relationship('Mission', backref='type')


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    type = db.Column(db.String(20))

    __mapper_args__ = {'polymorphic_identity': 'user', 'polymorphic_on': type}

    def __str__(self):
        return f'{self.firstname} {self.lastname} ({self.country.name})'


class Agent(User):
    __tablename__ = 'agents'
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True)
    birthdate = db.Column(db.Date)
    code = db.Column(db.String)
    nationality_id = db.Column(db.Integer,
                               db.ForeignKey('countries.id'),
                               nullable=False)
    speciality_id = db.Column(db.Integer,
                              db.ForeignKey('specialities.id'),
                              nullable=False)

    __mapper_args__ = {'polymorphic_identity': 'agent'}


class Target(User):
    __tablename__ = 'targets'
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True)
    birthdate = db.Column(db.Date)
    code = db.Column(db.String)
    nationality_id = db.Column(db.Integer,
                               db.ForeignKey('countries.id'),
                               nullable=False)

    __mapper_args__ = {'polymorphic_identity': 'target'}


class Contact(User):
    __tablename__ = 'contacts'
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True)
    birthdate = db.Column(db.Date)
    code = db.Column(db.String(10))
    nationality_id = db.Column(db.Integer,
                               db.ForeignKey('countries.id'),
                               nullable=False)

    __mapper_args__ = {'polymorphic_identity': 'contact'}


class Admin(User):
    __tablename__ = 'admins'
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    __mapper_args__ = {'polymorphic_identity': 'admin'}


class Speciality(db.Model):
    __tablename__ = 'specialities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    agents = db.relationship('Agent', backref='speciality')
    missions = db.relationship('Mission', backref='required_speciality')

    def __str__(self):
        return self.name


class Hideout(db.Model):
    __tablename__ = 'hideouts'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    country_id = db.Column(db.Integer,
                           db.ForeignKey('countries.id'),
                           nullable=False)

    def __str__(self):
        return f'{self.code} ({self.country.name})'


class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    hideouts = db.relationship('Hideout', backref='country')
    missions = db.relationship('Mission', backref='country')
    agents = db.relationship('Agent', backref='country')
    targets = db.relationship('Target', backref='country')
    contacts = db.relationship('Contact', backref='country')
