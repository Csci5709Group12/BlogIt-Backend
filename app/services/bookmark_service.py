from app.models.bookmark import Bookmark


class BookmarkService:
    @staticmethod
    def add_bookmark(user_id, post_id):
        bookmark = Bookmark(user_id, post_id)
        response = bookmark.save()
        if response["result"] == "success":
            return {"success": True, "message": "Bookmark added successfully."}
        elif response["result"] == "Bookmark already exists":
            return {"success": False, "message": response["result"]}
        return {"success": False, "message": response["result"]}

    @staticmethod
    def remove_bookmark(user_id, post_id):
        response = Bookmark.delete(user_id, post_id)
        if response["result"] == "success":
            return {"success": True, "message": "Bookmark removed successfully."}
        return {"success": False, "message": response["result"]}
