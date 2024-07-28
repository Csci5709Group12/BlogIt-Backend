from flask import Blueprint, request, jsonify
from app.services.blog_post_service import BlogPostService

blogs_bp = Blueprint('blogs', __name__, url_prefix='/blogs')

@blogs_bp.route('/create', methods=['POST'])
def create_blog_post():
    try:
        data = request.get_json()
        blog_id = data.get('blog_post_id')
        title = data.get('title')
        author = data.get('author')
        tags = data.get('tags')
        image_url = data.get('image_url')
        content = data.get('content')

        print(all([blog_id, title, author, tags, image_url, content]))

        if not all([blog_id, title, author, tags, image_url, content]):
            return jsonify({'error': 'Missing blog post parameters'}), 400

        BlogPostService.create_blog_post(
            blog_id,
            title,
            author,
            tags,
            image_url,
            content
        )

        return jsonify({'message': 'Post created successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An internal server error occurred: ' + str(e)}), 500

@blogs_bp.route('/get/all', methods=['GET'])
def get_all_videos():
    try:
        blogs = BlogPostService.get_all_blogs()

        return jsonify({'message': 'Retrieved Blogs successfully', 'blogs': blogs}), 200
    except Exception as e:
        return jsonify({'error': 'An internal server error occurred: ' + str(e)}), 500
    
@blogs_bp.route('/get/<blog_id>', methods=['GET'])
def get_video_post(blog_id):
    try:
        blog = BlogPostService.get_post_by_id(blog_id)
        if blog:
            return jsonify(blog), 200
        else:
            return jsonify({'error': 'Post not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blogs_bp.route('/edit/<id>', methods=['PUT'])
def edit_video_post(id):
    data = request.get_json()
    
    updates = {
        'title': data.get('title'),
        'content': data.get('content'),
        'tags': data.get('tags'),
        'time': data.get('time'),
        'author': data.get('author'),
        'thumbnail_url': data.get('thumbnail_url'),
        'video_url': data.get('video_url')
    }
    
    if not id:
        return jsonify({'error': 'Post ID is required'}), 400

    try:
        BlogPostService.edit_post_by_id(id, updates)
        return jsonify({'message': 'Post updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blogs_bp.route('/delete/<id>', methods=['DELETE'])
def delete_post(id):
    try:
        deleted_count = BlogPostService.delete_post_by_id(id)
        if deleted_count != 0:
            return jsonify({'message': 'Post deleted successfully'}), 200
        else:
            return jsonify({'error': 'Post not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500