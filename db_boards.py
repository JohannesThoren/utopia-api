# Copyright (c) 2021 Johannes Thorén
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import db_user
import json
import pymongo
from uuid import uuid4, UUID
from datetime import datetime


from response_codes import *
from db_user import auth_user


def update_board_helper(mongo, token, db, settings, board):
    user_id, username = auth_user(mongo, token)
    if user_id == UUID(board["owner"]):
        db.update({"id": board["id"]}, {"$set": {"name": settings["name"], "owner": settings["owner"], "description": settings["description"]}})
        return {"msg": "settings changed", "response code": OK}
    else:
        return {"response code": NOT_FOUND, "err": "you are not the owner of this board, So changing the settings are therefor not possible"}


def update_board_settings(mongo, token, settings, board_id):
    db = mongo.db.boards
    board = db.find_one({"id": UUID(board_id)})
    name_check_board = db.find_one({"name": settings["name"]})
    user_id, username = auth_user(mongo, token)
    if not db.find_one({"name": settings["name"]}):
        return update_board_helper(mongo, token, db, settings, board)
    elif name_check_board["id"] == UUID(board_id):
        return update_board_helper(mongo, token, db, settings, board)
    else:
        return {"err": "a board with that name already exists", "response code": NOT_ALLOWED}


def user_follow_board(mongo, token, board_id):
    db = mongo.db.users
    user = db.find_one({"token": token})
    following = user["following"]
    if not board_id in following:
        following.append(board_id)
        if db.update({"token": token}, {"$set": {"following": following}}):
            board_followers = mongo.db.boards.find_one(
                {"id": UUID(board_id)})["followers"]
            mongo.db.boards.update({"id": UUID(board_id)}, {
                                   "$set": {"followers": board_followers + 1}})
            return {"response code": OK}
        else:
            return {"response code": NOT_AUTHORIZED}
    else:
        return {"response code": NOT_ALLOWED}


def user_unfollow_board(mongo, token, board_id):
    db = mongo.db.users
    user = db.find_one({"token": token})
    following = user["following"]

    if board_id in following:
        following.remove(board_id)
        if db.update({"token": token}, {"$set": {"following": following}}):
            board_followers = mongo.db.boards.find_one(
                {"id": UUID(board_id)})["followers"]
            mongo.db.boards.update({"id": UUID(board_id)}, {
                                   "$set": {"followers": board_followers - 1}})
            return {"response code": OK}
        else:
            return {"response code": NOT_ALLOWED}
    else:
        return {"response code": NOT_FOUND}


def get_all_boards(mongo):
    db = mongo.db.boards
    boards = {}
    index = 0
    for board in db.find({}).sort("created", pymongo.DESCENDING):
        boards.update({f"{index}": {"id": board["id"], "name": board["name"],
                      "followers": board["followers"], "created": board["created"]}})
        index += 1

    return boards


def get_n_most_followed_boards(mongo, n):
    n = int(n)
    db = mongo.db.boards
    boards = db.find({}).sort("followers", pymongo.DESCENDING).limit(n)
    boards_dict = {}
    index = 0

    if boards:
        for board in boards:
            boards_dict.update({f"{index}": {"name": board["name"], "id": board["id"], "description": board["description"],
                               "owner": board["owner"], "created": board["created"], "followers": board["followers"]}})
            index += 1
        return boards_dict
    return {"response code": NOT_FOUND}


def get_specific_board_by_id(mongo, id):
    db = mongo.db.boards
    try:
        board = db.find_one({"id": UUID(id)})
    except Exception as e:
        return {"response code": 404, "msg": str(e)}
    if board:
        return {"response code": 200, "name": board["name"], "id": board["id"], "description": board["description"], "owner": board["owner"], "created": board["created"], "followers": board["followers"]}
    else:
        return {"response code": 404}


def get_specific_board_by_name(mongo, name):
    db = mongo.db.boards
    board = db.find_one({"name": name})
    if board:
        return {"response code": 200, "name": board["name"], "id": board["id"], "description": board["description"], "owner": board["owner"], "created": board["created"], "followers": board["followers"]}
    else:
        return {"response code": 404}


def create_board(mongo, name, description, token):
    db = mongo.db.boards

    owner_id, owner_username = db_user.auth_user(mongo, token)

    if owner_id:
        if not db.find_one({"name": name}):
            board = {"id": uuid4(), "name": name, "description": description,
                     "owner": owner_id, "created": datetime.now(), "followers": 0}
            db.insert(board)
            return {"response code": 200}
        else:
            return {"response code": 401}
    else:
        return {"response code": 403}


def delete_board(mongo, id, token):
    db = mongo.db.boards
    db_deleted_boards = mongo.db.deleted_boards
    board = db.find_one({"id": UUID(id)})
    owner_id, owner_username = db_user.auth_user(mongo, token)

    if board:
        if board["owner"] == owner_id:
            db_deleted_boards.insert(board)
            db.delete_one(board)
            return {"response code": 200, "msg": "board deleted"}
        else:
            return {"response code": 403}
    else:
        return {"response code": 404, "msg": "could not find any boards with that id!"}
