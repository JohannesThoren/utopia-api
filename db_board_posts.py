# Copyright (c) 2021 Johannes Thorén
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from uuid import UUID, uuid4
from datetime import datetime

import db_user

from response_codes import *
def new_post(mongo, board_id, token, content, title, flag="TEXT"):
      db = mongo.db.posts
      if db_user.auth_user(mongo, token):
            user_id, username = db_user.auth_user(mongo, token)

            # a post dict that will be used to add a new post to the database
            new_post = {
                  "title": title, 
                  "content": content, 
                  "board": UUID(board_id), 
                  "created": datetime.now(), 
                  "author": user_id, 
                  "flag": flag, 
                  "id": uuid4()
                  }

            db.insert(new_post)
            return {"response code": OK, "msg": "post created"}
      else:
            return {"response code": NOT_AUTHORIZED}      

def get_specific_post(mongo, post_id):
      db = mongo.db.posts
      post = db.find_one({"id": UUID(post_id)})
      if post:
            return {
                  "id": post["id"],
                  "title": post["title"],
                  "author": post["author"],
                  "board": post["board"],
                  "created": post["created"],
                  "content": post["content"],
                  "response code": Codes.ok
                  }
      else:
            return {"response code": NOT_FOUND}


def get_all_posts(mongo, board_id):
      db = mongo.db.posts
      posts = db.find({"board": UUID(board_id)})
      post_dict = {}
      index = 0

      if posts:
            for post in posts:
                  post_dict.update({f"{index}":{"title": post["title"],"id": post["id"], "content": post["content"], "author": post["author"], "created": post["created"]}})
                  index += 1

            return post_dict
      else:
            return {"response code": NOT_FOUND, "msg": "there are currently no posts"}


def delete_post(mongo, post_id, token):
      db = mongo.db.posts
      post = db.find_one({"id": UUID(post_id)})
      author_id, username = db_user.auth_user(mongo, token)
      if post:
            if post["author"] == author_id:
                  db.delete_one(post)
                  return {"response code": OK, "msg": "post deleted"}
            else:
                  return {"response code": NOT_AUTHORIZED}
      else:
            return {"response code": NOT_FOUND}
            