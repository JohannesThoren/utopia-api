import json

from datetime import datetime
from uuid import uuid4, UUID
from db_user import auth_user

import response_codes


def new_comment(mongo, comment, post_id, token):
    '''
    Creates a new comment on a specific post.
    '''
    db = mongo.db.comments
    user_id, username = auth_user(mongo, token)

    if len(comment) <= 500:

        if user_id:
            db.insert({"id": uuid4(), "user": user_id,
                       "date": datetime.now(), "post": post_id, "comment": comment})
            return {"msg": "Success", "response code": response_codes.OK}
        else:
            return {"err": "could not authorize"}
    else:
        return {"msg": "comment to long, comment has to be less than 500 characters!", "response code": response_codes.NOT_ALLOWED}


def delete_comment(mongo, comment_id, post_id, token):
    '''deletes a comment'''
    db = mongo.db.comments
    user_id, username = auth_user(mongo, token)
    comment = db.find({"id": comment_id, "post": post_id})

    if user_id:
        if user_id == comment["id"]:
            db.delete(comment)
            return {"msg": "Success", "response code": response_codes.OK}
        else:
            return {"err": "you are not the author of this comment"}
    else:
        return {"err": "could not authorize"}


def get_comment(mongo, comment_id):
    '''fetches a specific comment by its comment id'''
    db = mongo.db.comments
    comment = db.find({"id": comment_id})
    if comment:
        return {"id": comment["id"], "user": comment["user"], "date": comment["date"], "post": comment["post"]}
    else:
        return {"err": "could not find a post with that id"}


def get_comments_for_post(mongo, post_id):
    '''gets all comments for a specific post'''
    db = mongo.db.comments
    comments = db.find({"post": post_id})
    index = 0
    comments_obj = {}

    if comments:
        for comment in comments:
            comments_obj.update(
                {index: {"id": comment["id"], "comment": comment["comment"], "user": comment["user"], "date": comment["date"], "post": comment["post"]}})
            index += 1
        return comments_obj
    else:
        return {"msg": "There are no comments for this post yet", "response code": response_codes.NOT_FOUND}
