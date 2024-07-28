from pymongo.errors import PyMongoError
from app.mongo import MongoDB
from app.config import Config


class Bookmark:
    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id
        self.mongo = MongoDB(Config.MONGO_URI, Config.DATABASE_NAME)

    def save(self):
        try:
            collection = self.mongo.get_collection('bookmark')
            # Check if bookmark already exists
            try:
                existing = collection.find_one({
                    '_id': self.post_id,
                    'user_id': self.user_id
                })
            except Exception as e:
                print('Error ')
                print(e)
            if existing:
                return {"result": "Bookmark already exists"}

            # Insert new bookmark
            result = collection.insert_one({
                '_id': self.post_id,
                'user_id': self.user_id
            })
            return {"result": "success", "id": str(result.inserted_id)}
        except RuntimeError as e:
            print(f"Error: {e}")
            return {"result": "Runtime error"}
        except PyMongoError as e:
            print(f"MongoDB error while saving bookmark: {e}")
            return {"result": "MongoDB error"}

    @staticmethod
    def delete(user_id, post_id):
        try:
            mongo = MongoDB(Config.MONGO_URI, Config.DATABASE_NAME)
            collection = mongo.get_collection('bookmark')
            result = collection.delete_one({
                '_id': post_id,
                'user_id': user_id
            })
            if result.deleted_count == 0:
                return {"result": "Bookmark not found"}
            return {"result": "success", "deleted_count": result.deleted_count}
        except RuntimeError as e:
            print(f"Error: {e}")
            return {"result": "Runtime error"}
        except PyMongoError as e:
            print(f"MongoDB error while deleting bookmark: {e}")
            return {"result": "MongoDB error"}
