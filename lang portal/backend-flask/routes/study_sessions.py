from flask import Blueprint, jsonify, request
from models import StudySession, WordReviewItem, Word, db

study_sessions_bp = Blueprint('study_sessions', __name__)

@study_sessions_bp.route('/study_sessions', methods=['POST'])
def create_study_session():
    data = request.json
    group_id = data.get('group_id')
    study_activity_id = data.get('study_activity_id')

    session = StudySession(group_id=group_id, study_activity_id=study_activity_id)
    db.session.add(session)
    db.session.commit()

    return jsonify({'id': session.id}), 201

@study_sessions_bp.route('/study_sessions/<int:id>/review', methods=['POST'])
def log_review(id):
    data = request.json
    word_id = data.get('word_id')
    correct = data.get('correct')

    review = WordReviewItem(word_id=word_id, study_session_id=id, correct=correct)
    word = Word.query.get(word_id)

    if word:
        if correct:
            word.correct_count += 1
        else:
            word.wrong_count += 1

    db.session.add(review)
    db.session.commit()

    return jsonify({'message': 'Review logged successfully'}), 201