from app.models.blog_post import BlogPost

class BlogPostService:
    @staticmethod
    def create_blog_post(
        blog_post_id,
        title,
        author,
        tags,
        image_url,
        content
    ):
        blogPost = BlogPost(
            blog_post_id,
            title,
            author,
            tags,
            image_url,
            content
        )
        blogPost.save()

    @staticmethod
    def get_post_by_id(id):
        return BlogPost.get_post_by_id(id)

    @staticmethod
    def get_all_blogs():
        return BlogPost.get_all_posts()
    
    @staticmethod
    def get_post_by_user_id(user_id):
        return BlogPost.get_post_by_user_id(user_id)

    @staticmethod
    def edit_post_by_id(blog_post_id, updates):
        blogPost = BlogPost.get_post_by_id(blog_post_id)
        if blogPost:
            blogPost.edit(updates)
        else:
            print(f"No blog post found with ID {blog_post_id}")

    @staticmethod
    def delete_post_by_id(id):
        return BlogPost.delete_post_by_id(id)