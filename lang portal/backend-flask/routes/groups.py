from flask import Blueprint, jsonify, request
from models import Group, Word, WordGroup, db

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/groups', methods=['GET'])
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

@groups_bp.route('/groups/<int:id>', methods=['GET'])
def get_group_words(id):
    page = int(request.args.get('page', 1))
    sort_by = request.args.get('sort_by', 'kanji')
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