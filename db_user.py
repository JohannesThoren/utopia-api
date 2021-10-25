# Copyright (c) 2021 Johannes Thorén
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import toml
import bcrypt
from uuid import uuid4, UUID

settings = toml.load("settings.toml")

def get_token(mongo, username, password):
    db = mongo.db.users
    user = db.find_one({"username": username})

    if bcrypt.checkpw(password.encode("UTF-8"), user["password"]):
        return {"response code": 200, "token": user["token"]}
    else:
        return {"response code": 401}


def create_user(mongo, username, password, email, image=str(settings["settings"]["url"]+"/profile_picture")):
    db = mongo.db.users

    if not db.find_one({"username": username}):
        password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())
        new_user = {"username": username, "email": email, "password": password,
                    "token": uuid4(), "id": uuid4(), "image": image}
        db.insert(new_user)
        return {"response code": 200, "username": username}
    else:
        return {"response code": 403}

def delete_user(mongo, token):
    db = mongo.db.users
    user = db.find_one({"token": UUID(token)})
    if user:
        db.delete_one(user)
        return {"response code": 200}
    else:
        return {"response code": 404}

def get_user_by_name(mongo, username):
    db = mongo.db.users
    user = db.find_one({"username": username})
    if user:
        return {"response code": 200, "username": user["username"], "id": user["id"], "profile_picture": user["image"]}
    else:
        return {"response code": 404}


def get_user_by_id(mongo, id):
    db = mongo.db.users
    user = db.find_one({"id": UUID(id)})
    if user:
        return {"response code": 200, "username": user["username"], "id": user["id"], "profile_picture": user["image"]}
    else:
        return {"response code": 404}


def get_user_by_token(mongo, token):
    print(token)
    db = mongo.db.users
    token = UUID(token)
    user = db.find_one({"token": token})
    if user:
        return {"response code": 200, "username": user["username"], "id": user["id"], "profile_picture": user["image"]}
    else:
        return {"response code": 404}

def auth_user(mongo, token):
    db = mongo.db.users
    token = UUID(token)
    user = db.find_one({"token": token})
    if user:
        return user["id"], user["username"]
    else:
        return False