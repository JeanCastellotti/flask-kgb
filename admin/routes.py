from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required
from models import Mission, Country, Agent, Speciality, Type, Contact, Hideout, Target
from .forms import MissionForm, CountryForm, AgentForm, SpecialityForm, TypeForm, ContactForm, HideoutForm, TargetForm
from app import db

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/missions')
@login_required
def missions():
    page = request.args.get('page', 1, type=int)
    missions = Mission.query.order_by(Mission.id.desc()).paginate(page=page,
                                                                  per_page=5)
    return render_template('admin/missions.html', missions=missions)


@admin.route('/missions/create', methods=['GET', 'POST'])
@login_required
def create_mission():
    form = MissionForm()
    if form.validate_on_submit():
        mission = Mission(title=form.title.data,
                          description=form.description.data,
                          code=form.code.data,
                          country=form.country.data,
                          type=form.type.data,
                          required_speciality=form.required_speciality.data,
                          starts_at=form.starts_at.data,
                          ends_at=form.ends_at.data,
                          agents=form.agents.data,
                          targets=form.targets.data,
                          contacts=form.contacts.data,
                          hideouts=form.hideouts.data)
        db.session.add(mission)
        db.session.commit()
        flash('La mission a été créée.', 'success')
        return redirect(url_for('admin.missions'))

    return render_template('admin/mission-form.html', form=form)


@admin.route('/missions/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_mission(id):
    mission = Mission.query.get_or_404(id)
    form = MissionForm()
    if form.validate_on_submit():
        mission.title = form.title.data
        mission.description = form.description.data
        mission.code = form.code.data
        mission.country = form.country.data
        mission.type = form.type.data
        mission.required_speciality = form.required_speciality.data
        mission.status = form.status.data or mission.status
        mission.starts_at = form.starts_at.data
        mission.ends_at = form.ends_at.data
        mission.agents = form.agents.data
        mission.targets = form.targets.data
        mission.contacts = form.contacts.data
        mission.hideouts = form.hideouts.data
        db.session.commit()
        flash('La mission a été modifiée.', 'success')
        return redirect(url_for('admin.missions'))
    if request.method == 'GET':
        form.title.data = mission.title
        form.description.data = mission.description
        form.code.data = mission.code
        form.country.data = mission.country
        form.type.data = mission.type
        form.required_speciality.data = mission.required_speciality
        form.status.data = mission.status
        form.starts_at.data = mission.starts_at
        form.ends_at.data = mission.ends_at
        form.agents.data = mission.agents
        form.targets.data = mission.targets
        form.contacts.data = mission.contacts
        form.hideouts.data = mission.hideouts
    return render_template('admin/mission-form.html',
                           mission=mission,
                           form=form,
                           edit=True)


@admin.route('/missions/<int:id>/delete', methods=['POST'])
@login_required
def delete_mission(id):
    mission = Mission.query.get_or_404(id)
    db.session.delete(mission)
    db.session.commit()
    flash('La mission a été supprimée.', 'success')
    return redirect(url_for('admin.missions'))


@admin.route('/countries')
@login_required
def countries():
    countries = Country.query.order_by('name').all()
    return render_template('admin/countries.html', countries=countries)


@admin.route('/countries/create', methods=['GET', 'POST'])
@login_required
def create_country():
    form = CountryForm()
    if form.validate_on_submit():
        country = Country(name='-'.join(form.name.data.title().split()),
                          nationality=form.nationality.data.capitalize())
        db.session.add(country)
        db.session.commit()
        flash('Le pays a été ajouté.', 'success')
        return redirect(url_for('admin.countries'))
    return render_template('admin/country-form.html', form=form)


@admin.route('/countries/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_country(id):
    country = Country.query.get_or_404(id)
    form = CountryForm()
    if form.validate_on_submit():
        country.name = form.name.data.capitalize()
        country.nationality = form.nationality.data.capitalize()
        db.session.commit()
        flash('Le pays a été modifié.', 'success')
        return redirect(url_for('admin.countries'))
    if request.method == 'GET':
        form.name.data = country.name
        form.nationality.data = country.nationality
    return render_template('admin/country-form.html', form=form, edit=True)


@admin.route('/countries/<int:id>/delete', methods=['POST'])
@login_required
def delete_country(id):
    country = Country.query.get_or_404(id)
    try:
        db.session.delete(country)
        db.session.commit()
    except:
        flash('Ce pays ne peut pas être supprimé.', 'danger')
        return redirect(url_for('admin.countries'))
    flash('Le pays a été supprimé.', 'success')
    return redirect(url_for('admin.countries'))


@admin.route('/specialities')
@login_required
def specialities():
    specialities = Speciality.query.order_by('name').all()
    return render_template('admin/specialities.html',
                           specialities=specialities)


@admin.route('/specialities/create', methods=['GET', 'POST'])
@login_required
def create_speciality():
    form = SpecialityForm()
    if form.validate_on_submit():
        spciality = Speciality(name=form.name.data.title())
        db.session.add(spciality)
        db.session.commit()
        flash('La spécialité a été ajoutée.', 'success')
        return redirect(url_for('admin.specialities'))
    return render_template('admin/speciality-form.html', form=form)


@admin.route('/specialities/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_speciality(id):
    speciality = Speciality.query.get_or_404(id)
    form = SpecialityForm()
    if form.validate_on_submit():
        speciality.name = form.name.data.title()
        db.session.commit()
        flash('La spécialité a été modifiée.', 'success')
        return redirect(url_for('admin.specialities'))
    if request.method == 'GET':
        form.name.data = speciality.name
    return render_template('admin/speciality-form.html', form=form, edit=True)


@admin.route('/specialities/<int:id>/delete', methods=['POST'])
@login_required
def delete_speciality(id):
    speciality = Speciality.query.get_or_404(id)
    try:
        db.session.delete(speciality)
        db.session.commit()
    except:
        flash('Cette spécialité ne peut pas être supprimée.', 'danger')
        return redirect(url_for('admin.specialities'))
    flash('La spécialité a été supprimée.', 'success')
    return redirect(url_for('admin.specialities'))


@admin.route('/types')
@login_required
def types():
    types = Type.query.order_by('name').all()
    return render_template('admin/types.html', types=types)


@admin.route('/types/create', methods=['GET', 'POST'])
@login_required
def create_type():
    form = TypeForm()
    if form.validate_on_submit():
        spciality = Type(name=form.name.data.title())
        db.session.add(spciality)
        db.session.commit()
        flash('Le type a été ajouté.', 'success')
        return redirect(url_for('admin.types'))
    return render_template('admin/type-form.html', form=form)


@admin.route('/types/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_type(id):
    type = Type.query.get_or_404(id)
    form = TypeForm()
    if form.validate_on_submit():
        type.name = form.name.data.title()
        db.session.commit()
        flash('Le type a été modifié.', 'success')
        return redirect(url_for('admin.types'))
    if request.method == 'GET':
        form.name.data = type.name
    return render_template('admin/type-form.html', form=form, edit=True)


@admin.route('/types/<int:id>/delete', methods=['POST'])
@login_required
def delete_type(id):
    type = Type.query.get_or_404(id)
    try:
        db.session.delete(type)
        db.session.commit()
    except:
        flash('Ce type ne peut pas être supprimé', 'danger')
        return redirect(url_for('admin.types'))
    flash('Le type a été supprimé.', 'success')
    return redirect(url_for('admin.types'))


@admin.route('/agents')
@login_required
def agents():
    agents = Agent.query.all()
    return render_template('admin/agents.html', agents=agents)


@admin.route('/agents/create', methods=['GET', 'POST'])
@login_required
def create_agent():
    form = AgentForm()
    if form.validate_on_submit():
        agent = Agent(firstname=form.firstname.data,
                      lastname=form.lastname.data,
                      birthdate=form.birthdate.data,
                      code=form.code.data,
                      country=form.nationality.data,
                      speciality=form.speciality.data)
        db.session.add(agent)
        db.session.commit()
        flash("L'agent a été créé.", 'success')
        return redirect(url_for('admin.agents'))
    return render_template('admin/agent-form.html', form=form)


@admin.route('/agents/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_agent(id):
    agent = Agent.query.get_or_404(id)
    form = AgentForm()
    if form.validate_on_submit():
        agent.firstname = form.firstname.data
        agent.lastname = form.lastname.data
        agent.birthdate = form.birthdate.data
        agent.code = form.code.data
        agent.country = form.nationality.data
        agent.speciality = form.speciality.data
        db.session.commit()
        flash("L'agent a été modifié.", 'success')
        return redirect(url_for('admin.agents'))
    if request.method == 'GET':
        form.firstname.data = agent.firstname
        form.lastname.data = agent.lastname
        form.birthdate.data = agent.birthdate
        form.code.data = agent.code
        form.nationality.data = agent.country
        form.speciality.data = agent.speciality
    return render_template('admin/agent-form.html', form=form, edit=True)


@admin.route('/agents/<int:id>/delete', methods=['POST'])
@login_required
def delete_agent(id):
    agent = Agent.query.get_or_404(id)
    if agent.missions:
        flash('Cet agent ne peut pas être supprimé.', 'danger')
    else:
        db.session.delete(agent)
        db.session.commit()
        flash("L'agent a été supprimé.", 'success')
    return redirect(url_for('admin.agents'))


@admin.route('/targets')
@login_required
def targets():
    targets = Target.query.all()
    return render_template('admin/targets.html', targets=targets)


@admin.route('/targets/create', methods=['GET', 'POST'])
@login_required
def create_target():
    form = TargetForm()
    if form.validate_on_submit():
        target = Target(firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        birthdate=form.birthdate.data,
                        code=form.code.data,
                        country=form.nationality.data)
        db.session.add(target)
        db.session.commit()
        flash('La cible a été créée.', 'success')
        return redirect(url_for('admin.targets'))
    return render_template('admin/target-form.html', form=form)


@admin.route('/targets/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_target(id):
    target = Target.query.get_or_404(id)
    form = TargetForm()
    if form.validate_on_submit():
        target.firstname = form.firstname.data
        target.lastname = form.lastname.data
        target.birthdate = form.birthdate.data
        target.code = form.code.data
        target.country = form.nationality.data
        db.session.commit()
        flash('La cible a été modifiée.', 'success')
        return redirect(url_for('admin.targets'))
    if request.method == 'GET':
        form.firstname.data = target.firstname
        form.lastname.data = target.lastname
        form.birthdate.data = target.birthdate
        form.code.data = target.code
        form.nationality.data = target.country
    return render_template('admin/target-form.html', form=form, edit=True)


@admin.route('/targets/<int:id>/delete', methods=['POST'])
@login_required
def delete_target(id):
    target = Target.query.get_or_404(id)
    if target.missions:
        flash('Cette cible ne peut pas être supprimé.', 'danger')
    else:
        db.session.delete(target)
        db.session.commit()
        flash('La cible a été supprimée.', 'success')
    return redirect(url_for('admin.targets'))


@admin.route('/contacts')
@login_required
def contacts():
    contacts = Contact.query.all()
    return render_template('admin/contacts.html', contacts=contacts)


@admin.route('/contacts/create', methods=['GET', 'POST'])
@login_required
def create_contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(firstname=form.firstname.data,
                          lastname=form.lastname.data,
                          birthdate=form.birthdate.data,
                          code=form.code.data,
                          country=form.nationality.data)
        db.session.add(contact)
        db.session.commit()
        flash('Le contact a été créé.', 'success')
        return redirect(url_for('admin.contacts'))
    return render_template('admin/contact-form.html', form=form)


@admin.route('/contacts/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    form = ContactForm()
    if form.validate_on_submit():
        contact.firstname = form.firstname.data
        contact.lastname = form.lastname.data
        contact.birthdate = form.birthdate.data
        contact.code = form.code.data
        contact.country = form.nationality.data
        db.session.commit()
        flash('La cible a été modifiée.', 'success')
        return redirect(url_for('admin.contacts'))
    if request.method == 'GET':
        form.firstname.data = contact.firstname
        form.lastname.data = contact.lastname
        form.birthdate.data = contact.birthdate
        form.code.data = contact.code
        form.nationality.data = contact.country
    return render_template('admin/contact-form.html', form=form, edit=True)


@admin.route('/contacts/<int:id>/delete', methods=['POST'])
@login_required
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    if contact.missions:
        flash('Ce contact ne peut pas être supprimé.', 'danger')
    else:
        db.session.delete(contact)
        db.session.commit()
        flash('Le contact a été supprimé.', 'success')
    return redirect(url_for('admin.contacts'))


@admin.route('/hideouts')
@login_required
def hideouts():
    hideouts = Hideout.query.all()
    return render_template('admin/hideouts.html', hideouts=hideouts)


@admin.route('/hideouts/create', methods=['GET', 'POST'])
@login_required
def create_hideout():
    form = HideoutForm()
    if form.validate_on_submit():
        hideout = Hideout(code=form.code.data,
                          address=form.address.data,
                          country=form.country.data)
        db.session.add(hideout)
        db.session.commit()
        flash('La planque a été créée.', 'success')
        return redirect(url_for('admin.hideouts'))
    return render_template('admin/hideout-form.html', form=form)


@admin.route('/hideouts/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_hideout(id):
    hideout = Hideout.query.get_or_404(id)
    form = HideoutForm()
    if form.validate_on_submit():
        hideout.code = form.code.data
        hideout.address = form.address.data
        hideout.country = form.country.data
        db.session.commit()
        flash('La planque a été modifiée.', 'success')
        return redirect(url_for('admin.hideouts'))
    if request.method == 'GET':
        form.code.data = hideout.code
        form.address.data = hideout.address
        form.country.data = hideout.country
    return render_template('admin/hideout-form.html', form=form, edit=True)


@admin.route('/hideouts/<int:id>/delete', methods=['POST'])
@login_required
def delete_hideout(id):
    hideout = Hideout.query.get_or_404(id)
    db.session.delete(hideout)
    db.session.commit()
    flash('La planque a été supprimée.', 'success')
    return redirect(url_for('admin.hideouts'))
