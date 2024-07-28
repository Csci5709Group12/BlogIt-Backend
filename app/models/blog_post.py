from app.mongo import MongoDB
from app.config import Config
from pymongo.errors import PyMongoError

class BlogPost:
    def __init__(
        self,
        blog_post_id,
        title,
        author,
        tags,
        image_url,
        content,
    ):
        self.blog_post_id = blog_post_id
        self.title = title
        self.author = author
        self.tags = tags
        self.image_url = image_url
        self.content = content
        self.mongo = MongoDB(Config.MONGO_URI, Config.DATABASE_NAME)

    def save(self):
        try:
            collection = self.mongo.get_collection('blog_posts')
            collection.insert_one({
                '_id': self.blog_post_id,
                'title': self.title,
                'author': self.author,
                'tags': self.tags,
                'image_url': self.image_url,
                'content': self.content,
            })
            print(f"Video Post {self.title} saved successfully")
        except RuntimeError as e:
            print(f"Error: {e}")
        except PyMongoError as e:
            print(f"MongoDB error while saving video post: {e}")

    def edit(self, updates):
        try:
            collection = self.mongo.get_collection('blog_posts')
            result = collection.update_one(
                {'_id': self.blog_post_id},
                {'$set': updates}
            )
            if result.matched_count > 0:
                print(f"Blog Post {self.title} updated successfully")
            else:
                print(f"No matching video post found with ID {self.blog_post_id}")
        except RuntimeError as e:
            print(f"Error: {e}")
        except PyMongoError as e:
            print(f"MongoDB error while updating video post: {e}")

    @staticmethod
    def get_post_by_id(id):
        query = {"_id": int(id)}
        print(query)
        try:
            mongo = MongoDB(Config.MONGO_URI, Config.DATABASE_NAME)
            collection = mongo.get_collection("blog_posts")
            doc = collection.find_one(query)
            if doc:
                return convert_blog_post_doc_to_blog_post(doc)
            else:
                return None
        except RuntimeError as e:
            print(f"Error: {e}")
        except PyMongoError as e:
            print(f"MongoDB error while accessing MongoDB: {str(e)}")

    @staticmethod
    def get_all_posts():
        try:
            mongo = MongoDB(Config.MONGO_URI, Config.DATABASE_NAME)
            collection = mongo.get_collection('blog_posts')
            posts = list(collection.find({}))
            posts = [post for post in posts]
            return posts
        except RuntimeError as e:
            print(f"Error: {e}")
            return []
        except PyMongoError as e:
            print(f"MongoDB error while retrieving video post: {e}")
            return []

    @staticmethod
    def get_post_by_user_id(user_id):
        try:
            mongo = MongoDB(Config.MONGO_URI, Config.DATABASE_NAME)
            collection = mongo.get_collection('blog_posts')
            post = collection.find_one({'author': user_id})
            return post
        except RuntimeError as e:
            print(f"Error: {e}")
            return None
        except PyMongoError as e:
            print(f"MongoDB error while retrieving blog post: {e}")
            return None

    @staticmethod
    def delete_post_by_id(post_id):
        try:
            mongo = MongoDB(Config.MONGO_URI, Config.DATABASE_NAME)
            collection = mongo.get_collection('blog_posts')
            result = collection.delete_one({'_id': post_id})
            return result.deleted_count
        except RuntimeError as e:
            print(f"Error: {e}")
            return 0
        except PyMongoError as e:
            print(f"MongoDB error while deleting blog post: {e}")
            return 0

def convert_blog_post_doc_to_blog_post(document):
    if document:
        return {
            "blog_post_id": document["_id"],
            "title": document["title"],
            "author": document["author"],
            "tags": document["tags"],
            "image_url": document["image_url"],
            "content": document["content"]
        }
    else:
        return None