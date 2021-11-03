from flask import render_template, Blueprint
from models import Mission

main = Blueprint('main', __name__)


@main.route('/')
def index():
    missions = Mission.query.all()
    return render_template('index.html', missions=missions)


@main.route('/mission/<int:id>')
def mission(id):
    mission = Mission.query.get_or_404(id)
    print(mission.agents)
    return render_template('mission.html', mission=mission)