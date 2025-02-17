from flask import Blueprint, jsonify, request
from models import Word, db

words_bp = Blueprint('words', __name__)

@words_bp.route('/words', methods=['GET'])
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