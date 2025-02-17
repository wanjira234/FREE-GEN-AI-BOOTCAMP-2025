from flask import Blueprint, jsonify
from models import Word, StudySession, WordReviewItem

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    total_words = Word.query.count()
    total_sessions = StudySession.query.count()
    total_reviews = WordReviewItem.query.count()

    return jsonify({
        'total_words': total_words,
        'total_study_sessions': total_sessions,
        'total_reviews': total_reviews
    })