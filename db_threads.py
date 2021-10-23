# Copyright (c) 2021 Johannes Thorén
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import db_user
import json
from uuid import uuid4, UUID
from datetime import datetime


def get_all_threads(mongo):
      db = mongo.db.threads
      threads = {}
      index = 0
      for thread in db.find({}):
            threads.update({f"{index}": {"id": thread["id"], "name": thread["name"]}})
            index += 1

      return threads

def get_specific_thread_by_id(mongo, id):
      db = mongo.db.threads
      thread = db.find_one({"id": UUID(id)})
      if thread:
            return {"response code": 200,"name": thread["name"],"id": thread["id"], "description": thread["description"], "author": thread["author"], "created": thread["created"]}
      else:
            return {"response code": 404}

def get_specific_thread_by_name(mongo, name):
      db = mongo.db.threads
      thread = db.find_one({"name": name})
      if thread:
            return {"response code": 200,"name": thread["name"],"id": thread["id"], "description": thread["description"], "author": thread["author"], "created": thread["created"]}
      else:
            return {"response code": 404}
          

def create_thread(mongo, name, description, token):
      db = mongo.db.threads

      author_id, author_username = db_user.auth_user(mongo, token)

      if author_id:
            if not db.find_one({"name": name}):
                  thread = {"id":uuid4(),"name": name, "description": description, "author": author_id, "created": datetime.now()}
                  db.insert(thread)
                  return {"response code": 200}
            else:
                  return {"response code": 401}
      else:
            return {"response code": 403}