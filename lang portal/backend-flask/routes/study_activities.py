from flask import Blueprint, jsonify, request
from models import StudyActivity, db

study_activities_bp = Blueprint('study_activities', __name__)

@study_activities_bp.route('/study_activities', methods=['GET'])
def get_study_activities():
    activities = StudyActivity.query.all()
    return jsonify([activity.to_dict() for activity in activities])