# Copyright (c) 2021 Johannes Thorén
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import toml
import bcrypt
import secrets
from uuid import uuid4, UUID
from response_codes import *

import hashlib

settings = toml.load("settings.toml")


def get_token(mongo, username, password):
    '''
    Returns a dictionary with a response code and if a user with the specified username,
    and the password is correct, it will also return a token.
    '''
    db = mongo.db.users
    user = db.find_one({"username": username})
    if user:
        if bcrypt.checkpw(password.encode("UTF-8"), user["password"]):
            new_token = secrets.token_urlsafe(64)
            db.update({"username": username}, {"$set": {"token": new_token}})
            return {"response code": OK, "token": new_token}
        else:
            return {"response code": NOT_AUTHORIZED}
    else:
        return {"response code": NOT_FOUND}


def create_user(mongo, username, password, email, image=""):
    '''
    Checks if a user with the provided name exists and if not then create a user with that name,
    and returns the username.
    '''

    if image == "":
            pp_hash = hashlib.sha1(username.encode("UTF-8")).hexdigest()  
            image = f"https://www.gravatar.com/avatar/{pp_hash}?s=1024&d=identicon"
    
    
    db = mongo.db.users
    if not db.find_one({"username": username, "email": email}):
        password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())
        new_user = {"username": username, "email": email, "password": password,
                    "token": secrets.token_urlsafe(64), "id": uuid4(), "image": image, "following": []}
        db.insert(new_user)
        return {"response code": OK, "username": username}
    else:
        return {"response code": NOT_ALLOWED, "msg": "username or email already in use"}

# TODO make this function also remove all posts by the user


def delete_user(mongo, token):
    '''Deletes a user with the corresponding token'''
    db = mongo.db.users
    user = db.find_one({"token": UUID(token)})
    if user:
        db.delete_one(user)
        return {"response code": 200}
    else:
        return {"response code": 404}


def get_posts(mongo, user_id):
    '''all posts that a specific user has posted'''
    db = mongo.db.posts
    posts = db.find({"author": UUID(user_id)})
    post_dict = {}
    index = 0

    if posts:
        for post in posts:
                post_dict.update({f"{index}": {"title": post["title"], "id": post["id"], "content": post["content"],
                                 "author": post["author"], "created": post["created"], "flag": post["flag"], "board": post["board"]}})
                index += 1

        return post_dict
    else:
        return {"response code": NOT_FOUND}


def get_user_by_name(mongo, username):
    '''Returns a user by using the username to search through the database'''
    db = mongo.db.users
    user = db.find_one({"username": username})
    if user:
        return {"response code": 200, "username": user["username"], "id": user["id"], "profile_picture": user["image"]}
    else:
        return {"response code": 404}


def get_user_by_id(mongo, id):
    '''fetch a user with a specific id'''
    db = mongo.db.users
    user = db.find_one({"id": UUID(id)})
    if user:
        return {"response code": 200, "username": user["username"], "id": user["id"], "profile_picture": user["image"]}
    else:
        return {"response code": 404}


def get_user_by_token(mongo, token):
    '''fetch a user with a specific token (this will only be used by the owner of user account)'''

    db = mongo.db.users
    user = db.find_one({"token": token})
    if user:
        return {"response code": 200, "username": user["username"], "id": user["id"], "profile_picture": user["image"], "following": user["following"], "token":
            user["token"]}
    else:
        return {"response code": 404}


def get_user_owned_boards(mongo, id):
    '''gets the boars that a specific user owns'''
    db = mongo.db.boards
    boards = db.find({"owner": UUID(id)})
    boards_dict = {}
    index = 0
    if boards:
            for board in boards:
                    boards_dict.update({f"{index}": { "response code": OK,
                        "name": board["name"], "id": board["id"], "description": board["description"], "owner": board["owner"], "created": board["created"], "followers": board["followers"]}})
                    index += 1
            return boards_dict
    else:
        return {"response code": NOT_FOUND}   
             
def auth_user(mongo, token):
    '''checks if there is a user that has the specified token'''
    db = mongo.db.users
    user = db.find_one({"token": token})
    if user:
        return user["id"], user["username"]
    else:
        return False
