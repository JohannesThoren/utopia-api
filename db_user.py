# Copyright (c) 2021 Johannes Thorén
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import toml
import bcrypt
from response_codes import Codes
from uuid import uuid4, UUID

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
            return {"response code": Codes.ok, "token": user["token"]}
        else:
            return {"response code": Codes.not_authorized}
    else:
        return {"response code": Codes.not_found}


def create_user(mongo, username, password, email, image=str(settings["settings"]["url"]+"/profile_picture")):
    '''
    Checks if a user with the provided name exists and if not then create a user with that name,
    and returns the username.
    '''

    db = mongo.db.users
    if not db.find_one({"username": username}):
        password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())
        new_user = {"username": username, "email": email, "password": password,
                    "token": uuid4(), "id": uuid4(), "image": image}
        db.insert(new_user)
        return {"response code": Codes.ok, "username": username}
    else:
        return {"response code": Codes.not_allowed}

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
    token = UUID(token)
    user = db.find_one({"token": token})
    if user:
        return {"response code": 200, "username": user["username"], "id": user["id"], "profile_picture": user["image"]}
    else:
        return {"response code": 404}


def auth_user(mongo, token):
    '''checks if there is a user that has the specified token'''
    db = mongo.db.users
    token = UUID(token)
    user = db.find_one({"token": token})
    if user:
        return user["id"], user["username"]
    else:
        return False
