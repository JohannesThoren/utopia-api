# Copyright (c) 2021 Johannes Thorén
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import db_user
import json
from uuid import uuid4, UUID
from datetime import datetime


def get_all_boards(mongo):
      db = mongo.db.boards
      boards = {}
      index = 0
      for board in db.find({}):
            boards.update({f"{index}": {"id": board["id"], "name": board["name"]}})
            index += 1

      return boards

def get_specific_board_by_id(mongo, id):
      db = mongo.db.boards
      board = db.find_one({"id": UUID(id)})
      if board:
            return {"response code": 200,"name": board["name"],"id": board["id"], "description": board["description"], "owner": board["owner"], "created": board["created"]}
      else:
            return {"response code": 404}

def get_specific_board_by_name(mongo, name):
      db = mongo.db.boards
      board = db.find_one({"name": name})
      if board:
            return {"response code": 200,"name": board["name"],"id": board["id"], "description": board["description"], "owner": board["owner"], "created": board["created"]}
      else:
            return {"response code": 404}
          

def create_board(mongo, name, description, token):
      db = mongo.db.boards

      owner_id, owner_username = db_user.auth_user(mongo, token)

      if owner_id:
            if not db.find_one({"name": name}):
                  board = {"id":uuid4(),"name": name, "description": description, "owner": owner_id, "created": datetime.now()}
                  db.insert(board)
                  return {"response code": 200}
            else:
                  return {"response code": 401}
      else:
            return {"response code": 403}


def delete_board(mongo, id, token):
      db = mongo.db.boards
      board = db.find_one({"id": UUID(id)})
      owner_id, owner_username = db_user.auth_user(mongo, token)
      
      if board:
            if board["owner"] == owner_id:
                  db.delete_one(board)
                  return {"response code": 200, "msg": "board deleted"}
            else:
                  return {"response code": 403}
      else:
            return {"response code": 404, "msg": "could not find any boards with that id!"}