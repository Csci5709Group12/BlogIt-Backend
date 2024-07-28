from flask import Blueprint, request, jsonify
from app.services.bookmark_service import BookmarkService

bookmark_bp = Blueprint('bookmarks', __name__, url_prefix='/bookmarks')


@bookmark_bp.route('/add', methods=['OPTIONS'])
def bookmarks_add_options():
    return '', 200


@bookmark_bp.route('/add', methods=['POST'])
def add_bookmark():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        post_id = data.get('post_id')

        if not user_id or not post_id:
            return jsonify({'error': 'Missing parameters'}), 400

        result = BookmarkService.add_bookmark(user_id, post_id)
        if result['success']:
            return jsonify({'message': result['message']}), 200
        else:
            return jsonify({'error': result['message']}), 500
    except Exception as e:
        return jsonify({'error': f'An internal server error occurred: {e}'}), 500


@bookmark_bp.route('/remove', methods=['OPTIONS'])
def bookmarks_remove_options():
    return '', 200


@bookmark_bp.route('/remove', methods=['POST'])
def remove_bookmark():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        post_id = data.get('post_id')

        if not user_id or not post_id:
            return jsonify({'error': 'Missing parameters'}), 400

        result = BookmarkService.remove_bookmark(user_id, post_id)
        if result['success']:
            return jsonify({'message': result['message']}), 200
        else:
            return jsonify({'error': result['message']}), 404
    except Exception as e:
        return jsonify({'error': f'An internal server error occurred: {e}'}), 500
