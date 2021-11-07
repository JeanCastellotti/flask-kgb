from flask import render_template, Blueprint, request
from models import Mission

main = Blueprint('main', __name__)


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    missions = Mission.query.order_by(Mission.id.desc()).paginate(page=page,
                                                                  per_page=5)
    return render_template('index.html', missions=missions)


@main.route('/mission/<int:id>')
def mission(id):
    mission = Mission.query.get_or_404(id)
    return render_template('mission.html', mission=mission)