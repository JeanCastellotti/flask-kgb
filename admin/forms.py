from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from models import Speciality, Country, Agent, Target, Contact, Hideout, Type


def required_if(form, field):
    if form.status.data == 'failed':
        return True
    elif not len(field.data):
        raise ValidationError('Ce champs est obligatoire')


class MissionForm(FlaskForm):
    title = StringField('Titre de la mission',
                        validators=[
                            DataRequired('Ce champs est obligatoire.'),
                            Length(max=150)
                        ])
    description = TextAreaField(
        'Description de la mission',
        validators=[DataRequired('Ce champs est obligatoire.')])
    code = StringField('Code',
                       validators=[
                           DataRequired('Ce champs est obligatoire.'),
                           Length(max=10)
                       ])
    country = QuerySelectField(
        'Pays',
        validators=[DataRequired('Ce champs est obligatoire.')],
        query_factory=lambda: Country.query.order_by('name').all(),
        allow_blank=True,
        blank_text='Choisir un pays',
        get_label='name')
    type = QuerySelectField(
        'Type',
        validators=[DataRequired('Ce champs est obligatoire.')],
        query_factory=lambda: Type.query.order_by('name').all(),
        allow_blank=True,
        blank_text='Choisir un type',
        get_label='name')
    required_speciality = QuerySelectField(
        'Spécialité requise',
        validators=[DataRequired('Ce champs est obligatoire.')],
        query_factory=lambda: Speciality.query.order_by('name').all(),
        allow_blank=True,
        blank_text='Choisir une spécialité',
        get_label='name')
    status = SelectField('Status',
                         choices=[('preparation', 'En préparation'),
                                  ('progress', 'En cours'),
                                  ('completed', 'Terminée'),
                                  ('failed', 'Échec')],
                         validate_choice=False)
    starts_at = DateField(
        'Début de la mission',
        validators=[DataRequired('Ce champs est obligatoire.')])
    ends_at = DateField(
        'Fin de la mission',
        validators=[DataRequired('Ce champs est obligatoire.')])
    agents = QuerySelectMultipleField('Agents',
                                      validators=[required_if],
                                      query_factory=lambda: Agent.query.all())
    targets = QuerySelectMultipleField(
        'Cibles',
        validators=[required_if],
        query_factory=lambda: Target.query.all())
    contacts = QuerySelectMultipleField(
        'Contacts',
        validators=[required_if],
        query_factory=lambda: Contact.query.all())
    hideouts = QuerySelectMultipleField(
        'Planques', query_factory=lambda: Hideout.query.all())

    def validate_hideouts(self, hideouts):
        if not all(hideout.country == self.country.data
                   for hideout in hideouts.data):
            raise ValidationError(
                'Les planques doivent se trouver dans le même pays.')

    def validate_contacts(self, contacts):
        if not all(contact.country == self.country.data
                   for contact in contacts.data):
            raise ValidationError(
                'Les contacts doivent obligatoirement être de la nationalité du pays de la mission.'
            )

    def validate_agents(self, agents):
        if agents.data and not any(
                agent.speciality == self.required_speciality.data
                for agent in agents.data):
            raise ValidationError(
                'Au moins 1 agent doit disposer de la spécialité requise.')

    def validate_targets(self, targets):
        agents_nationalities = list(
            map(lambda agent: agent.country.nationality, self.agents.data))
        if any(target.country.nationality in agents_nationalities
               for target in targets.data):
            raise ValidationError(
                'La ou les cibles ne peuvent avoir la même nationalité que le ou les agents.'
            )


class CountryForm(FlaskForm):
    name = StringField('Nom du pays',
                       validators=[
                           DataRequired('Ce champs est obligatoire.'),
                           Length(max=50)
                       ])
    nationality = StringField('Nationalité',
                              validators=[
                                  DataRequired('Ce champs est obligatoire.'),
                                  Length(max=50)
                              ])


class SpecialityForm(FlaskForm):
    name = StringField('Nom de la spécialité',
                       validators=[
                           DataRequired('Ce champs est obligatoire.'),
                           Length(max=50)
                       ])


class TypeForm(FlaskForm):
    name = StringField('Nom du type',
                       validators=[
                           DataRequired('Ce champs est obligatoire.'),
                           Length(max=50)
                       ])


class AgentForm(FlaskForm):
    firstname = StringField('Prénom',
                            validators=[
                                DataRequired('Ce champs est obligatoire.'),
                                Length(max=50)
                            ])
    lastname = StringField('Nom',
                           validators=[
                               DataRequired('Ce champs est obligatoire.'),
                               Length(max=50)
                           ])
    birthdate = DateField(
        'Date de naissance',
        validators=[DataRequired('Ce champs est obligatoire.')])
    code = StringField('Code',
                       validators=[
                           DataRequired('Ce champs est obligatoire.'),
                           Length(max=10)
                       ])
    nationality = QuerySelectField(
        'Nationalité',
        validators=[DataRequired('Ce champs est obligatoire.')],
        query_factory=lambda: Country.query.order_by('name').all(),
        allow_blank=True,
        blank_text='Choisir une nationalité',
        get_label='nationality')
    speciality = QuerySelectField(
        'Spécialité',
        validators=[DataRequired('Ce champs est obligatoire.')],
        query_factory=lambda: Speciality.query.order_by('name').all(),
        allow_blank=True,
        blank_text='Choisir une spécialité',
        get_label='name')


class TargetForm(FlaskForm):
    firstname = StringField('Prénom',
                            validators=[
                                DataRequired('Ce champs est obligatoire.'),
                                Length(max=50)
                            ])
    lastname = StringField('Nom',
                           validators=[
                               DataRequired('Ce champs est obligatoire.'),
                               Length(max=50)
                           ])
    birthdate = DateField(
        'Date de naissance',
        validators=[DataRequired('Ce champs est obligatoire.')])
    code = StringField('Code',
                       validators=[
                           DataRequired('Ce champs est obligatoire.'),
                           Length(max=10)
                       ])
    nationality = QuerySelectField(
        'Nationalité',
        validators=[DataRequired('Ce champs est obligatoire.')],
        query_factory=lambda: Country.query.order_by('name').all(),
        allow_blank=True,
        blank_text='Choisir une nationalité',
        get_label='nationality')


class ContactForm(FlaskForm):
    firstname = StringField('Prénom',
                            validators=[
                                DataRequired('Ce champs est obligatoire.'),
                                Length(max=50)
                            ])
    lastname = StringField('Nom',
                           validators=[
                               DataRequired('Ce champs est obligatoire.'),
                               Length(max=50)
                           ])
    birthdate = DateField(
        'Date de naissance',
        validators=[DataRequired('Ce champs est obligatoire.')])
    code = StringField('Code',
                       validators=[
                           DataRequired('Ce champs est obligatoire.'),
                           Length(max=10)
                       ])
    nationality = QuerySelectField(
        'Nationalité',
        validators=[DataRequired('Ce champs est obligatoire.')],
        query_factory=lambda: Country.query.order_by('name').all(),
        allow_blank=True,
        blank_text='Choisir une nationalité',
        get_label='nationality')


class HideoutForm(FlaskForm):
    code = StringField('Code',
                       validators=[
                           DataRequired('Ce champs est obligatoire.'),
                           Length(max=10)
                       ])
    address = StringField('Adresse',
                          validators=[
                              DataRequired('Ce champs est obligatoire.'),
                              Length(max=100)
                          ])
    country = QuerySelectField(
        'Pays',
        validators=[DataRequired('Ce champs est obligatoire.')],
        query_factory=lambda: Country.query.order_by('name').all(),
        allow_blank=True,
        blank_text='Choisir un pays',
        get_label='name')