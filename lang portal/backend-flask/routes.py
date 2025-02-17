from flask import jsonify, request
from app import app
from models import Word, Group, WordGroup, StudySession, WordReviewItem, db

@app.route('/words', methods=['GET'])
def get_words():
    page = int(request.args.get('page', 1))
    sort_by = request.args.get('sort_by', 'kanji')
    order = request.args.get('order', 'asc')

    query = Word.query.order_by(getattr(Word, sort_by).asc() if order == 'asc' else getattr(Word, sort_by).desc())
    paginated = query.paginate(page=page, per_page=10)

    return jsonify({
        'words': [word.to_dict() for word in paginated.items],
        'total_pages': paginated.pages,
        'current_page': paginated.page
    })

@app.route('/groups', methods=['GET'])
def get_groups():
    page = int(request.args.get('page', 1))
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')

    query = Group.query.order_by(getattr(Group, sort_by).asc() if order == 'asc' else getattr(Group, sort_by).desc())
    paginated = query.paginate(page=page, per_page=10)

    return jsonify({
        'groups': [group.to_dict() for group in paginated.items],
        'total_pages': paginated.pages,
        'current_page': paginated.page
    })

@app.route('/groups/<int:id>', methods=['GET'])
def get_group_words(id):
    page = int(request.args.get('page', 1))
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')

    group = Group.query.get_or_404(id)
    query = Word.query.join(WordGroup).filter_by(group_id=id).order_by(
        getattr(Word, sort_by).asc() if order == 'asc' else getattr(Word, sort_by).desc()
    )
    paginated = query.paginate(page=page, per_page=10)

    return jsonify({
        'group_name': group.name,
        'words': [word.to_dict() for word in paginated.items],
        'total_pages': paginated.pages,
        'current_page': paginated.page
    })

from flask import request

@app.route('/study_sessions', methods=['POST'])
def create_study_session():
    data = request.json
    group_id = data.get('group_id')
    study_activity_id = data.get('study_activity_id')

    session = StudySession(group_id=group_id, study_activity_id=study_activity_id)
    db.session.add(session)
    db.session.commit()

    return jsonify({'id': session.id}), 201

@app.route('/study_sessions/<int:id>/review', methods=['POST'])
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